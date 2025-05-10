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
            bpy.ops.mesh.remove_doubles()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.delete_loose()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.tris_convert_to_quads()

            bpy.ops.cleanup.cleanverts()
            
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            bpy.ops.object.shade_smooth()
            bpy.ops.object.shade_auto_smooth(angle=math.radians(40))
            
            if 'Weld' not in obj.modifiers:
                weld_mod = obj.modifiers.new(name='Weld', type='WELD')
                weld_mod.merge_threshold = 0.0001
        
        # Process parent objects and their child hierarchies
        parent_objects = [obj for obj in selected_objects if obj.parent is None]
        
        def process_child_hierarchy(parent_obj, child_obj):
            """Recursively process a child object and its children"""
            context.view_layer.objects.active = child_obj
            
            if child_obj.type == 'MESH':
                # Add data transfer modifier if it doesn't exist
                if 'NormalTransfer' not in child_obj.modifiers:
                    transfer_mod = child_obj.modifiers.new(name='NormalTransfer', type='DATA_TRANSFER')
                    transfer_mod.object = parent_obj
                    transfer_mod.use_loop_data = True
                    transfer_mod.data_types_loops = {'CUSTOM_NORMAL'}
                    transfer_mod.loop_mapping = 'NEAREST_POLYNOR'
                    transfer_mod.mix_mode = 'REPLACE'
                    
                # Move modifier to the top
                while child_obj.modifiers[0].name != 'NormalTransfer':
                    bpy.ops.object.modifier_move_up(modifier='NormalTransfer')
            
            # Process child objects of this child (nested hierarchy)
            for nested_child in bpy.data.objects:
                if nested_child.parent == child_obj and nested_child.type == 'MESH':
                    process_child_hierarchy(parent_obj, nested_child)
        
        for parent in parent_objects:
            # Direct children
            for child in [obj for obj in bpy.data.objects if obj.parent == parent and obj.type == 'MESH']:
                process_child_hierarchy(parent, child)
        
        # Reselect all objects
        for obj in selected_objects:
            obj.select_set(True)
            
        self.report({'INFO'}, f"Fixed mesh and normals on {len(selected_objects)} objects")
        return {"FINISHED"}

classes = (BEAUTIFY_OT_operator,) 