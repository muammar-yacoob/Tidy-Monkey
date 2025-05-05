import bpy
from bpy.types import Panel
from ..support import support_links
from ..export.share_love import SHARE_OT_operator

class SUPPORT_PT_panel(bpy.types.Panel):
    bl_label = "Support"
    bl_idname = "TIDYMONKEY_PT_Support"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'TIDYMONKEY_PT_Base'
    bl_options = {'DEFAULT_CLOSED'}
    bl_order = 10
    
    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        try:
            box = layout.box()
            row = box.row()
            row.label(text="Share the Love")
            
            row.operator(SHARE_OT_operator.bl_idname, text="", icon='COMMUNITY').shareType = 'YT'
            row.operator(SHARE_OT_operator.bl_idname, text="", icon='FUND').shareType = 'WB'
            
            support_links.create_support_section(layout)
        except Exception as e:
            print(f'Error in SUPPORT_PT_panel draw method: {str(e)}')

classes = (
    SUPPORT_PT_panel,
) 