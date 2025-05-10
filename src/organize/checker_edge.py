import bpy
import bmesh
from mathutils import Vector
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
        initial_selected = [e for e in bm.edges if e.select]
        if not initial_selected: return {'CANCELLED'}
        
        initial_selected.sort(key=lambda e: e.index)
        
        edges_to_keep = []
        for i, edge in enumerate(initial_selected):
            if i % 2 == 1:  # Store odd-indexed edges (the ones we deselect)
                v1 = edge.verts[0].co
                v2 = edge.verts[1].co
                direction = (v2 - v1).normalized()
                edges_to_keep.append((tuple(v1), tuple(v2), tuple(direction)))
        
        for i, edge in enumerate(initial_selected): edge.select = i % 2 == 0
        bmesh.update_edit_mesh(obj.data)
        
        if self.dissolve:
            bpy.ops.mesh.dissolve_edges()
            
            bm = bmesh.from_edit_mesh(obj.data)
            bpy.ops.mesh.select_all(action='DESELECT')
            
            for edge in bm.edges:
                v1 = edge.verts[0].co
                v2 = edge.verts[1].co
                current_dir = (v2 - v1).normalized()
                
                for orig_v1, orig_v2, orig_dir in edges_to_keep:
                    alignment = abs(current_dir.dot(Vector(orig_dir)))
                    if alignment > 0.9:  # Threshold for "parallel enough"
                        v1_orig = Vector(orig_v1)
                        v2_orig = Vector(orig_v2)
                        dist1 = min((v1_orig - v1).length, (v1_orig - v2).length)
                        dist2 = min((v2_orig - v1).length, (v2_orig - v2).length)
                        if dist1 < 0.001 or dist2 < 0.001:
                            edge.select = True
                            break
            
            bmesh.update_edit_mesh(obj.data)
        
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "dissolve")

classes = (CHECKER_EDGE_OT_operator,)