import bpy
from .cleanup import beautify

modules_to_process = []

try:
    from . import base_panel
    modules_to_process.append(base_panel)
except ImportError as e:
    print(f"ERROR importing base_panel: {e}")

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
    # First register all operator modules
    modules_to_process.extend([
        origin_to_selected, center_origins, origin_to_bottom,
        align_to_view, align_objects, apply_modifiers, select_similar, checker_edge,
        select_bottom, select_similar_mesh
    ])
    modules_to_process.append(organize_panel)
except ImportError as e:
    print(f"ERROR importing organize modules: {e}")

# Import Cleanup Modules
try:
    from .cleanup import (
        cleanup_panel,
        clear_materials,
        generate_actions,
        clean_textures,
        rename_bones,
        select_similar_verts,
        fix_rotation
    )
    # First register all operator modules
    modules_to_process.extend([
        beautify, clear_materials, generate_actions,
        clean_textures, rename_bones, select_similar_verts, fix_rotation
    ])
    modules_to_process.append(cleanup_panel)
except ImportError as e:
    print(f"ERROR importing cleanup modules: {e}")

# Import Export Modules
try:
    from .export import (
        export_panel,
        export_fbx,
        export_glb
    )
    modules_to_process.extend([export_fbx, export_glb])
    modules_to_process.append(export_panel)
except ImportError as e:
    print(f"ERROR importing export modules: {e}")

# Import Support Modules
try:
    from .support import support_panel, support_links
    modules_to_process.append(support_links)
    modules_to_process.append(support_panel)
except ImportError as e:
    print(f"ERROR importing support modules: {e}")

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

_registered_classes = set()

def print_module_classes():
    """Helper function to debug which modules have classes attribute"""
    print("\n--- MODULE CLASS CHECK ---")
    for module in modules_to_process:
        module_name = module.__name__
        has_classes = hasattr(module, 'classes')
        class_count = len(module.classes) if has_classes else 0
        class_names = [cls.__name__ for cls in module.classes] if has_classes else []
        print(f"Module {module_name}: has_classes={has_classes}, count={class_count}, classes={class_names}")
    print("-------------------------\n")

def register():
    global _registered_classes
    _registered_classes.clear()
    
    for module in modules_to_process:
        module_name = module.__name__
        
        if hasattr(module, 'classes') and isinstance(module.classes, (list, tuple)):
            for cls in module.classes:
                if cls in _registered_classes:
                    continue
                class_name = cls.__name__
                try:
                    bpy.utils.register_class(cls)
                    _registered_classes.add(cls)
                except ValueError as ve:
                    _registered_classes.add(cls)
                except Exception as e:
                    print(f"ERROR registering class {class_name}: {str(e)}")

        if hasattr(module, 'register') and callable(module.register):
            if module_name != __name__:
                 try:
                     module.register()
                 except Exception as e:
                     print(f"ERROR in {module_name}.register(): {str(e)}")

        if hasattr(module, 'register_support_handlers') and callable(module.register_support_handlers):
             try:
                 module.register_support_handlers()
             except Exception as e:
                 print(f"ERROR in {module_name}.register_support_handlers(): {str(e)}")

def unregister():
    global _registered_classes
    modules_to_unregister = list(reversed(modules_to_process))
    
    for module in modules_to_unregister:
        module_name = module.__name__

        if hasattr(module, 'unregister') and callable(module.unregister):
            if module_name != __name__:
                try:
                    module.unregister()
                except Exception as e:
                    print(f"ERROR in {module_name}.unregister(): {str(e)}")
                    
        if hasattr(module, 'unregister_support_handlers') and callable(module.unregister_support_handlers):
            try:
                module.unregister_support_handlers()
            except Exception as e:
                print(f"ERROR in {module_name}.unregister_support_handlers(): {str(e)}")
        
        if hasattr(module, 'classes') and isinstance(module.classes, (list, tuple)):
            for cls in reversed(module.classes):
                if cls in _registered_classes:
                    class_name = cls.__name__
                    try:
                        bpy.utils.unregister_class(cls)
                        _registered_classes.remove(cls)
                    except RuntimeError:
                        if cls in _registered_classes: _registered_classes.remove(cls)
                    except Exception as e:
                        print(f"ERROR unregistering class {class_name}: {str(e)}")
    
    _registered_classes.clear() 