import bpy
from bpy.types import Operator
import mathutils

class ORG_ALIGNTOVIEW_OT_operator(bpy.types.Operator):
    bl_label = "Align to View"
    bl_idname = "organize.aligntoview"
    bl_description = "Aligns object to view"
    bl_options = {'REGISTER', 'UNDO'}
    
    apply_rotation: bpy.props.BoolProperty(
        name="Apply Rotation",
        description="Apply the rotation or just show the rotation values",
        default=True
    )
    
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "apply_rotation")
    
    def execute(self, context):
        view_rotation = context.region_data.view_rotation
        
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}
        
        if self.apply_rotation:
            for obj in selected_objects:
                original_location = obj.location.copy()
                obj.rotation_mode = 'QUATERNION'
                obj.rotation_quaternion = view_rotation
                obj.location = original_location
            
            self.report({'INFO'}, f"Aligned {len(selected_objects)} objects to current view")
        else:
            rotation_euler = view_rotation.to_euler()
            x = round(rotation_euler.x * 57.2958, 2)
            y = round(rotation_euler.y * 57.2958, 2)
            z = round(rotation_euler.z * 57.2958, 2)
            self.report({'INFO'}, f"View rotation: X={x}°, Y={y}°, Z={z}°")
        
        return {"FINISHED"}

classes = (ORG_ALIGNTOVIEW_OT_operator,) 