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
            
        armatures = [obj for obj in sel_objs if obj.type == 'ARMATURE']
        armature_children = {}
        
        for arm in armatures:
            armature_children[arm] = [obj for obj in bpy.data.objects 
                                     if obj.parent == arm and obj.type == 'MESH']
        
        # Store original selection state
        original_active = context.view_layer.objects.active
        
        # Call cleanup operators once before export
        bpy.ops.cleanup.cleantextures()
        bpy.ops.cleanup.clearmats()
        
        # Generate actions from animations
        try:
            bpy.ops.cleanup.generateactions()
        except Exception as e:
            self.report({'INFO'}, "No actions to generate")
        
        # Apply modifiers to selected objects
        try:
            bpy.ops.organize.applymodifiers()
        except Exception as e:
            self.report({'INFO'}, "No modifiers to apply")
        
        # Re-select all objects
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
            
            obj_path = os.path.join(directory, arm.name + ".glb")
            
            try:
                # Use minimal set of parameters to avoid compatibility issues
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
                self.report({'INFO'}, f"Exported armature: {arm.name}")
            except Exception as e:
                self.report({'ERROR'}, f"Could not export armature {arm.name}\n{str(e)}")
            
        remaining_objs = [obj for obj in sel_objs if obj not in armatures and 
                         obj.parent not in armatures]
                         
        for obj in remaining_objs:
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            has_morph = False
            if obj.type == 'MESH' and hasattr(obj.data, 'shape_keys') and obj.data.shape_keys:
                if obj.data.shape_keys.key_blocks:
                    has_morph = len(obj.data.shape_keys.key_blocks) > 0
                    
            obj_path = os.path.join(directory, obj.name + ".glb")
            
            try:
                # Use minimal set of parameters to avoid compatibility issues
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
            except Exception as e:
                self.report({'ERROR'}, f"Could not export object {obj.name}\n{str(e)}")
                
        context.scene.frame_set(current_frame)
        bpy.ops.object.select_all(action='DESELECT')
        for obj in sel_objs:
            obj.select_set(True)
            
        self.report({'INFO'}, f"{exported_count} objects were exported to {directory}")
        
        # Cross-platform directory opening
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