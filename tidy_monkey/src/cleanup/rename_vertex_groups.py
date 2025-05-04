import bpy
from bpy.types import Operator

class REN_VERT_OT_operator(bpy.types.Operator):
    bl_label = "Rename Mixamo Vert Groups"
    bl_idname = "renamevertgroups.rename"
    bl_description = "Removes the word Mixamo from all vertex groups"
    bl_options = {'REGISTER', 'UNDO'}
    
    text_input: bpy.props.StringProperty(name="Text Input")
    
    def execute(self, context):
        return {"FINISHED"}

classes = (REN_VERT_OT_operator,) 