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
                    row = layout.row()
                    row.alignment = 'LEFT'
                    row.label(text=f"Mode: {mode}", icon='OBJECT_DATA')
                elif mode == 'EDIT':
                    row = layout.row()
                    row.alignment = 'LEFT'
                    edit_row = row.row()
                    edit_row.alert = True
                    edit_row.label(text=f"Mode: {mode}", icon='EDITMODE_HLT')
                elif mode == 'POSE':
                    row = layout.row()
                    row.alignment = 'LEFT'
                    row.label(text=f"Mode: {mode}", icon='ARMATURE_DATA')
                else:
                    row = layout.row()
                    row.alignment = 'LEFT'
                    row.label(text=f"Mode: {mode}")
            except:
                row = layout.row()
                row.alignment = 'LEFT'
                row.label(text="Mode: ERROR")
        else:
            row = layout.row()
            row.alignment = 'LEFT'
            row.label(text="Mode: N/A", icon='ERROR')

classes = (TITLE_PT_panel,) 