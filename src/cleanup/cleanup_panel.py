import bpy
from bpy.types import Panel, PropertyGroup
import bpy.props
import bmesh

from .beautify import BEAUTIFY_OT_operator
from ..cleanup.clear_materials import CLEAR_MATS_OT_operator
from ..cleanup.generate_actions import GEN_ACTS_OT_operator
from ..cleanup.clean_textures import CLEAN_TEX_OT_operator
from ..cleanup.rename_bones import REN_BONES_OT_operator, RenameBonesProps
from .clean_verts import CLEAN_VERTS_OT_operator
from ..cleanup.fix_rotation import FIXROTATION_OT_operator
from ..base_panel import TITLE_PT_panel

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class CLEANUP_PT_panel(bpy.types.Panel):
    bl_label = "Clean Up"
    bl_idname = "CLEANUP_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = TITLE_PT_panel.bl_idname
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        in_edit_mode = context.active_object is not None and context.active_object.mode == 'EDIT'
        in_edit_mesh = context.mode == 'EDIT_MESH'
        in_edit_armature = context.mode == 'EDIT_ARMATURE'
        selection_count = len(context.selected_objects)
        
        try:
            if not in_edit_mode:
                selected_mesh_count = len([obj for obj in context.selected_objects if obj.type == 'MESH'])
                
                box = layout.box()
                # box.label(text="Mesh Cleanup")
                
                row = box.row()
                if selected_mesh_count > 1: row.operator("cleanup.beautify", text=f"Beautify ({selected_mesh_count})", icon='SHADERFX')
                else: row.operator("cleanup.beautify", text="Beautify", icon='SHADERFX')
                row.enabled = selected_mesh_count > 0
                
                row = box.row()
                if selection_count > 1: row.operator("cleanup.clearmats", text=f"Clear Materials ({selection_count})", icon='NODE_MATERIAL')
                else: row.operator("cleanup.clearmats", text="Clear Materials", icon='NODE_MATERIAL')
                row.enabled = context.active_object and context.active_object.type == 'MESH' and selection_count > 0
            
                row = box.row()
                row.operator("cleanup.cleantextures", icon='RENDER_RESULT')
                row.enabled = context.active_object and context.active_object.type == 'MESH'
                
                row = layout.row()
                row.operator("cleanup.generateactions", text="Generate Actions", icon='ARMATURE_DATA')
                
                has_armature = any(obj.type == 'ARMATURE' for obj in context.selected_objects)
                if has_armature and hasattr(context.scene, "rename_bones_props"):
                    box = layout.box()
                    box.label(text="Rename Bones")
                    props = context.scene.rename_bones_props
                    
                    row = box.row()
                    row.prop(props, "old_text")
                    
                    row = box.row()
                    row.prop(props, "new_text")
                    
                    row = box.row()
                    row.prop(props, "match_case")
                    
                    row = box.row()
                    op = row.operator("cleanup.renamebones", icon='BONE_DATA')
                    if props:
                        op.old_text = props.old_text
                        op.new_text = props.new_text
                        op.match_case = props.match_case
                elif has_armature:
                     layout.label(text="Rename Bones properties not registered.", icon='ERROR')
            
            if in_edit_mesh:
                edit_box = layout.box()
                # edit_box.label(text=  "Edit Mode Tools")
                
                row = edit_box.row()
                row.operator("cleanup.cleanverts", icon='STICKY_UVS_DISABLE')
                
                if in_edit_mesh or in_edit_armature:
                    row = edit_box.row()
                    op = row.operator("cleanup.fixrotation", text="Fix Rotation", icon='EMPTY_SINGLE_ARROW')
                    
                    if in_edit_mesh:
                        obj = context.edit_object
                        if obj and obj.type == 'MESH':
                            mesh = bmesh.from_edit_mesh(obj.data)
                            
                            if context.tool_settings.mesh_select_mode[2]: row.enabled = any(f.select for f in mesh.faces)  # Face mode
                            elif context.tool_settings.mesh_select_mode[1]: row.enabled = any(e.select for e in mesh.edges)  # Edge mode
                            elif context.tool_settings.mesh_select_mode[0]: row.enabled = any(v.select for v in mesh.verts)  # Vertex mode
                            else: row.enabled = False
                        else: row.enabled = False
            elif in_edit_armature:
                edit_box = layout.box()
                edit_box.label(text="Edit Mode Tools")
                
                row = edit_box.row()
                op = row.operator("cleanup.fixrotation", text="Fix Rotation", icon='EMPTY_SINGLE_ARROW')
            
        except Exception as e:
            pass

classes = (
    CLEANUP_PT_panel,
    RenameBonesProps
)

def register():
    try:
        bpy.types.Scene.rename_bones_props = bpy.props.PointerProperty(type=RenameBonesProps)
    except Exception as e:
        pass

def unregister():
    try:
        if hasattr(bpy.types.Scene, "rename_bones_props"):
            del bpy.types.Scene.rename_bones_props
    except Exception as e:
        pass 