import bpy
from bpy.types import Operator
import math

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class SpacingProperties(bpy.types.PropertyGroup):
    x_spacing: bpy.props.FloatProperty(name="X Spacing", default=0.0) # type: ignore
    y_spacing: bpy.props.FloatProperty(name="Y Spacing", default=0.0) # type: ignore
    z_spacing: bpy.props.FloatProperty(name="Z Spacing", default=0.0) # type: ignore

class SPACE_OT_operator(bpy.types.Operator):
    bl_label = "Space Objects"
    bl_idname = "organize.spaceobjects"
    bl_description = "Space selected objects along an axis"
    bl_options = {'REGISTER', 'UNDO'}
    
    axis: bpy.props.StringProperty(name="Axis", default="X") # type: ignore
    
    @classmethod
    def poll(cls, context): return len(context.selected_objects) > 1
    
    def execute(self, context):
        axis_idx = 0 if self.axis == 'X' else 1 if self.axis == 'Y' else 2
        selected = sorted([obj for obj in context.selected_objects], key=lambda obj: obj.location[axis_idx])
        
        if len(selected) < 2: return {'CANCELLED'}
        
        avg_dimension = sum([obj.dimensions[axis_idx] if hasattr(obj, "dimensions") and obj.dimensions else 0.1 for obj in selected]) / len(selected)
        
        is_touching = True
        current_extra_spacing = 0
        
        for i in range(1, len(selected)):
            prev_half_dim = selected[i-1].dimensions[axis_idx] / 2 if selected[i-1].dimensions else 0.1
            curr_half_dim = selected[i].dimensions[axis_idx] / 2 if selected[i].dimensions else 0.1
            expected_pos = selected[i-1].location[axis_idx] + prev_half_dim + curr_half_dim
            actual_gap = selected[i].location[axis_idx] - expected_pos
            
            if actual_gap > 0.001:
                is_touching = False
                current_extra_spacing = max(current_extra_spacing, actual_gap / avg_dimension)
        
        spacing_factor = 0 if is_touching else current_extra_spacing + 0.1
        current_pos = selected[0].location[axis_idx]
        
        for i in range(1, len(selected)):
            prev_half_dim = selected[i-1].dimensions[axis_idx] / 2 if selected[i-1].dimensions else 0.1
            curr_half_dim = selected[i].dimensions[axis_idx] / 2 if selected[i].dimensions else 0.1
            extra_space = avg_dimension * spacing_factor if spacing_factor > 0 else 0
            current_pos += prev_half_dim + curr_half_dim + extra_space
            selected[i].location[axis_idx] = current_pos
        
        self.report({'INFO'}, f"{'Arranged' if is_touching else 'Increased spacing between'} {len(selected)} objects along {self.axis} axis")
        return {'FINISHED'}

classes = (SPACE_OT_operator,) 