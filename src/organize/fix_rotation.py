import bpy
from bpy.types import Operator
import bmesh
from mathutils import Vector, Matrix, Quaternion

class ORG_FIXROTATION_OT_operator(bpy.types.Operator):
    bl_label = "Orient Face to Bottom"
    bl_idname = "fix.rotation"
    bl_description = "Orients the object with selected face facing down"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (obj and obj.type == 'MESH' and 
                context.mode == 'EDIT_MESH' and 
                context.tool_settings.mesh_select_mode[2] and 
                context.edit_object.data.total_face_sel > 0)
    
    def execute(self, context):
        obj = context.active_object
        
        bm = bmesh.from_edit_mesh(obj.data)
        selected_faces = [f for f in bm.faces if f.select]
        
        if not selected_faces:
            self.report({'ERROR'}, "No faces selected")
            return {'CANCELLED'}
        
        if bm.faces.active and bm.faces.active.select:
            face_normal = bm.faces.active.normal.copy()
        else:
            face_normal = selected_faces[0].normal.copy()
        
        face_normal_world = obj.matrix_world.to_3x3() @ face_normal
        face_normal_world.normalize()
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        orig_loc = obj.location.copy()
        
        negative_z = Vector((0, 0, -1))
        
        rotation = negative_z.rotation_difference(face_normal_world)
        
        obj.rotation_mode = 'QUATERNION'
        obj.rotation_quaternion = rotation
        
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        obj.location = orig_loc
        
        self.report({'INFO'}, "Object oriented with face facing down")
        return {'FINISHED'}

classes = (ORG_FIXROTATION_OT_operator,) 