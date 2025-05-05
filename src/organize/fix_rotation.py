import bpy
from bpy.types import Operator
import bmesh

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
                context.tool_settings.mesh_select_mode[2] and  # Face select mode
                context.edit_object.data.total_face_sel > 0)   # At least one face selected
    
    def execute(self, context):
        # Get the active object and its mesh
        obj = context.active_object
        mesh = obj.data
        
        # Create a bmesh to access face data
        bm = bmesh.from_edit_mesh(mesh)
        
        # Get selected faces and calculate average normal
        selected_faces = [f for f in bm.faces if f.select]
        if not selected_faces:
            self.report({'ERROR'}, "No faces selected")
            return {'CANCELLED'}
        
        # Use the normal of the first selected face (or calculate average if needed)
        face_normal = selected_faces[0].normal.copy()
        face_normal.normalize()
        
        # Convert to world space
        face_normal = obj.matrix_world.to_3x3() @ face_normal
        
        # Switch to object mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Use a temporary object to do the alignment
        cursor_loc = context.scene.cursor.location.copy()
        cursor_rot = context.scene.cursor.rotation_euler.copy()
        
        # Set cursor to object's location
        context.scene.cursor.location = obj.location
        
        # Create an empty and align it to face normal (facing -Z direction)
        bpy.ops.object.empty_add(type='ARROWS', align='WORLD')
        empty = context.active_object
        
        # Align the empty so that its -Z axis points in the direction of the face normal
        empty.rotation_euler = face_normal.to_track_quat('Z', 'Y').to_euler()
        
        # Select the original object and make it active
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        context.view_layer.objects.active = obj
        
        # Parent the object to the empty
        bpy.ops.object.parent_set(type='OBJECT')
        
        # Clear the rotation of the empty (making selected face face down)
        empty.rotation_euler = (0, 0, 0)
        
        # Clear parent relationship while keeping transform
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        
        # Apply rotation to make it permanent
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
        
        # Delete the empty
        bpy.ops.object.select_all(action='DESELECT')
        empty.select_set(True)
        bpy.ops.object.delete()
        
        # Restore cursor position and rotation
        context.scene.cursor.location = cursor_loc
        context.scene.cursor.rotation_euler = cursor_rot
        
        # Return to object mode (we're already in object mode)
        self.report({'INFO'}, "Object oriented with face facing down")
        return {'FINISHED'}

classes = (ORG_FIXROTATION_OT_operator,) 