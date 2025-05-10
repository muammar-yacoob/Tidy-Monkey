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
            
        # Work in object mode for reliable edge access
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Get initially selected edges by index
        initial_edges = [i for i, e in enumerate(obj.data.edges) if e.select]
        if not initial_edges: return {'CANCELLED'}
        
        # Store all unselected edges to select later
        unselected_edges = [i for i, e in enumerate(obj.data.edges) if not e.select]
        
        # Deselect every other edge
        for i, idx in enumerate(initial_edges):
            obj.data.edges[idx].select = i % 2 == 0
            
        # Apply changes and dissolve
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(type='EDGE')
        
        # Deselected edges from initial selection - to select after dissolve
        odd_indices = [initial_edges[i] for i in range(len(initial_edges)) if i % 2 == 1]
        
        if self.dissolve: 
            bpy.ops.mesh.dissolve_edges()
            
            # Get back to object mode to select remaining edges
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Select odd-indexed edges from initial selection
            for idx in odd_indices:
                if idx < len(obj.data.edges):
                    obj.data.edges[idx].select = True
                    
            # Return to edit mode
            bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "dissolve")

classes = (CHECKER_EDGE_OT_operator,)