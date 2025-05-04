import bpy
import traceback

# --- Module Imports --- 
print("Tidy Monkey: src/__init__.py - Importing submodules...")
modules_to_process = []

try:
    from . import base_panel
    modules_to_process.append(base_panel)
    print("  Imported: base_panel")
except ImportError as e:
    print(f"  ERROR importing base_panel: {e}")
    traceback.print_exc()

try:
    from .organize import organize_panel, organize_ops
    modules_to_process.append(organize_panel)
    modules_to_process.append(organize_ops)
    print("  Imported: organize_panel, organize_ops")
except ImportError as e:
    print(f"  ERROR importing organize modules: {e}")
    traceback.print_exc()

try:
    from .cleanup import cleanup_panel, cleanup_ops
    modules_to_process.append(cleanup_panel)
    modules_to_process.append(cleanup_ops)
    print("  Imported: cleanup_panel, cleanup_ops")
except ImportError as e:
    print(f"  ERROR importing cleanup modules: {e}")
    traceback.print_exc()

try:
    from .export import export_panel, export_ops
    modules_to_process.append(export_panel)
    modules_to_process.append(export_ops)
    print("  Imported: export_panel, export_ops")
except ImportError as e:
    print(f"  ERROR importing export modules: {e}")
    traceback.print_exc()

try:
    from .support import support_panel, support_links
    modules_to_process.append(support_panel)
    modules_to_process.append(support_links)
    print("  Imported: support_panel, support_links")
except ImportError as e:
    print(f"  ERROR importing support modules: {e}")
    traceback.print_exc()

print(f"Tidy Monkey: src/__init__.py - Finished importing. {len(modules_to_process)} module references collected.")

# Keep track of classes registered by this module to prevent duplicate registration attempts
_registered_classes = set()

# --- Registration Function --- 
def register():
    global _registered_classes
    _registered_classes.clear() # Clear on re-registration
    print("\n--- Tidy Monkey: src.register() called ---")
    
    for module in modules_to_process:
        module_name = module.__name__
        print(f"  Processing module for registration: {module_name}")
        
        # Register classes from the module's 'classes' tuple/list
        if hasattr(module, 'classes') and isinstance(module.classes, (list, tuple)):
            print(f"    Found {len(module.classes)} classes in {module_name}.classes")
            for cls in module.classes:
                if cls in _registered_classes:
                    print(f"      INFO: Class {cls.__name__} already registered by src, skipping.")
                    continue
                class_name = cls.__name__
                try:
                    print(f"      Attempting to register: {class_name}")
                    bpy.utils.register_class(cls)
                    _registered_classes.add(cls) # Track registered class
                    print(f"      SUCCESS: Registered {class_name}")
                except ValueError:
                    # This often means it was already registered by Blender elsewhere or a previous run
                    print(f"      INFO: Class {class_name} is likely already registered. Skipping.")
                    _registered_classes.add(cls) # Assume it's registered
                except Exception as e:
                    print(f"      ERROR registering class {class_name} from {module_name}: {e}")
                    traceback.print_exc()
        else:
            print(f"    INFO: Module {module_name} does not have a 'classes' attribute.")

        # Handle module-specific registration functions
        if hasattr(module, 'register') and callable(module.register):
            # Avoid calling this register function recursively
            if module_name != __name__:
                 try:
                     print(f"    Calling {module_name}.register()...")
                     module.register()
                     print(f"    SUCCESS: Called {module_name}.register()")
                 except Exception as e:
                     print(f"    ERROR calling {module_name}.register(): {e}")
                     traceback.print_exc()
                     
        if hasattr(module, 'register_support_handlers') and callable(module.register_support_handlers):
             try:
                 print(f"    Calling {module_name}.register_support_handlers()...")
                 module.register_support_handlers()
                 print(f"    SUCCESS: Called {module_name}.register_support_handlers()")
             except Exception as e:
                 print(f"    ERROR calling {module_name}.register_support_handlers(): {e}")
                 traceback.print_exc()
                 
    print(f"--- Tidy Monkey: src.register() finished. Registered {_registered_classes} classes in this session. ---")

# --- Unregistration Function --- 
def unregister():
    global _registered_classes
    print("\n--- Tidy Monkey: src.unregister() called ---")
    modules_to_unregister = list(reversed(modules_to_process))
    
    for module in modules_to_unregister:
        module_name = module.__name__
        print(f"  Processing module for unregistration: {module_name}")

        # Handle module-specific unregistration functions first
        if hasattr(module, 'unregister') and callable(module.unregister):
            if module_name != __name__:
                try:
                    print(f"    Calling {module_name}.unregister()...")
                    module.unregister()
                    print(f"    SUCCESS: Called {module_name}.unregister()")
                except Exception as e:
                    print(f"    ERROR calling {module_name}.unregister(): {e}")
                    traceback.print_exc()
                    
        if hasattr(module, 'unregister_support_handlers') and callable(module.unregister_support_handlers):
            try:
                print(f"    Calling {module_name}.unregister_support_handlers()...")
                module.unregister_support_handlers()
                print(f"    SUCCESS: Called {module_name}.unregister_support_handlers()")
            except Exception as e:
                print(f"    ERROR calling {module_name}.unregister_support_handlers(): {e}")
                traceback.print_exc()
        
        # Unregister classes from the module's 'classes' tuple/list
        if hasattr(module, 'classes') and isinstance(module.classes, (list, tuple)):
            print(f"    Found {len(module.classes)} classes in {module_name}.classes to unregister")
            for cls in reversed(module.classes): # Unregister in reverse order
                if cls in _registered_classes:
                    class_name = cls.__name__
                    try:
                        print(f"      Attempting to unregister: {class_name}")
                        bpy.utils.unregister_class(cls)
                        _registered_classes.remove(cls) # Untrack
                        print(f"      SUCCESS: Unregistered {class_name}")
                    except RuntimeError:
                         print(f"      INFO: Could not unregister {class_name} (already unregistered?).")
                         if cls in _registered_classes: _registered_classes.remove(cls)
                    except Exception as e:
                        print(f"      ERROR unregistering class {class_name} from {module_name}: {e}")
                        traceback.print_exc()
                else:
                    # This class wasn't registered by this module in this session, potentially already unregistered or never registered
                    print(f"      INFO: Skipping unregistration of {cls.__name__} (not tracked as registered by src)." )
        else:
             print(f"    INFO: Module {module_name} does not have a 'classes' attribute.")
             
    print(f"--- Tidy Monkey: src.unregister() finished. Remaining tracked classes (should be 0): {len(_registered_classes)} ---")
    _registered_classes.clear() # Ensure clear even if errors happened 