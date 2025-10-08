import bpy
from bpy.types import Operator
import mathutils

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class OBJECT_OT_origin_to_bottom(bpy.types.Operator):
    bl_label = "Origin to Bottom Center"
    bl_idname = "object.origin_to_bottom"
    bl_description = "Sets origin to bottom center (average X/Y, lowest Z)"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT' and context.selected_objects
    
    def execute(self, context):
        sel_objs = [obj for obj in context.selected_objects if obj.type in {'MESH', 'ARMATURE'}]
        if not sel_objs:
            self.report({'ERROR'}, "No mesh or armature objects selected")
            return {'CANCELLED'}
        
        processed_count = 0
        
        for obj in sel_objs:
            # Get world space vertices
            verts = []
            if obj.type == 'MESH':
                verts = [obj.matrix_world @ v.co for v in obj.data.vertices]
            elif obj.type == 'ARMATURE':
                if obj.data.bones:
                    verts = [obj.matrix_world @ bone.head_local for bone in obj.data.bones]
                    verts.extend([obj.matrix_world @ bone.tail_local for bone in obj.data.bones])
            
            if not verts:
                continue
            
            # Calculate new origin position
            min_z = min(v.z for v in verts)
            avg_x = sum(v.x for v in verts) / len(verts)
            avg_y = sum(v.y for v in verts) / len(verts)
            new_origin = mathutils.Vector((avg_x, avg_y, min_z))
            
            # Calculate the difference between current origin and new origin
            delta = new_origin - obj.matrix_world.translation
            
            # Update mesh/armature data to keep vertices in place
            if obj.type == 'MESH':
                for v in obj.data.vertices:
                    v.co = obj.matrix_world.inverted() @ (obj.matrix_world @ v.co - delta)
            elif obj.type == 'ARMATURE':
                for bone in obj.data.bones:
                    bone.head_local = obj.matrix_world.inverted() @ (obj.matrix_world @ bone.head_local - delta)
                    bone.tail_local = obj.matrix_world.inverted() @ (obj.matrix_world @ bone.tail_local - delta)
            
            # Move object origin
            obj.matrix_world.translation = new_origin
            processed_count += 1
        
        self.report({'INFO'}, f"Set origin to bottom center for {processed_count} objects")
        return {'FINISHED'}

classes = (OBJECT_OT_origin_to_bottom,) 