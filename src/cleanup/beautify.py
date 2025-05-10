import bpy
import math
from bpy.types import Operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class BEAUTIFY_OT_operator(bpy.types.Operator):
    bl_label = "Beautify"
    bl_idname = "cleanup.beautify"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        
        if not selected_objects:
            self.report({'ERROR'}, "No mesh objects selected")
            return {"CANCELLED"}
        
        for obj in selected_objects:
            context.view_layer.objects.active = obj
            
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')

            # Make Normals Consistent
            bpy.ops.mesh.normals_make_consistent(inside=False)

            # Cleanup Mesh
            bpy.ops.mesh.select_all(action='SELECT')
            # bpy.ops.mesh.remove_doubles()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.delete_loose()
            bpy.ops.mesh.select_all(action='SELECT')
            
            bpy.ops.cleanup.cleanverts()
            
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.tris_convert_to_quads(face_threshold=40, shape_threshold=math.radians(180))
            
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            bpy.ops.object.shade_smooth()
            bpy.ops.object.shade_auto_smooth(angle=math.radians(40))
            
            if 'Bevel' not in obj.modifiers:
                bevel_mod = obj.modifiers.new(name='Bevel', type='BEVEL')
                bevel_mod.width = 0.01
                bevel_mod.segments = 2
                bevel_mod.limit_method = 'ANGLE'
                bevel_mod.angle_limit = math.radians(40)
                bevel_mod.harden_normals = True
                bevel_mod.miter_outer = 'MITER_ARC'
            
            if 'WeightedNormal' not in obj.modifiers:
                weighted_mod = obj.modifiers.new(name='WeightedNormal', type='WEIGHTED_NORMAL')
                weighted_mod.weight = 100
                weighted_mod.keep_sharp = True
                weighted_mod.mode = 'FACE_AREA_WITH_ANGLE'
            
            if 'Weld' not in obj.modifiers:
                weld_mod = obj.modifiers.new(name='Weld', type='WELD')
                weld_mod.merge_threshold = 0.0001
        
        parent_objects = [obj for obj in selected_objects if obj.parent is None]
        
        def process_child_hierarchy(parent_obj, child_obj):
            context.view_layer.objects.active = child_obj
            
            if child_obj.type == 'MESH':
                # Create vertex group for seam vertices
                if "SeamVerts" not in child_obj.vertex_groups:
                    seam_group = child_obj.vertex_groups.new(name="SeamVerts")
                    threshold = 0.02
                    
                    # Select vertices near parent
                    for v_idx, vert in enumerate(child_obj.data.vertices):
                        world_pos = child_obj.matrix_world @ vert.co
                        closest = parent_obj.closest_point_on_mesh(parent_obj.matrix_world.inverted() @ world_pos)
                        
                        if closest[0]:
                            dist = (world_pos - (parent_obj.matrix_world @ closest[1])).length
                            if dist < threshold:
                                weight = 1.0 - (dist / threshold)
                                if weight > 0: seam_group.add([v_idx], weight, 'REPLACE')
                
                # Add normal transfer modifier
                if 'NormalTransfer' not in child_obj.modifiers:
                    mod = child_obj.modifiers.new(name='NormalTransfer', type='DATA_TRANSFER')
                    mod.object = parent_obj
                    mod.use_loop_data = True
                    mod.data_types_loops = {'CUSTOM_NORMAL'}
                    mod.loop_mapping = 'NEAREST_POLYNOR'
                    mod.mix_mode = 'REPLACE'
                    mod.vertex_group = "SeamVerts"
                    
                    # Move to top
                    while child_obj.modifiers[0].name != 'NormalTransfer':
                        bpy.ops.object.modifier_move_up(modifier='NormalTransfer')
            
            # Process nested children
            for nested_child in [obj for obj in bpy.data.objects if obj.parent == child_obj and obj.type == 'MESH']:
                process_child_hierarchy(parent_obj, nested_child)
        
        # Process children of parent objects
        for parent in parent_objects:
            for child in [obj for obj in bpy.data.objects if obj.parent == parent and obj.type == 'MESH']:
                process_child_hierarchy(parent, child)
        
        # Reselect objects
        for obj in selected_objects:
            obj.select_set(True)
            
        self.report({'INFO'}, f"Fixed mesh and normals on {len(selected_objects)} objects")
        return {"FINISHED"}

classes = (BEAUTIFY_OT_operator,) 