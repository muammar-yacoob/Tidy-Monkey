import bpy
from bpy.types import Operator
import os
import platform
import subprocess

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class EXPORT_GLB_OT_operator(bpy.types.Operator):
    bl_idname = "exportglb.export"
    bl_label = "Export GLB"
    bl_description = "Exports selected objects as GLB files for web/game engines"

    def find_parent_armature(self, current_obj):
        p = current_obj.parent
        while p:
            if p.type == 'ARMATURE':
                return p
            p = p.parent
        return None

    def execute(self, context):
        if not bpy.data.filepath:
            self.report({'ERROR'}, "Please save your file first before exporting")
            return {'CANCELLED'}
            
        bpy.ops.object.mode_set(mode='OBJECT')
        
        blend_file_path = bpy.data.filepath
        directory = os.path.join(os.path.dirname(blend_file_path), "GLBs")
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        sel_objs = [obj for obj in context.selected_objects]
        if not sel_objs:
            self.report({'ERROR'}, "No objects selected to export")
            return {'CANCELLED'}
            
        original_active = context.view_layer.objects.active
        original_area_type = context.area.type
        
        bpy.ops.cleanup.cleantextures()
        bpy.ops.cleanup.clearmats()
        
        try:
            bpy.ops.cleanup.generateactions()
        except Exception as e:
            self.report({'INFO'}, "No actions to generate")
        
        # Apply modifiers to selected objects
        try:
            bpy.ops.organize.applymodifiers()
        except Exception as e:
            self.report({'INFO'}, "No modifiers to apply")
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in sel_objs:
            obj.select_set(True)
        if original_active:
            context.view_layer.objects.active = original_active
        
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
        context.scene.frame_set(context.scene.frame_start)
        
        exported_count = 0

        # Helper function for recursive selection
        def local_select_hierarchy_recursively(obj_root_select):
            obj_root_select.select_set(True)
            for child_obj_select in obj_root_select.children: # Iterate over direct children
                local_select_hierarchy_recursively(child_obj_select) # Recurse

        for s_obj in sel_objs: # Iterate over originally selected objects
            export_filename_stem = s_obj.name
            export_root_object = s_obj # Default: export the selected object itself

            if s_obj.type != 'ARMATURE':
                parent_arm = self.find_parent_armature(s_obj)
                if parent_arm:
                    export_root_object = parent_arm
            
            # Deselect all, then select the hierarchy for the current export target
            bpy.ops.object.select_all(action='DESELECT')
            
            local_select_hierarchy_recursively(export_root_object)
            context.view_layer.objects.active = export_root_object # Set active object
            
            obj_path = os.path.join(directory, export_filename_stem + ".glb")
            
            try:
                bpy.ops.export_scene.gltf(
                    filepath=obj_path,
                    export_format='GLB',
                    use_selection=True,
                    use_visible=True,
                    export_apply=True,
                    export_yup=True,
                    export_morph=True,
                    export_morph_normal=True,
                    export_morph_animation=True,
                    export_animations=True
                )
                exported_count += 1
                self.report({'INFO'}, f"Exported '{export_filename_stem}.glb' (using hierarchy from '{export_root_object.name}')")
            except Exception as e:
                self.report({'ERROR'}, f"Could not export '{export_filename_stem}.glb' (hierarchy from '{export_root_object.name}')\\n{str(e)}")
                
        context.scene.frame_set(current_frame)
        
        context.area.type = 'VIEW_3D'
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in sel_objs:
            obj.select_set(True)
            
        self.report({'INFO'}, f"{exported_count} objects were exported to {directory}")
        
        try:
            if platform.system() == "Windows":
                os.startfile(directory)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", directory])
            else:  # Linux and others
                subprocess.run(["xdg-open", directory])
        except Exception as e:
            self.report({'WARNING'}, f"Could not open export directory: {str(e)}")
            
        return {'FINISHED'}

classes = (EXPORT_GLB_OT_operator,) 