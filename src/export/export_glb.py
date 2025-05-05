import bpy
from bpy.types import Operator
import os

class EXPORT_GLB_OT_operator(bpy.types.Operator):
    bl_idname = "exportglb.export"
    bl_label = "Export GLB"
    bl_description = "Exports selected objects as GLB files for web/game engines"

    def execute(self, context):
        if not bpy.data.filepath:
            self.report({'ERROR'}, "Please save your file first before exporting")
            return {'CANCELLED'}
            
        bpy.ops.object.mode_set(mode='OBJECT')
        
        blend_file_path = bpy.data.filepath
        directory = os.path.dirname(blend_file_path) + "/GLBs"
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
            
            obj_path = os.path.join(directory, arm.name + ".glb")
            
            try:
                bpy.ops.export_scene.gltf(
                    filepath=obj_path,
                    export_format='GLB',
                    use_selection=True,
                    export_animations=True,
                    export_frame_range=True,
                    export_frame_step=1,
                    export_apply=False,  # Don't apply transformations
                    export_texcoords=True,
                    export_normals=True,
                    export_tangents=True,
                    export_materials='EXPORT',
                    export_colors=True,
                    export_cameras=False,
                    export_lights=False,
                    export_extras=False,
                    export_yup=True,
                    export_force_sampling=True,
                    export_nla_strips=True,
                    export_skins=True,
                    export_all_influences=False,
                    export_morph=True,
                    export_morph_normal=True,
                    export_morph_tangent=False,
                    export_attributes=False,
                    export_image_format='AUTO',
                    export_texture_dir="textures",
                    export_keep_originals=False,
                    export_texcoords_from_uv_map="",
                    export_materials_for_motion_blur=False,
                    export_current_frame=False,
                    export_draco_mesh_compression_enable=False,
                    export_draco_mesh_compression_level=6,
                    export_draco_position_quantization=14,
                    export_draco_normal_quantization=10,
                    export_draco_texcoord_quantization=12,
                    export_draco_color_quantization=10,
                    export_draco_generic_quantization=12,
                    export_anim_single_armature=True,
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
            
            has_morph = False
            if obj.type == 'MESH' and hasattr(obj.data, 'shape_keys') and obj.data.shape_keys:
                if obj.data.shape_keys.key_blocks:
                    has_morph = len(obj.data.shape_keys.key_blocks) > 0
                    
            obj_path = os.path.join(directory, obj.name + ".glb")
            
            try:
                bpy.ops.export_scene.gltf(
                    filepath=obj_path,
                    export_format='GLB',
                    use_selection=True,
                    export_animations=has_morph,
                    export_frame_range=has_morph,
                    export_frame_step=1,
                    export_apply=False,  # Don't apply transformations
                    export_texcoords=True,
                    export_normals=True,
                    export_tangents=True,
                    export_materials='EXPORT',
                    export_colors=True,
                    export_cameras=False,
                    export_lights=False,
                    export_extras=False,
                    export_yup=True,
                    export_force_sampling=True,
                    export_nla_strips=has_morph,
                    export_skins=True,
                    export_all_influences=False,
                    export_morph=has_morph,
                    export_morph_normal=has_morph,
                    export_morph_tangent=False,
                    export_attributes=False,
                    export_image_format='AUTO',
                    export_texture_dir="textures",
                    export_keep_originals=False,
                    export_texcoords_from_uv_map="",
                    export_materials_for_motion_blur=False,
                    export_current_frame=False,
                    export_draco_mesh_compression_enable=False,
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

classes = (EXPORT_GLB_OT_operator,) 