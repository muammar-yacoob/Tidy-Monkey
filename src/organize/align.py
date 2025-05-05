import bpy
from bpy.types import Operator
import mathutils

class ORG_ALIGNTOVIEW_OT_operator(bpy.types.Operator):
    bl_label = "Align to View"
    bl_idname = "align.toview"
    bl_description = "Aligns object to view using current pivot"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        # Get the current view rotation
        view_rotation = context.region_data.view_rotation
        
        # Get currently selected objects
        selected_objects = context.selected_objects
        if not selected_objects:
            self.report({'ERROR'}, "No objects selected")
            return {'CANCELLED'}
        
        # Determine pivot point based on current transform settings
        pivot_point = context.scene.tool_settings.transform_pivot_point
        pivot_position = None
        
        if pivot_point == 'BOUNDING_BOX_CENTER':
            # Use bounding box center of selection
            min_co = mathutils.Vector((float('inf'), float('inf'), float('inf')))
            max_co = mathutils.Vector((float('-inf'), float('-inf'), float('-inf')))
            
            for obj in selected_objects:
                for corner in obj.bound_box:
                    world_corner = obj.matrix_world @ mathutils.Vector(corner)
                    min_co.x = min(min_co.x, world_corner.x)
                    min_co.y = min(min_co.y, world_corner.y)
                    min_co.z = min(min_co.z, world_corner.z)
                    max_co.x = max(max_co.x, world_corner.x)
                    max_co.y = max(max_co.y, world_corner.y)
                    max_co.z = max(max_co.z, world_corner.z)
            
            pivot_position = (min_co + max_co) / 2
            
        elif pivot_point == 'CURSOR':
            # Use 3D cursor position
            pivot_position = context.scene.cursor.location
            
        elif pivot_point == 'INDIVIDUAL_ORIGINS':
            # Each object rotates around its own origin
            for obj in selected_objects:
                original_location = obj.location.copy()
                obj.rotation_euler = view_rotation.to_euler()
                obj.location = original_location
            
            self.report({'INFO'}, "Aligned objects to view using individual origins")
            return {'FINISHED'}
            
        elif pivot_point == 'MEDIAN_POINT':
            # Use median point of selection
            if selected_objects:
                sum_co = mathutils.Vector((0, 0, 0))
                for obj in selected_objects:
                    sum_co += obj.matrix_world.translation
                pivot_position = sum_co / len(selected_objects)
        
        elif pivot_point == 'ACTIVE_ELEMENT':
            # Use active object as pivot
            if context.active_object:
                pivot_position = context.active_object.matrix_world.translation
            else:
                self.report({'WARNING'}, "No active object, using first selected")
                pivot_position = selected_objects[0].matrix_world.translation
        
        # Apply the rotation around the pivot point
        if pivot_position is not None:
            for obj in selected_objects:
                # Store original position relative to pivot
                original_position = obj.matrix_world.translation - pivot_position
                
                # Apply rotation to this relative position
                rotated_position = view_rotation @ original_position
                
                # Set the new rotation
                obj.rotation_euler = view_rotation.to_euler()
                
                # Calculate and set the new position
                obj.matrix_world.translation = pivot_position + rotated_position
        
        self.report({'INFO'}, f"Aligned to view using {pivot_point} pivot")
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