import bpy
from bpy.types import Operator
import mathutils

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class ALIGN_OT_operator(bpy.types.Operator):
    bl_label = "Align Objects"
    bl_idname = "organize.alignobjects"
    bl_description = "Aligns objects along axis with optional spacing"
    bl_options = {'REGISTER', 'UNDO'}
    
    algn: bpy.props.StringProperty(default='Z', options={'HIDDEN'})
    spacing: bpy.props.FloatProperty(name="Spacing", description="Distance between objects", default=0.0, min=0.0, precision=3)
    
    def execute(self, context):
        selected = [obj for obj in context.selected_objects if obj.type == 'MESH']
        if len(selected) < 2: return {'CANCELLED'}
        
        axis_idx = {'X': 0, 'Y': 1, 'Z': 2}.get(self.algn, 2)
        pivot = context.scene.tool_settings.transform_pivot_point
        active = context.active_object
        
        alignment_value = 0.0
        if pivot == 'ACTIVE_ELEMENT' and active and active in selected:
            alignment_value = active.matrix_world.translation[axis_idx]
        elif pivot == 'BOUNDING_BOX_CENTER':
            min_co, max_co = float('inf'), float('-inf')
            for obj in selected:
                for corner in obj.bound_box:
                    world_corner = obj.matrix_world @ mathutils.Vector(corner)
                    min_co, max_co = min(min_co, world_corner[axis_idx]), max(max_co, world_corner[axis_idx])
            alignment_value = (min_co + max_co) / 2 if min_co != float('inf') else 0.0
        elif pivot == 'CURSOR':
            alignment_value = context.scene.cursor.location[axis_idx]
        else:
            sum_co = sum(obj.matrix_world.translation[axis_idx] for obj in selected)
            alignment_value = sum_co / len(selected)
        
        for obj in selected:
            loc = obj.matrix_world.translation.copy()
            loc[axis_idx] = alignment_value
            obj.matrix_world.translation = loc
            
        if self.spacing > 0.0001:
            objects_to_space = sorted(selected, key=lambda o: o.name)
            scale_mult = active.scale[axis_idx] if active and active in selected else 1.0
            spacing_unit = self.spacing * scale_mult
            
            for i, obj in enumerate(objects_to_space):
                loc = obj.matrix_world.translation.copy()
                loc[axis_idx] = alignment_value + (i * spacing_unit)
                obj.matrix_world.translation = loc
        
        self.report({'INFO'}, f"Aligned on {self.algn}")
        return {"FINISHED"}

classes = (ALIGN_OT_operator,) 