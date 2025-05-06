import bpy
from bpy.types import Operator

class CLEAR_MATS_OT_operator(bpy.types.Operator):
    bl_label = "Clear Unused Materials"
    bl_idname = "cleanup.clearmats"
    bl_description = "Clears unused materials"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        sel_objs = [obj for obj in context.selected_objects if obj.type == 'MESH']
        for obj in sel_objs:
            bpy.ops.object.material_slot_remove_unused()
        
        self.report({'INFO'}, f"Unused Materials were removed from {len(sel_objs)} Objects")
        return {"FINISHED"}

classes = (CLEAR_MATS_OT_operator,) 