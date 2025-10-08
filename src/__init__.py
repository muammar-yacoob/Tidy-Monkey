import bpy
from .cleanup import beautify, clean_verts

ENABLE_SUPPORT_PANEL = False

modules_to_process = []

# Import preferences first
try:
    from . import ai_preferences
    modules_to_process.append(ai_preferences)
except ImportError:
    pass

try:
    from . import base_panel
    modules_to_process.append(base_panel)
except ImportError:
    pass

# Import Organize Modules
try:
    from .organize import (
        organize_panel,
        origin_to_selected,
        center_origins,
        origin_to_bottom,
        align_to_view,
        align_objects,
        apply_modifiers,
        select_similar,
        checker_edge,
        select_bottom,
        select_similar_mesh
    )
    # Register operator modules first
    modules_to_process.extend([
        origin_to_selected, center_origins, origin_to_bottom,
        align_to_view, align_objects, apply_modifiers, select_similar, checker_edge,
        select_bottom, select_similar_mesh
    ])
    modules_to_process.append(organize_panel)
except ImportError:
    pass

# Import Cleanup Modules
try:
    from .cleanup import (
        cleanup_panel,
        clear_materials,
        generate_actions,
        clean_textures,
        rename_bones,
        fix_rotation
    )
    # Register operator modules first
    modules_to_process.extend([
        beautify, clear_materials, generate_actions,
        clean_textures, rename_bones, clean_verts, fix_rotation
    ])
    modules_to_process.append(cleanup_panel)
except ImportError:
    pass

# Import Export Modules
try:
    from .export import (
        export_panel,
        export_glb
    )
    modules_to_process.extend([export_glb])
    modules_to_process.append(export_panel)
except ImportError:
    pass

# Import Support Modules
if ENABLE_SUPPORT_PANEL:
    try:
        from .support import support_panel, support_links
        modules_to_process.append(support_links)
        modules_to_process.append(support_panel)
    except ImportError:
        pass

# Import AI Modules
try:
    from .ai import (
        ai_modeling,
        ai_animation,
        ai_lighting,
        ai_panel
    )
    # Register operator modules first
    modules_to_process.extend([ai_modeling, ai_animation, ai_lighting])
    modules_to_process.append(ai_panel)
except ImportError as e:
    print(f"AI modules not available: {e}")
    pass

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

_registered_classes = set()

def register():
    """Register all addon classes and modules."""
    global _registered_classes
    _registered_classes.clear()
    
    for module in modules_to_process:
        # Register classes
        if hasattr(module, 'classes') and isinstance(module.classes, (list, tuple)):
            for cls in module.classes:
                if cls not in _registered_classes:
                    try:
                        bpy.utils.register_class(cls)
                        _registered_classes.add(cls)
                    except (ValueError, RuntimeError):
                        # Class already registered or other registration error
                        _registered_classes.add(cls)

        # Call module register function
        if hasattr(module, 'register') and callable(module.register):
            try:
                module.register()
            except Exception as e:
                print(f"Error registering {module.__name__}: {str(e)}")

        # Register support handlers if available
        if hasattr(module, 'register_support_handlers') and callable(module.register_support_handlers):
            try:
                module.register_support_handlers()
            except Exception as e:
                print(f"Error registering support handlers for {module.__name__}: {str(e)}")

def unregister():
    """Unregister all addon classes and modules."""
    global _registered_classes
    
    # Unregister in reverse order
    for module in reversed(modules_to_process):
        # Call module unregister function
        if hasattr(module, 'unregister') and callable(module.unregister):
            try:
                module.unregister()
            except Exception as e:
                print(f"Error unregistering {module.__name__}: {str(e)}")
                    
        # Unregister support handlers if available
        if hasattr(module, 'unregister_support_handlers') and callable(module.unregister_support_handlers):
            try:
                module.unregister_support_handlers()
            except Exception:
                pass
        
        # Unregister classes
        if hasattr(module, 'classes') and isinstance(module.classes, (list, tuple)):
            for cls in reversed(module.classes):
                if cls in _registered_classes:
                    try:
                        bpy.utils.unregister_class(cls)
                        _registered_classes.remove(cls)
                    except Exception:
                        if cls in _registered_classes:
                            _registered_classes.remove(cls)
    
    _registered_classes.clear()

# These functions are required by Blender 4.x extension system
def __register__():
    register()

def __unregister__():
    unregister()

if __name__ == "__main__":
    register() 