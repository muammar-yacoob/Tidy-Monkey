import bpy
from bpy.types import Operator

class ORG_SELECTED_OT_operator(bpy.types.Operator):
    bl_label = "Origin to Selected"
    bl_idname = "origin.toselected"
    bl_description = "Sets object origin to selection"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}

classes = (ORG_SELECTED_OT_operator,) 