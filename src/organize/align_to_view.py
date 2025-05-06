import bpy
from bpy.types import Operator
import mathutils

class ORG_ALIGNTOVIEW_OT_operator(bpy.types.Operator):
    bl_label = "Align to View"
    bl_idname = "organize.aligntoview"
    bl_description = "Aligns current object to match view rotation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.object is None:
            return {'CANCELLED'}
            
        orig_mode = context.object.rotation_mode
        
        context.object.rotation_mode = 'QUATERNION'
        context.object.rotation_quaternion = context.region_data.view_rotation
        
        context.object.rotation_mode = orig_mode
        
        return {"FINISHED"}

classes = (ORG_ALIGNTOVIEW_OT_operator,) 