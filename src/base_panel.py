import bpy
from bpy.types import Panel

class TITLE_PT_panel(bpy.types.Panel):
    bl_label = "Tidy Monkey"
    bl_idname = "TitlePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tidy Monkey'
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        try: 
            mode = context.active_object.mode
            if mode == 'OBJECT':
                row.label(text="Mode: ", icon='OBJECT_DATA')
                row.label(text=mode, icon_value=0)
                row.label(text="", icon='CHECKMARK')
            elif mode == 'EDIT':
                row.label(text="Mode: ", icon='EDITMODE_HLT')
                row.label(text=mode, icon_value=0)
                row.label(text="", icon='ERROR')
            elif mode == 'POSE':
                row.label(text="Mode: ", icon='ARMATURE_DATA')
                row.label(text=mode, icon_value=0)
                row.label(text="", icon='MOD_OCEAN')
            else:
                row.label(text=f"Mode: {mode}")
        except:
            row.label(text="Mode: N/A")

classes = (TITLE_PT_panel,) 