import bpy
import bmesh
from bpy.types import Operator

class SELECT_SIMILAR_VERTS_OT_operator(bpy.types.Operator):
    bl_label = "Select Similar Vertices"
    bl_idname = "cleanup.selectsimilarverts"
    bl_description = "Select all vertices with the same number of edge connections"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            object = bpy.context.active_object
            if not object or object.type != 'MESH' or object.mode != 'EDIT':
                self.report({'ERROR'}, 'Must be in Edit Mode with a mesh object')
                return {'CANCELLED'}
                
            bm = bmesh.from_edit_mesh(object.data)
            
            selected_verts = [v for v in bm.verts if v.select]
            if not selected_verts:
                self.report({'ERROR'}, 'No vertices selected')
                return {'CANCELLED'}
                
            edge_count = len(selected_verts[0].link_edges)
            
            for v in bm.verts:
                if len(v.link_edges) == edge_count:
                    v.select = True
            
            bmesh.update_edit_mesh(object.data)
            self.report({'INFO'}, f'Selected vertices with {edge_count} edge connections')
            
        except Exception as e:
            self.report({'ERROR'}, f'Error: {str(e)}')
            
        return {"FINISHED"}

classes = (SELECT_SIMILAR_VERTS_OT_operator,) 