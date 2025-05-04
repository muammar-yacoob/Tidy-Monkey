import bpy
from bpy.types import Operator

class ORG_FIXROTATION_OT_operator(bpy.types.Operator):
    bl_label = "Fix Rotation"
    bl_idname = "fix.rotation"
    bl_description = "Fixes Object Rotation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:    
            bpy.ops.view3d.snap_cursor_to_selected()
            
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    override = bpy.context.copy()
                    override['area'] = area
                    bpy.ops.view3d.view_axis(override, type='BOTTOM', align_active=True, relative=False)
                    break
            
            bpy.ops.object.mode_set(mode='OBJECT')    
            obj = bpy.context.active_object
            bpy.ops.mesh.primitive_cube_add(align='VIEW')
            plane = bpy.context.selected_objects[0]
            
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True) 
            plane.select_set(True)    
            bpy.context.view_layer.objects.active = plane

            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
            bpy.ops.object.rotation_clear(clear_delta=False)
            
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True) 
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

            bpy.ops.object.select_all(action='DESELECT')
            plane.select_set(True) 
            bpy.ops.object.delete(use_global=False)
            
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    override = bpy.context.copy()
                    override['area'] = area
                    bpy.ops.view3d.view_axis(override, type='FRONT', align_active=True, relative=False)
                    break
        except:
            self.report({'ERROR'}, "Please select a face first")
        
        return {"FINISHED"}

classes = (ORG_FIXROTATION_OT_operator,) 