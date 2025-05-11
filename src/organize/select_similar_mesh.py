import bpy
from bpy.types import Operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class SELECT_SAME_OT_operator(bpy.types.Operator):
    bl_label = "Select Similar Mesh"
    bl_idname = "organize.selectsimilarmesh"
    bl_description = "Selects objects with same vertex count and name"
    bl_options = {'REGISTER', 'UNDO'}
        
    similar: bpy.props.StringProperty(name="Similar:", options={'HIDDEN'})
    
    def execute(self, context):
        if context.mode != 'OBJECT':
            self.report({'ERROR'}, "Must be in Object Mode")
            return {'CANCELLED'}
            
        active_obj = context.active_object
        if not active_obj or active_obj.type != 'MESH':
            self.report({'ERROR'}, "Active object must be a mesh")
            return {'CANCELLED'}
            
        active_verts = len(active_obj.data.vertices)
        active_base_name = active_obj.name.split('.')[0]
        
        count = 0
        for obj in context.visible_objects:
            if obj != active_obj and obj.type == 'MESH':
                obj_base_name = obj.name.split('.')[0]
                verts = len(obj.data.vertices)
                
                if (verts == active_verts) and (obj_base_name == active_base_name):
                    obj.select_set(True)
                    count += 1
        
        self.report({'INFO'}, f"Selected {count} similar meshes")
        return {"FINISHED"}

classes = (SELECT_SAME_OT_operator,) 