import bpy
from bpy.types import Operator


class SELECT_MAT_OT_operator(bpy.types.Operator):
    bl_label = "Similar Material"
    bl_idname = "organize.selectmaterial"
    bl_description = "Select faces with similar material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.mesh.select_similar(type='FACE_MATERIAL')
        return {"FINISHED"}

class SELECT_PER_OT_operator(bpy.types.Operator):
    bl_label = "Similar Perimeter"
    bl_idname = "organize.selectperimeter"
    bl_description = "Select faces with similar perimeter"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.mesh.select_similar(type='FACE_PERIMETER')
        return {"FINISHED"}


classes = (
    SELECT_MAT_OT_operator, 
    SELECT_PER_OT_operator,
) 