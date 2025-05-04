import bpy
import bmesh
from bpy.types import Operator

class CHECKER_EDGE_OT_operator(bpy.types.Operator):
    bl_label = "Checker Edge"
    bl_idname = "checker.edge"
    bl_description = "Checker Select Edges"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.active_object.mode != 'EDIT':
            self.report({'ERROR'}, "Must be in Edit Mode")
            return {'CANCELLED'}
            
        obj = context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        
        for i, edge in enumerate(bm.edges):
            if i % 2 == 0:
                edge.select = True
                
        bmesh.update_edit_mesh(me)
        return {"FINISHED"}

classes = (CHECKER_EDGE_OT_operator,) 