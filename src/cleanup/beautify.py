import bpy
import math
import mathutils
import bmesh
from bpy.types import Operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class OBJECT_OT_beautify_mesh(Operator):
    bl_label = "Beautify Mesh"
    bl_idname = "object.beautify_mesh"
    bl_description = "Fix mesh topology, optimize geometry, and improve shading"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return (context.mode == 'OBJECT' and
                context.selected_objects and
                any(obj.type == 'MESH' for obj in context.selected_objects))
    
    def beautify_mesh(self, obj, context):
        # Create BMesh for direct mesh manipulation
        me = obj.data
        bm = bmesh.new()
        bm.from_mesh(me)
        
        # Fix normals using BMesh operations
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        
        # Check if normals need to be flipped
        center = sum((v.co for v in bm.verts), mathutils.Vector()) / len(bm.verts)
        inward_count = sum(1 for f in bm.faces if (center - f.calc_center_median()).dot(f.normal) > 0)
        
        if inward_count > len(bm.faces) / 2:
            bmesh.ops.reverse_faces(bm, faces=bm.faces)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        
        # Clean up mesh using BMesh operations
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.0001)
        
        # Delete loose geometry
        loose_verts = [v for v in bm.verts if not v.link_edges]
        loose_edges = [e for e in bm.edges if not e.link_faces]
        if loose_verts:
            bmesh.ops.delete(bm, geom=loose_verts, context='VERTS')
        if loose_edges:
            bmesh.ops.delete(bm, geom=loose_edges, context='EDGES')
        
        # Convert triangles to quads
        bmesh.ops.join_triangles(bm, faces=bm.faces, 
                                angle_face_threshold=math.radians(40),
                                angle_shape_threshold=math.radians(180))
        
        # Update mesh
        bm.to_mesh(me)
        me.update()
        bm.free()
        
        # Setup shading
        me.use_auto_smooth = True
        me.auto_smooth_angle = math.radians(40)
        me.clear_custom_split_normals()
        obj.shade_smooth()
        
        # Add modifiers in proper order
        self.setup_modifiers(obj)
    
    def setup_modifiers(self, obj):
        def ensure_modifier(name, type, settings=None):
            mod = obj.modifiers.get(name)
            if not mod:
                mod = obj.modifiers.new(name=name, type=type)
            if settings:
                for attr, value in settings.items():
                    setattr(mod, attr, value)
            return mod
        
        # Topology modifiers
        weld = ensure_modifier('Weld', 'WELD', {
            'merge_threshold': 0.0005
        })
        
        decimate = ensure_modifier('DecimateAngle', 'DECIMATE', {
            'decimate_type': 'DISSOLVE',
            'angle_limit': 0.1
        })
        
        # Shape modifiers
        bevel = ensure_modifier('Bevel', 'BEVEL', {
            'width': 0.01,
            'segments': 2,
            'limit_method': 'ANGLE',
            'angle_limit': math.radians(40),
            'harden_normals': True,
            'miter_outer': 'MITER_ARC'
        })
        
        # Normal modifiers
        weighted = ensure_modifier('WeightedNormal', 'WEIGHTED_NORMAL', {
            'weight': 100,
            'keep_sharp': True,
            'mode': 'FACE_AREA_WITH_ANGLE'
        })
        
        # Ensure correct modifier order
        if weld and decimate:
            while obj.modifiers.find(weld.name) > obj.modifiers.find(decimate.name):
                obj.modifiers.move(obj.modifiers.find(weld.name), obj.modifiers.find(decimate.name))
    
    def process_child_hierarchy(self, parent_obj, child_obj):
        if child_obj.type != 'MESH':
            return
            
        # Copy parent modifiers
        for pm in parent_obj.modifiers:
            if pm.name == 'NormalTransfer' or pm.name in child_obj.modifiers:
                continue
                
            cm = child_obj.modifiers.new(name=pm.name, type=pm.type)
            # Copy relevant properties based on modifier type
            if pm.type == 'BEVEL':
                props = ['width', 'segments', 'limit_method', 'angle_limit', 'harden_normals', 'miter_outer']
            elif pm.type == 'WEIGHTED_NORMAL':
                props = ['weight', 'keep_sharp', 'mode']
            elif pm.type == 'WELD':
                props = ['merge_threshold']
            elif pm.type == 'DECIMATE' and pm.decimate_type == 'DISSOLVE':
                props = ['decimate_type', 'angle_limit']
            else:
                continue
                
            for prop in props:
                if hasattr(pm, prop):
                    setattr(cm, prop, getattr(pm, prop))
        
        # Setup normal transfer
        if "SeamVerts" not in child_obj.vertex_groups:
            seam_group = child_obj.vertex_groups.new(name="SeamVerts")
            threshold = 0.02
            
            # Use object space for more accurate calculations
            parent_matrix_inv = parent_obj.matrix_world.inverted()
            child_matrix = child_obj.matrix_world
            
            for v_idx, vert in enumerate(child_obj.data.vertices):
                world_pos = child_matrix @ vert.co
                local_pos = parent_matrix_inv @ world_pos
                
                result = parent_obj.closest_point_on_mesh(local_pos)
                if result[0]:  # If found closest point
                    dist = (world_pos - (parent_obj.matrix_world @ result[1])).length
                    if dist < threshold:
                        weight = 1.0 - (dist / threshold)
                        if weight > 0:
                            seam_group.add([v_idx], weight, 'REPLACE')
        
        if 'NormalTransfer' not in child_obj.modifiers:
            mod = child_obj.modifiers.new(name='NormalTransfer', type='DATA_TRANSFER')
            mod.object = parent_obj
            mod.use_loop_data = True
            mod.data_types_loops = {'CUSTOM_NORMAL'}
            mod.loop_mapping = 'NEAREST_POLYNOR'
            mod.mix_mode = 'REPLACE'
            mod.vertex_group = "SeamVerts"
        
        # Process nested children
        for nested_child in [obj for obj in bpy.data.objects 
                           if obj.parent == child_obj and obj.type == 'MESH']:
            self.process_child_hierarchy(parent_obj, nested_child)
    
    def execute(self, context):
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_objects:
            self.report({'ERROR'}, "No mesh objects selected")
            return {'CANCELLED'}
        
        # Process each selected mesh
        for obj in selected_objects:
            self.beautify_mesh(obj, context)
        
        # Process hierarchies
        parent_objects = [obj for obj in selected_objects if obj.parent is None]
        for parent in parent_objects:
            for child in [obj for obj in bpy.data.objects 
                         if obj.parent == parent and obj.type == 'MESH']:
                self.process_child_hierarchy(parent, child)
        
        # Restore selection
        for obj in selected_objects:
            obj.select_set(True)
            
        self.report({'INFO'}, f"Optimized {len(selected_objects)} mesh objects")
        return {'FINISHED'}

classes = (OBJECT_OT_beautify_mesh,) 