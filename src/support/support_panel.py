import bpy
from bpy.types import Panel
from ..support import support_links

class SUPPORT_PT_panel(bpy.types.Panel):
    bl_label = ""
    bl_idname = "SUPPORT_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'TITLE_PT_panel'
    bl_options = {'HIDE_HEADER'}
    bl_order = 100
    
    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        try:
            box = layout.box()
            support_links.create_support_section(box)
        except Exception as e:
            pass

classes = (
    SUPPORT_PT_panel,
) 