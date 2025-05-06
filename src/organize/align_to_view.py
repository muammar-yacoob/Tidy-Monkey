import bpy
from bpy.types import Operator
import mathutils

class ORG_ALIGNTOVIEW_OT_operator(bpy.types.Operator):
    bl_label = "Align to View"
    bl_idname = "organize.aligntoview"
    bl_description = "Aligns object to view (Hold Alt to skip rotation)"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        view_rotation = context.region_data.view_rotation
        
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}
        
        # Check if Alt key is pressed - if it is, don't apply rotation
        apply_rotation = not self.alt_pressed
        
        for obj in selected_objects:
            original_location = obj.location.copy()
            
            if apply_rotation:
                obj.rotation_mode = 'QUATERNION'
                obj.rotation_quaternion = view_rotation
            
            obj.location = original_location
        
        action_text = "Positioned" if not apply_rotation else "Aligned"
        self.report({'INFO'}, f"{action_text} {len(selected_objects)} objects to current view")
        return {"FINISHED"}
    
    def invoke(self, context, event):
        self.alt_pressed = event.alt
        return self.execute(context)

classes = (ORG_ALIGNTOVIEW_OT_operator,) 