import bpy
from bpy.types import Operator
import mathutils

class ORG_ALIGNTOVIEW_OT_operator(bpy.types.Operator):
    bl_label = "Align to View"
    bl_idname = "align.toview"
    bl_description = "Aligns object to view"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Get the current view rotation as a quaternion
        view_rotation = context.region_data.view_rotation
        
        # Get currently selected objects
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}
        
        # Apply the view rotation to each selected object
        for obj in selected_objects:
            # Store the original location
            original_location = obj.location.copy()
            
            # Set rotation mode to quaternion
            obj.rotation_mode = 'QUATERNION'
            
            # Apply the view rotation
            obj.rotation_quaternion = view_rotation
            
            # Restore the original location
            obj.location = original_location
        
        self.report({'INFO'}, "Aligned objects to current view")
        return {"FINISHED"}

class ALIGN_OT_operator(bpy.types.Operator):
    bl_label = "Align Objects"
    bl_idname = "alignobjects.align"
    bl_description = "Aligns objects along a specific axis using current pivot"
    bl_options = {'REGISTER', 'UNDO'}
    
    algn: bpy.props.StringProperty(default='Z', options={'HIDDEN'})
    
    def execute(self, context):
        # Get selected objects
        selected_objects = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if len(selected_objects) < 2:
            self.report({'ERROR'}, "Select at least two mesh objects")
            return {'CANCELLED'}
        
        # Determine the axis index (X=0, Y=1, Z=2)
        axis_index = {'X': 0, 'Y': 1, 'Z': 2}.get(self.algn, 2)
        
        # Get the pivot point type
        pivot_point = context.scene.tool_settings.transform_pivot_point
        alignment_value = None
        
        # Calculate the target position based on pivot type
        if pivot_point == 'BOUNDING_BOX_CENTER':
            # Use bounding box center of all objects
            min_co = float('inf')
            max_co = float('-inf')
            
            for obj in selected_objects:
                for corner in obj.bound_box:
                    world_corner = obj.matrix_world @ mathutils.Vector(corner)
                    min_co = min(min_co, world_corner[axis_index])
                    max_co = max(max_co, world_corner[axis_index])
            
            alignment_value = (min_co + max_co) / 2
            
        elif pivot_point == 'CURSOR':
            # Use 3D cursor position for the selected axis
            alignment_value = context.scene.cursor.location[axis_index]
            
        elif pivot_point == 'MEDIAN_POINT':
            # Use median point of selection on the selected axis
            sum_co = 0
            for obj in selected_objects:
                sum_co += obj.matrix_world.translation[axis_index]
            alignment_value = sum_co / len(selected_objects)
            
        elif pivot_point == 'ACTIVE_ELEMENT':
            # Use active object as reference
            if context.active_object and context.active_object in selected_objects:
                alignment_value = context.active_object.matrix_world.translation[axis_index]
            else:
                self.report({'WARNING'}, f"No active object, using median for {self.algn} axis")
                # Fall back to median point
                sum_co = 0
                for obj in selected_objects:
                    sum_co += obj.matrix_world.translation[axis_index]
                alignment_value = sum_co / len(selected_objects)
        
        elif pivot_point == 'INDIVIDUAL_ORIGINS':
            # Individual origins don't make sense for alignment
            self.report({'WARNING'}, "Individual origins not applicable, using median point")
            # Fall back to median point
            sum_co = 0
            for obj in selected_objects:
                sum_co += obj.matrix_world.translation[axis_index]
            alignment_value = sum_co / len(selected_objects)
        
        # Apply the alignment to each object
        if alignment_value is not None:
            for obj in selected_objects:
                if pivot_point == 'ACTIVE_ELEMENT' and obj == context.active_object:
                    continue  # Skip the active object if it's the pivot
                    
                # Create a new location with the aligned axis
                new_location = obj.matrix_world.translation.copy()
                new_location[axis_index] = alignment_value
                obj.matrix_world.translation = new_location
        
        self.report({'INFO'}, f"Aligned objects on {self.algn} axis using {pivot_point}")
        return {"FINISHED"}

classes = (ORG_ALIGNTOVIEW_OT_operator, ALIGN_OT_operator) 