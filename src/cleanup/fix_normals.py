import bpy
import math
from bpy.types import Operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class FIX_NORMALS_OT_operator(bpy.types.Operator):
    bl_label = "Fix Mesh & Normals"
    bl_idname = "cleanup.fixnormals"
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


            
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            bpy.ops.object.shade_smooth()
            bpy.ops.object.shade_auto_smooth(angle=math.radians(40))
            
            if 'Weld' not in obj.modifiers:
                weld_mod = obj.modifiers.new(name='Weld', type='WELD')
                weld_mod.merge_threshold = 0.0001
        
        parent_objects = [obj for obj in selected_objects if obj.parent is None]
        
        for parent in parent_objects:
            child_objects = [obj for obj in selected_objects if obj.parent == parent]
            
            if not child_objects:
                continue
                
            for child in child_objects:
                context.view_layer.objects.active = child
                
                if 'NormalTransfer' not in child.modifiers:
                    transfer_mod = child.modifiers.new(name='NormalTransfer', type='DATA_TRANSFER')
                    transfer_mod.object = parent
                    transfer_mod.use_loop_data = True
                    transfer_mod.data_types_loops = {'CUSTOM_NORMAL'}
                    transfer_mod.loop_mapping = 'NEAREST_POLYNOR'
                
                while child.modifiers[0].name != 'NormalTransfer':
                    bpy.ops.object.modifier_move_up(modifier='NormalTransfer')
        
        for obj in selected_objects:
            obj.select_set(True)
            
        self.report({'INFO'}, f"Fixed mesh and normals on {len(selected_objects)} objects")
        return {"FINISHED"}

classes = (FIX_NORMALS_OT_operator,) 