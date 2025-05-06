import bpy
from bpy.types import Operator
import mathutils

class ALIGN_OT_operator(bpy.types.Operator):
    bl_label = "Align Objects"
    bl_idname = "alignobjects.align"
    bl_description = "Aligns objects along a specific axis using current pivot"
    bl_options = {'REGISTER', 'UNDO'}
    
    algn: bpy.props.StringProperty(default='Z', options={'HIDDEN'})
    
    def execute(self, context):
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if len(selected_objects) < 2:
            self.report({'ERROR'}, "Select at least two mesh objects")
            return {'CANCELLED'}
        
        axis_index = {'X': 0, 'Y': 1, 'Z': 2}.get(self.algn, 2)
        
        pivot_point = context.scene.tool_settings.transform_pivot_point
        alignment_value = None
        
        if pivot_point == 'BOUNDING_BOX_CENTER':
            min_co = float('inf')
            max_co = float('-inf')
            
            for obj in selected_objects:
                for corner in obj.bound_box:
                    world_corner = obj.matrix_world @ mathutils.Vector(corner)
                    min_co = min(min_co, world_corner[axis_index])
                    max_co = max(max_co, world_corner[axis_index])
            
            alignment_value = (min_co + max_co) / 2
            
        elif pivot_point == 'CURSOR':
            alignment_value = context.scene.cursor.location[axis_index]
            
        elif pivot_point == 'MEDIAN_POINT':
            sum_co = 0
            for obj in selected_objects:
                sum_co += obj.matrix_world.translation[axis_index]
            alignment_value = sum_co / len(selected_objects)
            
        elif pivot_point == 'ACTIVE_ELEMENT':
            if context.active_object and context.active_object in selected_objects:
                alignment_value = context.active_object.matrix_world.translation[axis_index]
            else:
                self.report({'WARNING'}, f"No active object, using median for {self.algn} axis")
                sum_co = 0
                for obj in selected_objects:
                    sum_co += obj.matrix_world.translation[axis_index]
                alignment_value = sum_co / len(selected_objects)
        
        elif pivot_point == 'INDIVIDUAL_ORIGINS':
            self.report({'WARNING'}, "Individual origins not applicable, using median point")
            sum_co = 0
            for obj in selected_objects:
                sum_co += obj.matrix_world.translation[axis_index]
            alignment_value = sum_co / len(selected_objects)
        
        if alignment_value is not None:
            for obj in selected_objects:
                if pivot_point == 'ACTIVE_ELEMENT' and obj == context.active_object:
                    continue
                    
                new_location = obj.matrix_world.translation.copy()
                new_location[axis_index] = alignment_value
                obj.matrix_world.translation = new_location
        
        self.report({'INFO'}, f"Aligned objects on {self.algn} axis using {pivot_point}")
        return {"FINISHED"}

classes = (ALIGN_OT_operator,) 