import bpy
from bpy.types import Operator

class SELECT_SIMILAR_OT_operator(bpy.types.Operator):
    bl_label = "Similar Selection"
    bl_idname = "similar.select"
    bl_description = "Select Similar Faces"
    bl_options = {'REGISTER', 'UNDO'}
    
    select_type: bpy.props.StringProperty(default='MATERIAL', options={'HIDDEN'})
    
    @classmethod
    def description(cls, context, properties):
        types = {
            'MATERIAL': 'Select faces with similar material',
            'PERIMETER': 'Select faces with similar perimeter',
            'NORMAL': 'Select faces with similar normal direction',
            'AREA': 'Select faces with similar area',
            'COPLANAR': 'Select coplanar faces'
        }
        return types.get(properties.select_type, cls.bl_description)
    
    def execute(self, context):
        try:
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
            bpy.ops.mesh.select_similar(type=self.select_type, threshold=0.01)
        except:
            bpy.ops.mesh.select_mode(type='FACE')
            self.report({'ERROR'}, "Select a face first")
        return {"FINISHED"}

class SELECT_MAT_OT_operator(bpy.types.Operator):
    bl_label = "Similar Material"
    bl_idname = "material.select"
    bl_description = "Select faces with similar material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.similar.select(select_type='MATERIAL')
        return {"FINISHED"}

class SELECT_PER_OT_operator(bpy.types.Operator):
    bl_label = "Similar Perimeter"
    bl_idname = "perimeter.select"
    bl_description = "Select faces with similar perimeter"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.similar.select(select_type='PERIMETER')
        return {"FINISHED"}

class SELECT_NORM_OT_operator(bpy.types.Operator):
    bl_label = "Similar Normal"
    bl_idname = "normal.select"
    bl_description = "Select faces with similar normal direction"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.similar.select(select_type='NORMAL')
        return {"FINISHED"}

class SELECT_AREA_OT_operator(bpy.types.Operator):
    bl_label = "Similar Area"
    bl_idname = "area.select"
    bl_description = "Select faces with similar area"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.similar.select(select_type='AREA')
        return {"FINISHED"}

class SELECT_COPLANAR_OT_operator(bpy.types.Operator):
    bl_label = "Similar Coplanar"
    bl_idname = "coplanar.select"
    bl_description = "Select coplanar faces"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.similar.select(select_type='COPLANAR')
        return {"FINISHED"}

classes = (
    SELECT_SIMILAR_OT_operator, 
    SELECT_MAT_OT_operator, 
    SELECT_PER_OT_operator,
    SELECT_NORM_OT_operator,
    SELECT_AREA_OT_operator,
    SELECT_COPLANAR_OT_operator
) 