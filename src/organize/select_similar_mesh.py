import bpy
from bpy.types import Operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class SELECT_SAME_OT_operator(bpy.types.Operator):
    bl_label = "Select Similar Mesh"
    bl_idname = "organize.selectsimilarmesh"
    bl_description = "Selects objects with same vertex count and name"
    bl_options = {'REGISTER', 'UNDO'}
        
    similar: bpy.props.StringProperty(name="Similar:", options={'HIDDEN'})
    use_name: bpy.props.BoolProperty(
        name="Match Name",
        description="Include object name in similarity search",
        default=True
    )
    
    def get_base_name(self, name):
        # Get base name by splitting from the last separator
        dot_split = name.rsplit('.', 1)[0]
        space_split = name.rsplit(' ', 1)[0]
        
        # Return the shorter result (more likely to be the actual base name)
        # If they're the same length, prefer the dot split as it's more common in Blender
        if len(dot_split) <= len(space_split):
            return dot_split
        return space_split
    
    def execute(self, context):
        if context.mode != 'OBJECT':
            self.report({'ERROR'}, "Must be in Object Mode")
            return {'CANCELLED'}
            
        active_obj = context.active_object
        if not active_obj or active_obj.type != 'MESH':
            self.report({'ERROR'}, "Active object must be a mesh")
            return {'CANCELLED'}
            
        # Deselect all objects first
        bpy.ops.object.select_all(action='DESELECT')
        
        active_verts = len(active_obj.data.vertices)
        active_base_name = self.get_base_name(active_obj.name) if self.use_name else None
        
        matched_objects = []  # Keep track of matched objects
        
        for obj in context.visible_objects:
            if obj != active_obj and obj.type == 'MESH':
                # Check vertex count first
                if len(obj.data.vertices) == active_verts:
                    if not self.use_name:
                        matched_objects.append(obj)
                    else:
                        # Compare base names
                        obj_base_name = self.get_base_name(obj.name)
                        if obj_base_name == active_base_name:
                            matched_objects.append(obj)
        
        # Select all matched objects
        for obj in matched_objects:
            obj.select_set(True)
            
        # Make sure the active object stays selected
        active_obj.select_set(True)
        
        self.report({'INFO'}, f"Selected {len(matched_objects)} similar meshes")
        return {"FINISHED"}

classes = (SELECT_SAME_OT_operator,) 