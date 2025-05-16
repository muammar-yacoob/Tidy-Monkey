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

    def find_parent_armature(self, current_obj):
        p = current_obj.parent
        while p:
            if p.type == 'ARMATURE':
                return p
            p = p.parent
        return None

    def local_select_hierarchy_recursively(self, obj_root_select):
        obj_root_select.select_set(True)
        for child_obj_select in obj_root_select.children:
            self.local_select_hierarchy_recursively(child_obj_select)

    def execute(self, context):
        if not bpy.data.filepath:
            self.report({'ERROR'}, "Please save your file first before exporting")
            return {'CANCELLED'}
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        blend_file_path = bpy.data.filepath
        directory = os.path.join(os.path.dirname(blend_file_path), "FBXs")
        if not os.path.exists(directory): os.makedirs(directory, exist_ok=True)

        sel_objs = [obj for obj in context.selected_objects]
        if not sel_objs:
            self.report({'ERROR'}, "No objects selected to export")
            return {'CANCELLED'}
        
        original_active = context.view_layer.objects.active
        
        bpy.ops.cleanup.cleantextures()
        bpy.ops.cleanup.clearmats()
        
        try: bpy.ops.cleanup.generateactions()
        except Exception: self.report({'INFO'}, "No actions to generate")
        
        try: bpy.ops.organize.applymodifiers()
        except Exception: self.report({'INFO'}, "No modifiers to apply or organize addon not found")

        bpy.ops.object.select_all(action='DESELECT')
        for obj in sel_objs: obj.select_set(True)
        if original_active and original_active.name in context.view_layer.objects: context.view_layer.objects.active = original_active
        
        try: bpy.ops.file.pack_all()
        except Exception as e: self.report({'WARNING'}, f"Could not pack all textures: {str(e)}")
        
        try:
            bpy.ops.file.unpack_all(method='USE_LOCAL')
            bpy.ops.file.make_paths_absolute()
        except Exception: self.report({'WARNING'}, "Error processing textures (unpack/make_paths_absolute)")
        
        current_frame = context.scene.frame_current
        context.scene.frame_set(context.scene.frame_start)
        
        exported_count = 0

        fbx_export_settings = {
            'check_existing': False,
            'global_scale': 1.0,
            'apply_scale_options': 'FBX_SCALE_UNITS', 
            'apply_unit_scale': True,
            'bake_space_transform': True, 
            'use_mesh_modifiers': True,
            'mesh_smooth_type': 'FACE',
            'use_mesh_edges': False,
            'use_tspace': True,
            'use_custom_props': True,
            'add_leaf_bones': False,
            'primary_bone_axis': 'Y',
            'secondary_bone_axis': 'X',
            'use_armature_deform_only': True,
            'armature_nodetype': 'NULL',
            'bake_anim': True,
            'bake_anim_use_all_bones': True,
            'bake_anim_use_nla_strips': True,
            'bake_anim_use_all_actions': True,
            'bake_anim_force_startend_keying': True,
            'path_mode': 'COPY',
            'embed_textures': True,
            'batch_mode': 'OFF',
            'use_metadata': True,
            'axis_forward': '-Z',
            'axis_up': 'Y',
        }

        for s_obj in sel_objs:
            export_filename_stem = s_obj.name
            export_root_object = s_obj

            if s_obj.type != 'ARMATURE':
                parent_arm = self.find_parent_armature(s_obj)
                if parent_arm:
                    export_root_object = parent_arm
            
            bpy.ops.object.select_all(action='DESELECT')
            
            original_locations = {}
            
            
            self.local_select_hierarchy_recursively(export_root_object)
            if export_root_object and export_root_object.name in context.view_layer.objects: # Ensure object is in current view layer
                 context.view_layer.objects.active = export_root_object
            
            current_selection_for_export = [obj for obj in context.selected_objects] # Capture current selection
            for obj_in_hierarchy in current_selection_for_export:
                original_locations[obj_in_hierarchy] = obj_in_hierarchy.location.copy()
                obj_in_hierarchy.location = (0, 0, 0)

            obj_path = os.path.join(directory, export_filename_stem + ".fbx")
            
            object_types_to_export = {'ARMATURE', 'MESH'}
            
            try:
                bpy.ops.export_scene.fbx(
                    filepath=obj_path,
                    use_selection=True,
                    object_types=object_types_to_export,
                    **fbx_export_settings
                )
                exported_count += 1
                self.report({'INFO'}, f"Exported '{export_filename_stem}.fbx' (hierarchy from '{export_root_object.name}')")
            except Exception as e: self.report({'ERROR'}, f"Could not export '{export_filename_stem}.fbx' (hierarchy from '{export_root_object.name}')\n{str(e)}")
            finally:
                for obj_in_hierarchy, loc in original_locations.items():
                    if obj_in_hierarchy and obj_in_hierarchy.name in bpy.data.objects: obj_in_hierarchy.location = loc
        
        context.scene.frame_set(current_frame)
        
        if hasattr(context.area, 'type'): context.area.type = 'VIEW_3D'
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in sel_objs:
            if obj and obj.name in bpy.data.objects: obj.select_set(True)
        if original_active and original_active.name in bpy.data.objects: context.view_layer.objects.active = original_active
            
        self.report({'INFO'}, f"{exported_count} FBX files were exported to {directory}")
        
        try:
            if platform.system() == "Windows": os.startfile(directory)
            elif platform.system() == "Darwin": subprocess.run(["open", directory], check=True)
            else: subprocess.run(["xdg-open", directory], check=True)
        except Exception as e: self.report({'WARNING'}, f"Could not open export directory: {str(e)}")
            
        return {'FINISHED'}

classes = (EXPORT_OT_operator,)

def register():
    bpy.utils.register_class(EXPORT_OT_operator)

def unregister():
    bpy.utils.unregister_class(EXPORT_OT_operator)

if __name__ == "__main__":
    register() 