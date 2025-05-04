import bpy
from bpy.types import Operator

class ORG_ALIGNTOVIEW_OT_operator(bpy.types.Operator):
    bl_label = "Align to View"
    bl_idname = "align.toview"
    bl_description = "Aligns object to view"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        regData = context.region_data
        context.object.rotation_euler = regData.view_rotation.to_euler()
        return {"FINISHED"}

class ALIGN_OT_operator(bpy.types.Operator):
    bl_label = "Align Objects"
    bl_idname = "alignobjects.align"
    bl_description = "Aligns objects along a specific axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    algn: bpy.props.StringProperty(default='Z', options={'HIDDEN'})
    
    def execute(self, context):
        sel_objs = [obj for obj in context.selected_objects if obj.type == 'MESH']
        self.report({'INFO'}, f"Aligned at {self.algn} axis")
        bpy.ops.object.align(align_axis={self.algn})
        return {"FINISHED"}

classes = (ORG_ALIGNTOVIEW_OT_operator, ALIGN_OT_operator) 