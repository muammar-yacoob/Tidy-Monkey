import bpy
from bpy.types import Operator
import mathutils

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class ALIGN_OT_operator(bpy.types.Operator):
    bl_label = "Align Objects"
    bl_idname = "organize.alignobjects"
    bl_description = "Aligns objects along a specific axis using current pivot"
    bl_options = {'REGISTER', 'UNDO'}
    
    algn: bpy.props.StringProperty(default='Z', options={'HIDDEN'})
    spacing: bpy.props.FloatProperty(name="Spacing", description="Space between objects after alignment", default=0.0, unit='LENGTH')
    
    def invoke(self, context, event):
        self.spacing = 0.0
        return self.execute(context)
    
    def execute(self, context):
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if len(selected_objects) < 2:
            self.report({'ERROR'}, "Select at least two mesh objects")
            return {'CANCELLED'}
        
        axis_index = {'X': 0, 'Y': 1, 'Z': 2}.get(self.algn, 2)
        
        if self.algn == 'X': bpy.ops.object.align(align_axis={'X'})
        elif self.algn == 'Y': bpy.ops.object.align(align_axis={'Y'})
        else: bpy.ops.object.align(align_axis={'Z'})
        
        if self.spacing != 0.0:
            sorted_objects = sorted(selected_objects, key=lambda obj: obj.matrix_world.translation[axis_index])
            original_selection = context.selected_objects.copy()
            original_active = context.active_object
            bpy.ops.object.select_all(action='DESELECT')
            base_pos = sorted_objects[0].matrix_world.translation[axis_index]
            
            for i, obj in enumerate(sorted_objects):
                if i == 0: continue
                obj.select_set(True)
                context.view_layer.objects.active = obj
                target_pos = base_pos + (i * self.spacing)
                current_pos = obj.matrix_world.translation[axis_index]
                offset = target_pos - current_pos
                
                if axis_index == 0: bpy.ops.transform.translate(value=(offset, 0, 0))
                elif axis_index == 1: bpy.ops.transform.translate(value=(0, offset, 0))
                else: bpy.ops.transform.translate(value=(0, 0, offset))
                
                obj.select_set(False)
            
            for obj in original_selection: obj.select_set(True)
            if original_active: context.view_layer.objects.active = original_active
        
        spacing_info = f" with {self.spacing} spacing" if self.spacing != 0.0 else ""
        self.report({'INFO'}, f"Aligned objects on {self.algn} axis{spacing_info}")
        return {"FINISHED"}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "spacing", text=f"Spacing({self.algn})")

classes = (ALIGN_OT_operator,) 