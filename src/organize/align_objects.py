import bpy
from bpy.types import Operator
import mathutils

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class OBJECT_OT_align(bpy.types.Operator):
    bl_label = "Align Objects"
    bl_idname = "object.align"
    bl_description = "Aligns objects along a specific axis using current pivot"
    bl_options = {'REGISTER', 'UNDO'}
    
    algn: bpy.props.StringProperty(default='Z', options={'HIDDEN'})
    spacing: bpy.props.FloatProperty(name="Spacing", description="Space between objects after alignment", default=0.0, unit='LENGTH')
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and len(context.selected_objects) > 1
    
    def invoke(self, context, event):
        self.spacing = 0.0
        return self.execute(context)
    
    def execute(self, context):
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if len(selected_objects) < 2:
            self.report({'ERROR'}, "Select at least two mesh objects")
            return {'CANCELLED'}
        
        axis_index = {'X': 0, 'Y': 1, 'Z': 2}.get(self.algn, 2)
        
        # Calculate average position for alignment
        avg_pos = sum((obj.matrix_world.translation[axis_index] for obj in selected_objects)) / len(selected_objects)
        
        # Align objects to average position
        for obj in selected_objects:
            loc = obj.matrix_world.translation.copy()
            loc[axis_index] = avg_pos
            obj.matrix_world.translation = loc
        
        if self.spacing != 0.0:
            sorted_objects = sorted(selected_objects, key=lambda obj: obj.matrix_world.translation[axis_index])
            base_pos = sorted_objects[0].matrix_world.translation[axis_index]
            
            # Apply spacing
            for i, obj in enumerate(sorted_objects[1:], 1):
                loc = obj.matrix_world.translation.copy()
                loc[axis_index] = base_pos + (i * self.spacing)
                obj.matrix_world.translation = loc
        
        spacing_info = f" with {self.spacing} spacing" if self.spacing != 0.0 else ""
        self.report({'INFO'}, f"Aligned objects on {self.algn} axis{spacing_info}")
        return {"FINISHED"}
    
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "spacing", text=f"Spacing({self.algn})")

classes = (OBJECT_OT_align,) 