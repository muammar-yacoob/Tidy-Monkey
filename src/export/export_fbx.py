import bpy
from bpy.types import Operator
import os

class EXPORT_OT_operator(bpy.types.Operator):
    bl_idname = "exportfbx.export"
    bl_label = "Export FBX"
    bl_description = "Exports selected objects as FBX files"

    def execute(self, context):
        if not bpy.data.filepath:
            self.report({'ERROR'}, "Please save your file first before exporting")
            return {'CANCELLED'}
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        blend_file_path = bpy.data.filepath
        directory = os.path.dirname(blend_file_path) + "/FBXs"
        if not os.path.exists(directory):
            os.mkdir(directory)

        sel_objs = [obj for obj in context.selected_objects]
        if not sel_objs:
            self.report({'ERROR'}, "No objects selected to export")
            return {'CANCELLED'}
        
        armatures = [obj for obj in sel_objs if obj.type == 'ARMATURE']
        armature_children = {}
        
        for arm in armatures:
            armature_children[arm] = [obj for obj in bpy.data.objects 
                                     if obj.parent == arm and obj.type == 'MESH']
        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.outliner.orphans_purge()
        
        try:
            bpy.ops.file.pack_all()
        except Exception as e:
            self.report({'WARNING'}, f"Could not pack all textures\n{str(e)}")
        
        try:
            bpy.ops.file.unpack_all(method='USE_LOCAL')
            bpy.ops.file.make_paths_absolute()
        except Exception as e:
            self.report({'WARNING'}, "Error processing textures")
        
        current_frame = context.scene.frame_current
        bpy.ops.screen.animation_cancel(restore_frame=True)
        context.scene.frame_set(context.scene.frame_start)
        
        exported_count = 0
        
        for arm in armatures:
            children = armature_children[arm]
            if not children:
                continue
                
            bpy.ops.object.select_all(action='DESELECT')
            
            arm.select_set(True)
            for child in children:
                child.select_set(True)
                
            context.view_layer.objects.active = arm
            
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            
            obj_path = os.path.join(directory, arm.name + ".fbx")
            
            try:
                bpy.ops.export_scene.fbx(
                    filepath=obj_path,
                    use_selection=True,
                    check_existing=False,
                    global_scale=1.0,
                    apply_scale_options='FBX_SCALE_UNITS',
                    axis_forward='-Z',
                    axis_up='Y',
                    use_mesh_modifiers=True,
                    mesh_smooth_type='FACE',
                    use_mesh_edges=False,
                    use_tspace=True,  # Important for normal maps
                    use_custom_props=True,
                    bake_space_transform=False,  # Don't bake transforms to preserve positions
                    bake_anim=True,
                    bake_anim_use_nla_strips=True,
                    bake_anim_use_all_actions=True,
                    add_leaf_bones=False,
                    primary_bone_axis='Y',
                    secondary_bone_axis='X',
                    use_armature_deform_only=False,  # Include all modifiers
                    path_mode='COPY',  # Copy textures
                    embed_textures=True,  # Embed textures
                    batch_mode='OFF',
                    use_metadata=True,
                )
                exported_count += 1
                self.report({'INFO'}, f"Exported armature: {arm.name}")
            except Exception as e:
                self.report({'ERROR'}, f"Could not export armature {arm.name}\n{str(e)}")
        
        remaining_objs = [obj for obj in sel_objs if obj not in armatures and 
                         obj.parent not in armatures]
        
        for obj in remaining_objs:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            
            has_shape_key = False
            if obj.type == 'MESH' and hasattr(obj.data, 'shape_keys') and obj.data.shape_keys:
                if obj.data.shape_keys.key_blocks:
                    has_shape_key = len(obj.data.shape_keys.key_blocks) > 0
            
            obj_path = os.path.join(directory, obj.name + ".fbx")
            
            try:
                bpy.ops.export_scene.fbx(
                    filepath=obj_path,
                    use_selection=True,
                    check_existing=False,
                    global_scale=1.0,
                    apply_scale_options='FBX_SCALE_UNITS',
                    axis_forward='-Z',
                    axis_up='Y',
                    use_mesh_modifiers=True,
                    mesh_smooth_type='FACE',
                    use_mesh_edges=False,
                    use_tspace=True,  # Important for normal maps
                    use_custom_props=True,
                    bake_space_transform=False,  # Don't bake transforms to preserve positions
                    bake_anim=has_shape_key,
                    bake_anim_use_nla_strips=has_shape_key,
                    bake_anim_use_all_actions=has_shape_key,
                    add_leaf_bones=False,
                    primary_bone_axis='Y',
                    secondary_bone_axis='X',
                    use_armature_deform_only=False,  # Include all modifiers
                    path_mode='COPY',  # Copy textures
                    embed_textures=True,  # Embed textures
                    batch_mode='OFF',
                    use_metadata=True,
                )
                exported_count += 1
            except Exception as e:
                self.report({'ERROR'}, f"Could not export object {obj.name}\n{str(e)}")
        
        context.scene.frame_set(current_frame)
        bpy.ops.object.select_all(action='DESELECT')
        for obj in sel_objs:
            obj.select_set(True)
        
        self.report({'INFO'}, f"{exported_count} objects were exported to {directory}")
        os.system("start " + directory)
        return {'FINISHED'}

classes = (EXPORT_OT_operator,) 