import bpy
from bpy.types import Panel
from ..organize.origin_to_selected import ORG_SELECTED_OT_operator
from ..organize.center_origins import ORG_CENTER_OT_operator
from ..organize.origin_to_bottom import ORG_BOTTOMCENTER_OT_operator
from ..organize.align import ORG_ALIGNTOVIEW_OT_operator, ALIGN_OT_operator
from ..organize.apply_modifiers import APPLY_MODS_OT_operator
from ..organize.select_similar import (
    SELECT_MAT_OT_operator, 
    SELECT_PER_OT_operator
)
from ..organize.checker_edge import CHECKER_EDGE_OT_operator
from ..organize.select_bottom import BUTTS_OT_operator
from ..organize.select_similar_mesh import SELECT_SAME_OT_operator

class ORGANIZE_PT_panel(bpy.types.Panel):
    bl_label = "Organize"
    bl_idname = "ORGANIZE_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'TITLE_PT_panel'
    
    def draw(self, context):
        layout = self.layout
        in_object_mode = context.active_object is not None and context.active_object.mode == 'OBJECT'
        in_edit_mode = context.active_object is not None and context.active_object.mode == 'EDIT'
        selection_count = len(context.selected_objects)

        try:
            if in_edit_mode:
                row = layout.row()
                row.operator(ORG_SELECTED_OT_operator.bl_idname, icon='PIVOT_CURSOR')
            
            if not in_edit_mode:
                row = layout.row()
                row.operator(ORG_ALIGNTOVIEW_OT_operator.bl_idname, text="Align to View", icon='ORIENTATION_GIMBAL')
                row.enabled = in_object_mode and selection_count == 1
            
            if in_edit_mode:
                box = layout.box()
                box.label(text="Selection Tools")
                
                row = box.row()
                row.operator(BUTTS_OT_operator.bl_idname, text="Select Bottom", icon='TRIA_DOWN_BAR')
                
                row = box.row()
                row.operator(SELECT_MAT_OT_operator.bl_idname, icon='RESTRICT_SELECT_OFF')
                
                row = box.row()
                row.operator(SELECT_PER_OT_operator.bl_idname, icon='RESTRICT_SELECT_OFF')
                
                row = box.row()
                row.operator(CHECKER_EDGE_OT_operator.bl_idname, icon='ALIGN_JUSTIFY')
            
            if not in_edit_mode and in_object_mode:
                row = layout.row()
                
                center_label = "Center Origin" if selection_count == 1 else f"Center Origins of {selection_count}"
                row.operator(ORG_CENTER_OT_operator.bl_idname, 
                            text=center_label, 
                            icon='ANCHOR_CENTER')
                row.enabled = selection_count > 0
                
                row = layout.row()
                bottom_label = "Origin to Bottom" if selection_count == 1 else f"Origin to Bottom for {selection_count}"
                row.operator(ORG_BOTTOMCENTER_OT_operator.bl_idname, text=bottom_label, icon='ANCHOR_BOTTOM')
                row.enabled = selection_count > 0
                
                row = layout.row()
                row.operator(SELECT_SAME_OT_operator.bl_idname, icon='MOD_MESHDEFORM')
                row.enabled = context.active_object.type == 'MESH' and selection_count == 1
                
                row = layout.row()
                
                modifier_label = "Apply Modifiers" if selection_count == 1 else f"Apply Modifiers for {selection_count}"
                row.operator(APPLY_MODS_OT_operator.bl_idname, icon='MODIFIER_DATA', 
                           text=modifier_label)
                row.enabled = context.active_object.type == 'MESH' and selection_count > 0
                
                col = layout.column(align=True)
                row = col.row(align=True)
                row.operator(ALIGN_OT_operator.bl_idname, text="X").algn = 'X'
                row.operator(ALIGN_OT_operator.bl_idname, text="Y").algn = 'Y'
                row.operator(ALIGN_OT_operator.bl_idname, text="Z").algn = 'Z'
                row.enabled = selection_count > 1
        except Exception as e:
            pass

classes = (ORGANIZE_PT_panel,) 