import bpy
from bpy.types import Operator
import os

class EXPORT_OT_operator(bpy.types.Operator):
    bl_idname = "exportfbxxx.export"
    bl_label = "Export FBX"
    bl_description = "Exports selected objects as FBX files"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        blend_file_path = bpy.data.filepath
        directory = os.path.dirname(blend_file_path) + "/FBXs"
        if not os.path.exists(directory):
            os.mkdir(directory)

        sel_objs = [obj for obj in context.selected_objects]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.outliner.orphans_purge()
        try:
            bpy.ops.file.pack_all()
        except Exception as e:
            self.report({'ERROR'}, f"Could not pack all textures\n{str(e)}")
        try:
            bpy.ops.file.unpack_all(method='USE_LOCAL')
            bpy.ops.file.make_paths_absolute()
        except:
            self.report({'ERROR'}, "Error packing textures")

        current_frame = context.scene.frame_current
        bpy.ops.screen.animation_cancel(restore_frame=True)
        context.scene.frame_set(context.scene.frame_start)

        for obj in sel_objs:
            bpy.ops.object.select_all(action='DESELECT')
            obj_path = os.path.join(directory, obj.name + ".fbx")

            obj.select_set(True)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            original_loc = obj.location.copy()
            obj.location = (0, 0, 0)

            has_shape_key = bool(obj.type == 'ARMATURE')
            if not has_shape_key:
                try:
                    has_shape_key = len(obj.data.shape_keys.key_blocks) > 0
                except:
                    pass

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
                    use_tspace=True,
                    use_custom_props=True,
                    bake_space_transform=True,
                    bake_anim=True,
                    bake_anim_use_nla_strips=True,
                    bake_anim_use_all_actions=True,
                    add_leaf_bones=False,
                    primary_bone_axis='Y',
                    secondary_bone_axis='X',
                    use_armature_deform_only=True,
                    path_mode='AUTO',
                    batch_mode='OFF',
                    use_metadata=True,
                )
            except Exception as e:
                self.report({'ERROR'}, f"Could not export FBX file\n{str(e)}")

            obj.location = original_loc
            obj.select_set(False)

        context.scene.frame_set(current_frame)
        for obj in sel_objs:
            obj.select_set(True)
        self.report({'INFO'}, f"{len(sel_objs)} objects were exported to {directory}")
        os.system("start " + os.path.dirname(blend_file_path))
        return {'FINISHED'}

classes = (EXPORT_OT_operator,) 