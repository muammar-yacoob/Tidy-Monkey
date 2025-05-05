import bpy
from bpy.types import Panel
from ..support import support_links
from ..export.share_love import SHARE_OT_operator

class SUPPORT_PT_panel(bpy.types.Panel):
    bl_label = "Support"
    bl_idname = "SUPPORT_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'TITLE_PT_panel'
    bl_options = {}
    bl_order = 10
    
    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        try:
            box = layout.box()
            support_links.create_support_section(box)
            
            row = box.row(align=True)
            row.scale_y = 1.0
            row.operator(SHARE_OT_operator.bl_idname, text="YouTube", icon='URL').shareType = 'YT'
            row.operator(SHARE_OT_operator.bl_idname, text="Website", icon='WORLD').shareType = 'WB'
        except Exception as e:
            pass

classes = (
    SUPPORT_PT_panel,
) 