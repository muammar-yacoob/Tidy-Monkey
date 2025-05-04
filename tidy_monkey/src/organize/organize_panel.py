import bpy
from bpy.types import Panel
from .origin_to_selected import ORG_SELECTED_OT_operator
from .center_origins import ORG_CENTER_OT_operator
from .origin_to_bottom import ORG_BOTTOMCENTER_OT_operator
from .align import ORG_ALIGNTOVIEW_OT_operator, ALIGN_OT_operator
from .fix_rotation import ORG_FIXROTATION_OT_operator
from .apply_modifiers import APPLY_MODS_OT_operator
from .select_similar import (
    SELECT_SIMILAR_OT_operator, 
    SELECT_MAT_OT_operator, 
    SELECT_PER_OT_operator,
    SELECT_NORM_OT_operator,
    SELECT_AREA_OT_operator,
    SELECT_COPLANAR_OT_operator
)
from .checker_edge import CHECKER_EDGE_OT_operator
from .select_bottom import BUTTS_OT_operator
from .select_similar_mesh import SELECT_SAME_OT_operator

class ORGANIZE_PT_panel(bpy.types.Panel):
    bl_label = "Organize"
    bl_idname = "OrganizePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'TitlePanel'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        in_object_mode = context.active_object is not None and context.active_object.mode == 'OBJECT'
        in_edit_mode = context.active_object is not None and context.active_object.mode == 'EDIT'
        selection_count = len(context.selected_objects)

        try:
            row = layout.row()
            row.operator("origin.toselected", icon='CLIPUV_HLT')
            row.enabled = in_edit_mode
            
            if not in_edit_mode:
                row = layout.row()
                row.operator("align.toview", text="Align to View", icon='ORIENTATION_GIMBAL')
                row.enabled = in_object_mode and selection_count == 1
            
            if in_edit_mode:
                box = layout.box()
                box.label(text="Selection Tools")
                
                row = box.row()
                row.operator("bottoms.select", text="Select Bottom", icon='TRIA_DOWN_BAR')
                
                row = box.row()
                row.operator("material.select", icon='RESTRICT_SELECT_OFF')
                
                row = box.row()
                row.operator("perimeter.select", icon='RESTRICT_SELECT_OFF')
                
                row = box.row()
                row.operator("checker.edge", icon='ALIGN_JUSTIFY')
            
            if not in_edit_mode and in_object_mode:
                row = layout.row()
                row.operator("centerregions.center", 
                            text=f"Center Origins of {selection_count}", 
                            icon='ANCHOR_CENTER')
                row.enabled = selection_count > 0
                
                row = layout.row()
                row.operator("origin.tobottomcenter", text="Origin to Bottom Center", icon='ANCHOR_BOTTOM')
                row.enabled = selection_count > 0
                
                row = layout.row()
                row.operator("samemesh.similar", icon='MOD_MESHDEFORM')
                row.enabled = context.active_object.type == 'MESH' and selection_count == 1
                
                row = layout.row()
                row.operator("apply.mods", icon='MODIFIER_DATA', 
                           text=f"Apply Modifiers for {selection_count}")
                row.enabled = context.active_object.type == 'MESH' and selection_count > 0
                
                col = layout.column(align=True)
                row = col.row(align=True)
                row.operator("alignobjects.align", text="X").algn = 'X'
                row.operator("alignobjects.align", text="Y").algn = 'Y'
                row.operator("alignobjects.align", text="Z").algn = 'Z'
                row.enabled = selection_count > 1
        except Exception as e:
            print(f'Error in ORGANIZE_PT_panel: {str(e)}')

classes = (ORGANIZE_PT_panel,) 