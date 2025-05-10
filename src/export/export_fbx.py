import bpy
from bpy.types import Operator
import os
import platform
import subprocess

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

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
        directory = os.path.join(os.path.dirname(blend_file_path), "FBXs")
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        sel_objs = [obj for obj in context.selected_objects]
        if not sel_objs:
            self.report({'ERROR'}, "No objects selected to export")
            return {'CANCELLED'}
        
        armatures = [obj for obj in sel_objs if obj.type == 'ARMATURE']
        armature_children = {}
        
        for arm in armatures:
            armature_children[arm] = [obj for obj in bpy.data.objects 
                                     if obj.parent == arm and obj.type == 'MESH']
        
        original_active = context.view_layer.objects.active
        original_area_type = context.area.type
        
        bpy.ops.cleanup.cleantextures()
        bpy.ops.cleanup.clearmats()
        
        try: bpy.ops.cleanup.generateactions()
        except Exception as e: self.report({'INFO'}, "No actions to generate")
        
        # try: bpy.ops.organize.applymodifiers()
        # except Exception as e: self.report({'INFO'}, "No modifiers to apply")
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in sel_objs:
            obj.select_set(True)
        if original_active:
            context.view_layer.objects.active = original_active
        
        try: bpy.ops.file.pack_all()
        except Exception as e: self.report({'WARNING'}, f"Could not pack all textures: {str(e)}")
        
        try:
            bpy.ops.file.unpack_all(method='USE_LOCAL')
            bpy.ops.file.make_paths_absolute()
        except Exception as e: self.report({'WARNING'}, "Error processing textures")
        
        current_frame = context.scene.frame_current
        context.scene.frame_set(context.scene.frame_start)
        
        exported_count = 0
        
        # Helper function to check if an object is a child of an armature in any parent level
        def is_armature_child(obj, arm):
            parent = obj.parent
            while parent:
                if parent == arm:
                    return True
                parent = parent.parent
            return False
        
        for arm in armatures:
            children = armature_children[arm]
            if not children:
                continue
                
            bpy.ops.object.select_all(action='DESELECT')
            
            arm.select_set(True)
            for child in children:
                child.select_set(True)
                
            # Also select all nested children
            for obj in bpy.data.objects:
                if is_armature_child(obj, arm):
                    obj.select_set(True)
                
            context.view_layer.objects.active = arm
            
            obj_path = os.path.join(directory, arm.name + ".fbx")
            
            try:
                bpy.ops.export_scene.fbx(
                    filepath=obj_path,
                    use_selection=True,
                    check_existing=False,
                    global_scale=1.0,
                    apply_scale_options='FBX_SCALE_NONE',
                    apply_unit_scale=True,
                    bake_space_transform=False,
                    object_types={'ARMATURE', 'MESH'},
                    use_mesh_modifiers=True,
                    mesh_smooth_type='FACE',
                    use_mesh_edges=False,
                    use_tspace=True,
                    use_custom_props=True,
                    add_leaf_bones=False,
                    primary_bone_axis='Y',
                    secondary_bone_axis='X',
                    use_armature_deform_only=False,
                    armature_nodetype='NULL',
                    bake_anim=True,
                    bake_anim_use_all_bones=True,
                    bake_anim_use_nla_strips=True,
                    bake_anim_use_all_actions=True,
                    bake_anim_force_startend_keying=True,
                    path_mode='COPY',
                    embed_textures=True,
                    batch_mode='OFF',
                    use_metadata=True,
                    axis_forward='-Z',
                    axis_up='Y',
                )
                exported_count += 1
                self.report({'INFO'}, f"Exported armature: {arm.name}")
            except Exception as e: self.report({'ERROR'}, f"Could not export armature {arm.name}\n{str(e)}")
        
        remaining_objs = [obj for obj in sel_objs if obj not in armatures and 
                         obj.parent not in armatures]
        
        for obj in remaining_objs:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            
            # Select all child objects recursively
            def select_children_recursive(parent_obj):
                for child in bpy.data.objects:
                    if child.parent == parent_obj:
                        child.select_set(True)
                        select_children_recursive(child)
            
            select_children_recursive(obj)
            
            context.view_layer.objects.active = obj
            
            has_animation = False
            if obj.type == 'MESH' and hasattr(obj.data, 'shape_keys') and obj.data.shape_keys:
                if obj.data.shape_keys.key_blocks and len(obj.data.shape_keys.key_blocks) > 0:
                    has_animation = True
            
            if obj.animation_data:
                if (obj.animation_data.action or 
                    (obj.animation_data.nla_tracks and len(obj.animation_data.nla_tracks) > 0)):
                    has_animation = True
            
            obj_path = os.path.join(directory, obj.name + ".fbx")
            
            try:
                bpy.ops.export_scene.fbx(
                    filepath=obj_path,
                    use_selection=True,
                    check_existing=False,
                    global_scale=1.0,
                    apply_scale_options='FBX_SCALE_NONE',
                    apply_unit_scale=True,
                    bake_space_transform=False,
                    object_types={'MESH', 'EMPTY', 'CAMERA', 'LIGHT'},
                    use_mesh_modifiers=True,
                    mesh_smooth_type='FACE',
                    use_mesh_edges=False,
                    use_tspace=True,
                    use_custom_props=True,
                    add_leaf_bones=False,
                    primary_bone_axis='Y',
                    secondary_bone_axis='X',
                    use_armature_deform_only=False,
                    armature_nodetype='NULL',
                    bake_anim=has_animation,
                    bake_anim_use_all_bones=has_animation,
                    bake_anim_use_nla_strips=has_animation,
                    bake_anim_use_all_actions=has_animation,
                    bake_anim_force_startend_keying=has_animation,
                    path_mode='COPY',
                    embed_textures=True,
                    batch_mode='OFF',
                    use_metadata=True,
                    axis_forward='-Z',
                    axis_up='Y',
                )
                exported_count += 1
            except Exception as e: self.report({'ERROR'}, f"Could not export object {obj.name}\n{str(e)}")
        
        context.scene.frame_set(current_frame)
        
        context.area.type = 'VIEW_3D'
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in sel_objs:
            obj.select_set(True)
        
        self.report({'INFO'}, f"{exported_count} objects were exported to {directory}")
        
        try:
            if platform.system() == "Windows":
                os.startfile(directory)
            elif platform.system() == "Darwin":
                subprocess.run(["open", directory])
            else:
                subprocess.run(["xdg-open", directory])
        except Exception as e: self.report({'WARNING'}, f"Could not open export directory: {str(e)}")
            
        return {'FINISHED'}

classes = (EXPORT_OT_operator,) 