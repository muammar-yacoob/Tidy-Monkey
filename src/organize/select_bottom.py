import bpy
import bmesh
from mathutils import Vector
from bpy.types import Operator

class BUTTS_OT_operator(bpy.types.Operator):
    bl_label = "Select Bottom"
    bl_idname = "organize.selectbottom"
    bl_description = "Selects lower most vertices"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.active_object.mode != 'EDIT':
            self.report({'ERROR'}, "Must be in Edit Mode")
            return {'CANCELLED'}
            
        obj = context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')
        bpy.ops.mesh.select_all(action='DESELECT')
        
        # Find lowest Z coordinate in global space
        lowest_z = float('inf')
        for vert in bm.verts:
            global_co = obj.matrix_world @ vert.co
            if global_co.z < lowest_z:
                lowest_z = global_co.z
                
        # Select all vertices at lowest Z (within a small threshold)
        threshold = 0.001
        for vert in bm.verts:
            global_co = obj.matrix_world @ vert.co
            if abs(global_co.z - lowest_z) < threshold:
                vert.select = True
                
        bmesh.update_edit_mesh(me)
        return {"FINISHED"}

classes = (BUTTS_OT_operator,) 