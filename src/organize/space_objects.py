import bpy
from bpy.types import Operator
import math

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class SPACE_OT_operator(bpy.types.Operator):
    bl_label = "Space Objects"
    bl_idname = "organize.spaceobjects"
    bl_description = "Space selected objects equally along an axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    axis: bpy.props.StringProperty(name="Axis", default="X") # type: ignore
    
    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 1
    
    def execute(self, context):
        selected = sorted([obj for obj in context.selected_objects], 
                          key=lambda obj: obj.location[0 if self.axis == 'X' else 1 if self.axis == 'Y' else 2])
        
        if len(selected) < 2:
            self.report({'ERROR'}, "Select at least 2 objects")
            return {'CANCELLED'}
        
        axis_idx = 0 if self.axis == 'X' else 1 if self.axis == 'Y' else 2
        
        # Get first and last object positions
        first_pos = selected[0].location[axis_idx]
        last_pos = selected[-1].location[axis_idx]
        total_distance = last_pos - first_pos
        
        # Calculate spacing
        count = len(selected) - 1
        if count <= 0:
            return {'CANCELLED'}
        
        # Calculate average object dimension along this axis
        avg_dimension = 0
        for obj in selected:
            if obj.type == 'MESH' and obj.dimensions:
                avg_dimension += obj.dimensions[axis_idx]
        if len(selected) > 0:
            avg_dimension /= len(selected)
            
        # Add 1/10th of average dimension to increase spacing
        extra_space = avg_dimension * 0.1 if avg_dimension > 0 else 0.1
        total_distance += extra_space * count  # Add extra space to total distance
            
        spacing = total_distance / count
        
        # Position objects with equal spacing (keeping first and last in place)
        for i in range(1, len(selected) - 1):
            obj = selected[i]
            new_pos = first_pos + (spacing * i)
            obj.location[axis_idx] = new_pos
        
        # Move the last object to maintain total distance plus expansion
        if len(selected) > 1:
            selected[-1].location[axis_idx] = first_pos + total_distance
        
        self.report({'INFO'}, f"Spaced {len(selected)} objects equally along {self.axis} axis")
        return {'FINISHED'}
    
    @staticmethod
    def are_aligned(objects, axis_idx, threshold=0.001):
        """Check if all objects are aligned on the same axis value within threshold"""
        if not objects or len(objects) < 2:
            return False
            
        first_value = objects[0].location[axis_idx]
        for obj in objects[1:]:
            if abs(obj.location[axis_idx] - first_value) > threshold:
                return False
        return True

# Helper function to check alignment status for UI
def check_axis_alignment(context, axis):
    if len(context.selected_objects) < 2:
        return False
        
    axis_idx = 0 if axis == 'X' else 1 if axis == 'Y' else 2
    objects = context.selected_objects
    
    # Check if objects are all on same value
    first_value = objects[0].location[axis_idx]
    for obj in objects[1:]:
        if abs(obj.location[axis_idx] - first_value) > 0.001:
            return False  # Not aligned, button should be enabled
    
    return True  # All aligned, button should be disabled

classes = (SPACE_OT_operator,) 