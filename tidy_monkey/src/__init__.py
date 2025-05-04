from . import base_panel
from .organize import organize_panel
from .cleanup import cleanup_panel
from .export import export_panel
from .support import support_panel
from .support import support_links

from bpy.types import PropertyGroup
import bpy

classes = (
    *base_panel.classes,
    *organize_panel.classes,
    *cleanup_panel.classes,
    *export_panel.classes,
    *support_panel.classes,
    *support_links.classes
)

def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            print(f"Failed to register class {cls.__name__}: {str(e)}")
            
    cleanup_panel.register()
    support_links.register_support_handlers()

def unregister():
    support_links.unregister_support_handlers()
    cleanup_panel.unregister()
    
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception as e:
            print(f"Failed to unregister class {cls.__name__}: {str(e)}") 