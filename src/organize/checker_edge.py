import bpy
import bmesh
from bpy.types import Operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class CHECKER_EDGE_OT_operator(bpy.types.Operator):
    bl_label = "Checker Edge Select"
    bl_idname = "organize.checkeredge"
    bl_description = "Deselect every other edge in the current selection"
    bl_options = {'REGISTER', 'UNDO'}
    
    dissolve: bpy.props.BoolProperty(
        name="Dissolve Edges",
        description="Dissolve selected edges after operation",
        default=False
    )
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        obj = context.edit_object
        if not obj or obj.type != 'MESH':
            return {'CANCELLED'}
            
        bm = bmesh.from_edit_mesh(obj.data)
        selected_edges = [e for e in bm.edges if e.select]
        
        if not selected_edges:
            return {'CANCELLED'}
        
        selected_edges.sort(key=lambda e: e.index)
        
        # Simple approach: just deselect odd-indexed edges
        for i, edge in enumerate(selected_edges): 
            if i % 2 == 1:
                edge.select = False
        
        if self.dissolve:
            # Store vertex coordinates of endpoints for even-indexed edges
            kept_verts = set()
            for i, edge in enumerate(selected_edges):
                if i % 2 == 0:  # These are the edges we're keeping
                    v1 = tuple(round(c, 4) for c in edge.verts[0].co)
                    v2 = tuple(round(c, 4) for c in edge.verts[1].co)
                    kept_verts.add(v1)
                    kept_verts.add(v2)
            
            # Dissolve selected edges
            bpy.ops.mesh.dissolve_edges()
            
            # Clear selection
            bpy.ops.mesh.select_all(action='DESELECT')
            
            # Get updated bmesh
            bm = bmesh.from_edit_mesh(obj.data)
            
            # Only select edges that have both vertices in our kept set
            for edge in bm.edges:
                v1 = tuple(round(c, 4) for c in edge.verts[0].co)
                v2 = tuple(round(c, 4) for c in edge.verts[1].co)
                if v1 in kept_verts and v2 in kept_verts:
                    edge.select = True
        
        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "dissolve")

classes = (CHECKER_EDGE_OT_operator,)