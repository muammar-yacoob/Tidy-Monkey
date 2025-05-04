import bpy
from bpy.types import Operator

class SELECT_SAME_OT_operator(bpy.types.Operator):
    bl_label = "Select Similar Mesh"
    bl_idname = "samemesh.similar"
    bl_description = "Selects objects with similar vertex count"
    bl_options = {'REGISTER', 'UNDO'}
        
    similar = bpy.props.StringProperty(name="Similar:", options={'HIDDEN'})
    
    def execute(self, context):
        if context.mode != 'OBJECT':
            self.report({'ERROR'}, "Must be in Object Mode")
            return {'CANCELLED'}
            
        active_obj = context.active_object
        if not active_obj or active_obj.type != 'MESH':
            self.report({'ERROR'}, "Active object must be a mesh")
            return {'CANCELLED'}
            
        active_verts = len(active_obj.data.vertices)
        threshold = 0.1  # 10% threshold
        min_verts = active_verts * (1 - threshold)
        max_verts = active_verts * (1 + threshold)
        
        count = 0
        for obj in context.visible_objects:
            if obj != active_obj and obj.type == 'MESH':
                verts = len(obj.data.vertices)
                if min_verts <= verts <= max_verts:
                    obj.select_set(True)
                    count += 1
        
        self.report({'INFO'}, f"Selected {count} similar meshes")
        return {"FINISHED"}

classes = (SELECT_SAME_OT_operator,) 