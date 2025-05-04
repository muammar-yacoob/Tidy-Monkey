import bpy
from bpy.types import Operator

class APPLY_MODS_OT_operator(bpy.types.Operator):
    bl_label = "Apply Modifiers"
    bl_idname = "apply.mods"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        sel_objs = [obj for obj in context.selected_objects if obj.type == 'MESH']
        for obj in sel_objs:
            bpy.ops.object.convert(target='MESH')
        
        self.report({'INFO'}, f"Mods applied to {len(sel_objs)} Objects")
        return {"FINISHED"}

classes = (APPLY_MODS_OT_operator,) 