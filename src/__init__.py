from . import base_panel
from .organize import organize_panel
from .cleanup import cleanup_panel
from .export import export_panel
from .support import support_panel

from bpy.types import PropertyGroup
import bpy

classes = (
    *base_panel.classes,
    *organize_panel.classes,
    *cleanup_panel.classes,
    *export_panel.classes,
    *support_panel.classes
)

def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            print(f"Failed to register panel {cls.__name__}: {str(e)}")
            
    cleanup_panel.register()

def unregister():
    cleanup_panel.unregister()
    
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception as e:
            print(f"Failed to unregister panel {cls.__name__}: {str(e)}") 