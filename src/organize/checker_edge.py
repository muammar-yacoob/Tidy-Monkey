import bpy
import bmesh
from bpy.types import Operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class CHECKER_EDGE_OT_operator(bpy.types.Operator):
    bl_label = "Checker Edge Select"
    bl_idname = "organize.checkeredge"
    bl_description = "Deselect every other edge in the current selection"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        obj = context.edit_object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Must be in Edit Mode with a mesh object")
            return {'CANCELLED'}
            
        bm = bmesh.from_edit_mesh(obj.data)
        
        selected_edges = [e for e in bm.edges if e.select]
        
        if not selected_edges:
            self.report({'ERROR'}, "No edges selected")
            return {'CANCELLED'}
            
        selected_edges.sort(key=lambda e: e.index)
        
        for i in range(len(selected_edges)):
            if i % 2 == 1:  # Deselect odd positions (every other one)
                selected_edges[i].select = False
        
        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}

classes = (CHECKER_EDGE_OT_operator,)