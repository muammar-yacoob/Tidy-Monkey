import bpy
from bpy.types import Operator

class ORG_BOTTOMCENTER_OT_operator(bpy.types.Operator):
    bl_label = "Origin to Bottom Center"
    bl_idname = "organize.origintobottomcenter"
    bl_description = "Sets origin to bottom center (average X/Y, lowest Z)"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        if context.mode != 'OBJECT':
            self.report({'ERROR'}, "Must be in Object Mode")
            return {'CANCELLED'}
            
        sel_objs = [obj for obj in context.selected_objects if obj.type in {'MESH', 'ARMATURE'}]
        if not sel_objs:
            self.report({'ERROR'}, "No mesh or armature objects selected")
            return {'CANCELLED'}
            
        original_cursor = context.scene.cursor.location.copy()
        original_selection = set(sel_objs)
        original_active = context.view_layer.objects.active
        processed_count = 0
        
        for obj in sel_objs:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            verts = []
            if obj.type == 'MESH':
                verts = [obj.matrix_world @ v.co for v in obj.data.vertices]
            elif obj.type == 'ARMATURE':
                if obj.data.bones:
                    verts = [obj.matrix_world @ bone.head_local for bone in obj.data.bones]
                    verts.extend([obj.matrix_world @ bone.tail_local for bone in obj.data.bones])
            
            if not verts:
                continue
                
            min_z = min(v.z for v in verts)
            avg_x = sum(v.x for v in verts) / len(verts)
            avg_y = sum(v.y for v in verts) / len(verts)
            
            context.scene.cursor.location = (avg_x, avg_y, min_z)
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            processed_count += 1
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in original_selection:
            obj.select_set(True)
            
        if original_active:
            context.view_layer.objects.active = original_active
            
        context.scene.cursor.location = original_cursor
        
        self.report({'INFO'}, f"Set origin to bottom center for {processed_count} objects")
        return {'FINISHED'}

classes = (ORG_BOTTOMCENTER_OT_operator,) 