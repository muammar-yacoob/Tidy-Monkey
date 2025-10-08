import bpy
from bpy.types import Panel
from ..export.export_glb import EXPORT_GLB_OT_operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class EXPORT_PT_panel(Panel):
    bl_label = "Export"
    bl_idname = "VIEW3D_PT_tidy_monkey_export_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tidy Monkey"
    
    def draw(self, context):
        layout = self.layout
        
        # Get the number of selected objects
        selection_count = len(context.selected_objects)
        
        # Show warning if no objects are selected
        if selection_count == 0:
            row = layout.row()
            row.alert = True
            row.label(text="No objects selected", icon='ERROR')
            return
        
        # Show warning if non-mesh objects are selected
        non_mesh_selected = False
        for obj in context.selected_objects:
            if obj.type != 'MESH':
                non_mesh_selected = True
                break
        
        if non_mesh_selected:
            row = layout.row()
            row.alert = True
            row.label(text="Warning: Non-mesh objects selected", icon='ERROR')
        
        # Export buttons
        box = layout.box()
        col = box.column(align=True)
        
        # GLB Export
        row = col.row(align=True)
        if selection_count > 1:
            row.operator(EXPORT_GLB_OT_operator.bl_idname, text=f"GLB Export ({selection_count})", icon='MESH_CUBE')
        else:
            row.operator(EXPORT_GLB_OT_operator.bl_idname, text="GLB Export", icon='MESH_CUBE')

classes = [
    EXPORT_PT_panel
]

def register():
    """Register the export panel class."""
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            # If already registered, try to unregister first
            try:
                bpy.utils.unregister_class(cls)
                bpy.utils.register_class(cls)
            except Exception as e2:
                print(f"Failed to register {cls.__name__}: {str(e2)}")

def unregister():
    """Unregister the export panel class."""
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception as e:
            print(f"Failed to unregister {cls.__name__}: {str(e)}") 