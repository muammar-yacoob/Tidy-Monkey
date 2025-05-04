import bpy
from bpy.types import Panel
from ..organize.organize_panel import ORG_FIXROTATION_OT_operator
from .fix_normals import FIX_NORMALS_OT_operator
from .clear_materials import CLEAR_MATS_OT_operator
from .generate_actions import GEN_ACTS_OT_operator
from .clean_textures import CLEAN_TEX_OT_operator
from .rename_bones import REN_BONES_OT_operator, RenameBonesProps
from .rename_vertex_groups import REN_VERT_OT_operator
from .clean_verts import CLEAN_VERTS_OT_operator

class CLEANUP_PT_panel(bpy.types.Panel):
    bl_label = "Clean Up"
    bl_idname = "CleanUp"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'TitlePanel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        in_edit_mode = context.active_object is not None and context.active_object.mode == 'EDIT'
        in_edit_mesh = context.mode == 'EDIT_MESH'
        in_edit_armature = context.mode == 'EDIT_ARMATURE'
        selection_count = len(context.selected_objects)
        
        try:
            if not in_edit_mode:
                row = layout.row()
                row.operator("fixnormals.fix", text=f"Fix Normals for {selection_count}", icon='NORMALS_FACE')
                row.enabled = context.active_object and context.active_object.type == 'MESH' and selection_count > 0
                
                row = layout.row()
                row.operator("clearmats.clear", text=f"Clear Unused Mats from {selection_count}", icon='NODE_MATERIAL')
                row.enabled = context.active_object and context.active_object.type == 'MESH' and selection_count > 0
                
                row = layout.row()
                row.operator("generate.actions", text="Generate Actions", icon='ARMATURE_DATA')
                
                row = layout.row()
                row.operator("deletetextures.delete", icon='RENDER_RESULT')
                row.enabled = context.active_object and context.active_object.type == 'MESH'
                
                has_armature = any(obj.type == 'ARMATURE' for obj in context.selected_objects)
                if has_armature:
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
                    op = row.operator("renamebones.rename", icon='BONE_DATA')
                    op.old_text = props.old_text
                    op.new_text = props.new_text
                    op.match_case = props.match_case
                
                row = layout.row()
                row.operator("renamevertgroups.rename", icon='GROUP_BONE')
                row.enabled = context.active_object and context.active_object.type == 'MESH' and selection_count > 0
            
            if in_edit_mesh:
                row = layout.row()
                row.operator("clean.verts", icon='STICKY_UVS_DISABLE')
                
            if in_edit_mesh or in_edit_armature:
                row = layout.row()
                row.operator("fix.rotation", text="Fix Rotation", icon='EMPTY_SINGLE_ARROW')
                
        except Exception as e:
            print(f'Error in CLEANUP_PT_panel: {str(e)}')

classes = (
    CLEANUP_PT_panel,
) 

def register():
    # Register property group
    bpy.types.Scene.rename_bones_props = bpy.props.PointerProperty(type=RenameBonesProps)

def unregister():
    # Unregister property group
    if hasattr(bpy.types.Scene, "rename_bones_props"):
        del bpy.types.Scene.rename_bones_props 