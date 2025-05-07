import bpy
import bmesh
from bpy.types import Operator


class SELECT_MAT_OT_operator(bpy.types.Operator):
    bl_label = "Similar Material"
    bl_idname = "organize.selectmaterial"
    bl_description = "Select faces with similar material"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.mesh.select_similar(type='FACE_MATERIAL')
        return {"FINISHED"}

class SELECT_PER_OT_operator(bpy.types.Operator):
    bl_label = "Similar Perimeter"
    bl_idname = "organize.selectperimeter"
    bl_description = "Select faces with similar perimeter"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if not (obj and obj.type == 'MESH' and context.mode == 'EDIT_MESH'):
            return False
            
        if not context.tool_settings.mesh_select_mode[2]:  # Face select mode
            return False
            
        bm = bmesh.from_edit_mesh(obj.data)
        selected_faces = [f for f in bm.faces if f.select]
        return len(selected_faces) == 1
    
    def execute(self, context):
        bpy.ops.mesh.select_similar(type='FACE_PERIMETER')
        return {"FINISHED"}

class SELECT_UV_OT_operator(bpy.types.Operator):
    bl_label = "Similar UV"
    bl_idname = "organize.selectuv"
    bl_description = "Select faces with similar UV layout"
    bl_options = {'REGISTER', 'UNDO'}
    
    threshold: bpy.props.FloatProperty(
        name="Threshold",
        description="Threshold for UV similarity",
        default=0.1,
        min=0.001,
        max=1.0,
        precision=3
    )
    
    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if not (obj and obj.type == 'MESH' and context.mode == 'EDIT_MESH'):
            return False
            
        if not context.tool_settings.mesh_select_mode[2]:  # Face select mode
            return False
            
        bm = bmesh.from_edit_mesh(obj.data)
        selected_faces = [f for f in bm.faces if f.select]
        return len(selected_faces) == 1
    
    def execute(self, context):
        obj = context.edit_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        
        # Ensure we have UV layers
        if not me.uv_layers.active:
            self.report({'WARNING'}, "No active UV layer found")
            return {'CANCELLED'}
        
        # Get selected face
        selected_face = None
        for f in bm.faces:
            if f.select:
                selected_face = f
                break
        
        if not selected_face:
            return {'CANCELLED'}
        
        # Get UV loop layer
        uv_layer = bm.loops.layers.uv.active
        
        # Calculate average UV coordinates for the selected face
        selected_uvs = [l[uv_layer].uv for l in selected_face.loops]
        selected_uv_x = sum(uv.x for uv in selected_uvs) / len(selected_uvs)
        selected_uv_y = sum(uv.y for uv in selected_uvs) / len(selected_uvs)
        
        # Deselect all faces first
        for f in bm.faces:
            f.select = False
        
        # Re-select the originally selected face
        selected_face.select = True
        
        # Select faces with similar UV coordinates
        for f in bm.faces:
            if f != selected_face:
                face_uvs = [l[uv_layer].uv for l in f.loops]
                if len(face_uvs) == len(selected_uvs):  # Same number of vertices
                    avg_uv_x = sum(uv.x for uv in face_uvs) / len(face_uvs)
                    avg_uv_y = sum(uv.y for uv in face_uvs) / len(face_uvs)
                    
                    # Check if UVs are similar (within threshold)
                    if (abs(avg_uv_x - selected_uv_x) < self.threshold and 
                        abs(avg_uv_y - selected_uv_y) < self.threshold):
                        f.select = True
        
        # Update the mesh
        bmesh.update_edit_mesh(me)
        return {'FINISHED'}


classes = (
    SELECT_MAT_OT_operator, 
    SELECT_PER_OT_operator,
    SELECT_UV_OT_operator,
) 