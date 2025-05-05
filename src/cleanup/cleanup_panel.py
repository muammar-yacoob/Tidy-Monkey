import bpy
from bpy.types import Panel, PropertyGroup
import bpy.props

from ..cleanup.fix_normals import FIX_NORMALS_OT_operator
from ..cleanup.clear_materials import CLEAR_MATS_OT_operator
from ..cleanup.generate_actions import GEN_ACTS_OT_operator
from ..cleanup.clean_textures import CLEAN_TEX_OT_operator
from ..cleanup.rename_bones import REN_BONES_OT_operator, RenameBonesProps
from ..cleanup.rename_vertex_groups import REN_VERT_OT_operator
from ..cleanup.clean_verts import CLEAN_VERTS_OT_operator
from ..organize.fix_rotation import ORG_FIXROTATION_OT_operator

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
                row.operator(FIX_NORMALS_OT_operator.bl_idname, text=f"Fix Normals for {selection_count}", icon='NORMALS_FACE')
                row.enabled = context.active_object and context.active_object.type == 'MESH' and selection_count > 0
                
                row = layout.row()
                row.operator(CLEAR_MATS_OT_operator.bl_idname, text=f"Clear Unused Mats from {selection_count}", icon='NODE_MATERIAL')
                row.enabled = context.active_object and context.active_object.type == 'MESH' and selection_count > 0
                
                row = layout.row()
                row.operator(GEN_ACTS_OT_operator.bl_idname, text="Generate Actions", icon='ARMATURE_DATA')
                
                row = layout.row()
                row.operator(CLEAN_TEX_OT_operator.bl_idname, icon='RENDER_RESULT')
                row.enabled = context.active_object and context.active_object.type == 'MESH'
                
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
                    op = row.operator(REN_BONES_OT_operator.bl_idname, icon='BONE_DATA')
                    if props:
                        op.old_text = props.old_text
                        op.new_text = props.new_text
                        op.match_case = props.match_case
                elif has_armature:
                     layout.label(text="Rename Bones properties not registered.", icon='ERROR')
                
                row = layout.row()
                row.operator(REN_VERT_OT_operator.bl_idname, icon='GROUP_BONE')
                row.enabled = context.active_object and context.active_object.type == 'MESH' and selection_count > 0
            
            if in_edit_mesh:
                row = layout.row()
                row.operator(CLEAN_VERTS_OT_operator.bl_idname, icon='STICKY_UVS_DISABLE')
                
            if in_edit_mesh or in_edit_armature:
                row = layout.row()
                row.operator(ORG_FIXROTATION_OT_operator.bl_idname, text="Fix Rotation", icon='EMPTY_SINGLE_ARROW')
                
        except Exception as e:
            print(f'Error in CLEANUP_PT_panel draw method: {str(e)}')

classes = (
    CLEANUP_PT_panel,
    RenameBonesProps
)

def register():
    try:
        print("  Attempting to register Scene.rename_bones_props from cleanup_panel...")
        bpy.types.Scene.rename_bones_props = bpy.props.PointerProperty(type=RenameBonesProps)
        print("  SUCCESS: Registered Scene.rename_bones_props")
    except Exception as e:
        print(f"  ERROR registering Scene.rename_bones_props in cleanup_panel: {e}")

def unregister():
    try:
        if hasattr(bpy.types.Scene, "rename_bones_props"):
            print("  Attempting to unregister Scene.rename_bones_props from cleanup_panel...")
            del bpy.types.Scene.rename_bones_props
            print("  SUCCESS: Unregistered Scene.rename_bones_props")
    except Exception as e:
        print(f"  ERROR unregistering Scene.rename_bones_props in cleanup_panel: {e}") 