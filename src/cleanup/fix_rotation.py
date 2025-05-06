import bpy
from bpy.types import Operator
import bmesh
from mathutils import Vector

class FIXROTATION_OT_operator(bpy.types.Operator):
    bl_label = "Orient Face to Bottom"
    bl_idname = "cleanup.fixrotation"
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
        
        face = bm.faces.active if bm.faces.active and bm.faces.active.select else selected_faces[0]
        face_normal = face.normal.copy()
        
        bmesh.update_edit_mesh(obj.data)
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        orig_loc = obj.location.copy()
        
        face_normal_world = obj.matrix_world.to_3x3() @ face_normal
        face_normal_world.normalize()
        
        target_axis = Vector((0, 0, -1))
        rotation = face_normal_world.rotation_difference(target_axis)
        
        obj.rotation_mode = 'QUATERNION'
        obj.rotation_quaternion = rotation
        
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        obj.location = orig_loc
        
        self.report({'INFO'}, "Object oriented with face facing down")
        return {'FINISHED'}

classes = (FIXROTATION_OT_operator,) 