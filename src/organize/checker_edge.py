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
              
        # Start in edit mode with BMesh
        bm = bmesh.from_edit_mesh(obj.data)
        initial_selected = [e for e in bm.edges if e.select]
        if not initial_selected: return {'CANCELLED'}
        
        # Sort edges for consistent results
        initial_selected.sort(key=lambda e: e.index)
        
        # Store vertices of alternating edges to keep
        verts_to_keep = set()
        for i, edge in enumerate(initial_selected):
            if i % 2 == 1:  # Store odd-indexed edges (the ones we deselect)
                v1 = tuple(round(float(c), 4) for c in edge.verts[0].co)
                v2 = tuple(round(float(c), 4) for c in edge.verts[1].co)
                verts_to_keep.add(v1)
                verts_to_keep.add(v2)
        
        # Apply checker pattern
        for i, edge in enumerate(initial_selected):
            edge.select = i % 2 == 0  # Keep even-indexed edges selected
        
        # Update the mesh
        bmesh.update_edit_mesh(obj.data)
        
        if self.dissolve:
            # Dissolve selected edges
            bpy.ops.mesh.dissolve_edges()
            
            # Get fresh BMesh after topology change
            bm = bmesh.from_edit_mesh(obj.data)
            
            # First deselect all
            bpy.ops.mesh.select_all(action='DESELECT')
            
            # Select edges where both vertices were in our original deselected edges
            for edge in bm.edges:
                v1 = tuple(round(float(c), 4) for c in edge.verts[0].co)
                v2 = tuple(round(float(c), 4) for c in edge.verts[1].co)
                if v1 in verts_to_keep and v2 in verts_to_keep:
                    edge.select = True
            
            # Update the mesh
            bmesh.update_edit_mesh(obj.data)
        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "dissolve")

classes = (CHECKER_EDGE_OT_operator,)