import bpy
from bpy.types import Operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class ORG_CENTER_OT_operator(bpy.types.Operator):
    bl_label = "Center Origins"
    bl_idname = "organize.centerorigins"
    bl_description = "Centers the origin of selected objects"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        sel_objs = [obj for obj in context.selected_objects]
        original_active = context.view_layer.objects.active
        
        for obj in sel_objs:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in sel_objs:
            obj.select_set(True)
        context.view_layer.objects.active = original_active
        
        self.report({'INFO'}, f"Centered origins for {len(sel_objs)} objects")
        return {"FINISHED"}

classes = (ORG_CENTER_OT_operator,) 