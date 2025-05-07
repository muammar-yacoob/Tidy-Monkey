import bpy
from bpy.types import Panel

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class TITLE_PT_panel(bpy.types.Panel):
    bl_label = "Tidy Monkey"
    bl_idname = "TITLE_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tidy Monkey'
    
    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        
        if context.active_object:
            try: 
                mode = context.active_object.mode
                if mode == 'OBJECT':
                    row = layout.row(align=True)
                    row.alignment = 'LEFT'
                    row.label(text="Mode:", icon='OBJECT_DATA')
                    row.label(text=mode)
                elif mode == 'EDIT':
                    row = layout.row(align=True)
                    row.alignment = 'LEFT'
                    row.label(text="Mode:", icon='EDITMODE_HLT')
                    edit_label = row.row()
                    edit_label.alert = True
                    edit_label.label(text=mode)
                elif mode == 'POSE':
                    row = layout.row(align=True)
                    row.alignment = 'LEFT'
                    row.label(text="Mode:", icon='ARMATURE_DATA')
                    row.label(text=mode)
                else:
                    row = layout.row(align=True)
                    row.alignment = 'LEFT'
                    row.label(text=f"Mode:{mode}")
            except:
                row = layout.row(align=True)
                row.alignment = 'LEFT'
                row.label(text="Mode:ERROR")
        else:
            row = layout.row(align=True)
            row.alignment = 'LEFT'
            row.label(text="Mode:N/A", icon='ERROR')

classes = (TITLE_PT_panel,) 