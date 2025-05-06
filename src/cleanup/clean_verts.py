import bpy
import bmesh
from bpy.types import Operator

class CLEAN_VERTS_OT_operator(bpy.types.Operator):
    bl_label = "Dissolve Similar Verts"
    bl_idname = "cleanup.cleanverts"
    bl_description = "Dissolves Verts with similar connections"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            object = bpy.context.active_object
            bm = bmesh.from_edit_mesh(object.data)
            
            bpy.ops.mesh.select_similar(type='EDGE')
            bpy.ops.mesh.dissolve_verts()

            self.report({'INFO'}, 'Verts Dissolved')
        except:
            self.report({'ERROR'}, 'No Selected Vertices')
            
        return {"FINISHED"}

classes = (CLEAN_VERTS_OT_operator,) 