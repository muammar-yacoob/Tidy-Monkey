import bpy
import bmesh
from bpy.types import Operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class CHECKER_EDGE_OT_operator(bpy.types.Operator):
    bl_label = "Checker Edge Select"
    bl_idname = "organize.checkeredge"
    bl_description = "Deselect every other edge in the current selection"
    bl_options = {'REGISTER', 'UNDO'}
    
    dissolve: bpy.props.BoolProperty(name="Dissolve Edges", description="Dissolve selected edges", default=True) # type: ignore
    
    @classmethod
    def poll(cls, context): return context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        obj = context.edit_object
        if not obj or obj.type != 'MESH': return {'CANCELLED'}
            
        bm = bmesh.from_edit_mesh(obj.data)
        edges = [e for e in bm.edges if e.select]
        
        if not edges: return {'CANCELLED'}
        
        edges.sort(key=lambda e: e.index)
        
        for i, e in enumerate(edges): e.select = i % 2 == 0
        
        if self.dissolve: bpy.ops.mesh.dissolve_edges()
        
        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "dissolve")

classes = (CHECKER_EDGE_OT_operator,)