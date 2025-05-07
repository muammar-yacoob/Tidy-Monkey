import bpy
from bpy.types import Operator
import mathutils

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class ORG_ALIGNTOVIEW_OT_operator(bpy.types.Operator):
    bl_label = "Align to View"
    bl_idname = "organize.aligntoview"
    bl_description = "Aligns objects to match view rotation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        selected_objects = context.selected_objects
        if not selected_objects:
            return {'CANCELLED'}
            
        for obj in selected_objects:
            orig_mode = obj.rotation_mode
            obj.rotation_mode = 'QUATERNION'
            obj.rotation_quaternion = context.region_data.view_rotation
            obj.rotation_mode = orig_mode
        
        return {"FINISHED"}

classes = (ORG_ALIGNTOVIEW_OT_operator,) 