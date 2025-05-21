import bpy
from bpy.types import Operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class SELECT_SAME_OT_operator(bpy.types.Operator):
    bl_label = "Select Similar Mesh"
    bl_idname = "organize.selectsimilarmesh"
    bl_description = "Selects objects with same vertex count and name"
    bl_options = {'REGISTER', 'UNDO'}
        
    similar: bpy.props.StringProperty(name="Similar:", options={'HIDDEN'})
    
    def get_name_variants(self, name):
        # Try different name patterns in order of priority
        variants = [
            name.split('.')[0],  # First try splitting by dot
            name.split(' ')[0],  # Then try splitting by space
            name                 # Finally use the full name
        ]
        return list(set(variants))  # Remove duplicates
    
    def execute(self, context):
        if context.mode != 'OBJECT':
            self.report({'ERROR'}, "Must be in Object Mode")
            return {'CANCELLED'}
            
        active_obj = context.active_object
        if not active_obj or active_obj.type != 'MESH':
            self.report({'ERROR'}, "Active object must be a mesh")
            return {'CANCELLED'}
            
        active_verts = len(active_obj.data.vertices)
        active_name_variants = self.get_name_variants(active_obj.name)
        
        count = 0
        # First find objects with matching vertex count
        for obj in context.visible_objects:
            if obj != active_obj and obj.type == 'MESH':
                if len(obj.data.vertices) == active_verts:
                    # Then check if any name variant matches
                    obj_name_variants = self.get_name_variants(obj.name)
                    if any(active_name in obj_name_variants for active_name in active_name_variants):
                        obj.select_set(True)
                        count += 1
        
        self.report({'INFO'}, f"Selected {count} similar meshes")
        return {"FINISHED"}

classes = (SELECT_SAME_OT_operator,) 