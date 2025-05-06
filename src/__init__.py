import bpy
import traceback

from .cleanup import fix_rotation

modules_to_process = []

try:
    from . import base_panel
    modules_to_process.append(base_panel)
except ImportError as e:
    pass

# Import Organize Modules
try:
    from .organize import (
        organize_panel,
        origin_to_selected,
        center_origins,
        origin_to_bottom,
        align,
        align_to_view,
        align_objects,
        apply_modifiers,
        select_similar,
        checker_edge,
        select_bottom,
        select_similar_mesh
    )
    modules_to_process.extend([
        organize_panel, origin_to_selected, center_origins, origin_to_bottom,
        align, align_to_view, align_objects, fix_rotation, apply_modifiers, select_similar, checker_edge,
        select_bottom, select_similar_mesh
    ])
except ImportError as e:
    pass

# Import Cleanup Modules
try:
    from .cleanup import (
        cleanup_panel,
        fix_normals,
        clear_materials,
        generate_actions,
        clean_textures,
        rename_bones,
        clean_verts
    )
    modules_to_process.extend([
        cleanup_panel, fix_normals, clear_materials, generate_actions,
        clean_textures, rename_bones, clean_verts
    ])
except ImportError as e:
    pass

# Import Export Modules
try:
    from .export import (
        export_panel,
        export_fbx,
        export_glb
    )
    modules_to_process.extend([export_panel, export_fbx, export_glb])
except ImportError as e:
    pass

# Import Support Modules
try:
    from .support import support_panel, support_links
    modules_to_process.extend([support_panel, support_links])
except ImportError as e:
    pass

_registered_classes = set()

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
                except ValueError:
                    _registered_classes.add(cls)
                except Exception as e:
                    pass

        if hasattr(module, 'register') and callable(module.register):
            if module_name != __name__:
                 try:
                     module.register()
                 except Exception as e:
                     pass
                     
        if hasattr(module, 'register_support_handlers') and callable(module.register_support_handlers):
             try:
                 module.register_support_handlers()
             except Exception as e:
                 pass

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
                    pass
                    
        if hasattr(module, 'unregister_support_handlers') and callable(module.unregister_support_handlers):
            try:
                module.unregister_support_handlers()
            except Exception as e:
                pass
        
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
                        pass
             
    _registered_classes.clear() 