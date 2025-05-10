import bpy
import bmesh
from bpy.types import Operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class SELECT_SIMILAR_VERTS_OT_operator(bpy.types.Operator):
    bl_label = "Clean Vertices"
    bl_idname = "cleanup.selectsimilarverts"
    bl_description = "Dissolve vertices with 2 edge connections"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            object = bpy.context.active_object
            if not object or object.type != 'MESH' or object.mode != 'EDIT':
                self.report({'ERROR'}, 'Must be in Edit Mode with a mesh object')
                return {'CANCELLED'}
                
            bm = bmesh.from_edit_mesh(object.data)
            
            # Find and dissolve vertices with 2 edges
            verts_to_dissolve = []
            for v in bm.verts:
                if len(v.link_edges) == 2:
                    verts_to_dissolve.append(v)
            
            # Dissolve the vertices
            if verts_to_dissolve:
                bmesh.ops.dissolve_verts(bm, verts=verts_to_dissolve)
            
            bmesh.update_edit_mesh(object.data)
            self.report({'INFO'}, f'Dissolved {len(verts_to_dissolve)} vertices with 2 edge connections')
            
        except Exception as e:
            self.report({'ERROR'}, f'Error: {str(e)}')
            
        return {"FINISHED"}

classes = (SELECT_SIMILAR_VERTS_OT_operator,) 