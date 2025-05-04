import bpy
import traceback

# --- Module Collection --- 
modules_to_register = []

print("Tidy Monkey: src/__init__.py - Starting module discovery")

try:
    from . import base_panel
    modules_to_register.append(base_panel)
    print("  Found: base_panel")
except ImportError as e:
    print(f"  ERROR importing base_panel: {e}")
    traceback.print_exc()

try:
    from .organize import organize_panel, organize_ops
    modules_to_register.append(organize_panel)
    modules_to_register.append(organize_ops)
    print("  Found: organize_panel, organize_ops")
except ImportError as e:
    print(f"  ERROR importing organize modules: {e}")
    traceback.print_exc()

try:
    from .cleanup import cleanup_panel, cleanup_ops
    modules_to_register.append(cleanup_panel)
    modules_to_register.append(cleanup_ops)
    print("  Found: cleanup_panel, cleanup_ops")
except ImportError as e:
    print(f"  ERROR importing cleanup modules: {e}")
    traceback.print_exc()

try:
    from .export import export_panel, export_ops
    modules_to_register.append(export_panel)
    modules_to_register.append(export_ops)
    print("  Found: export_panel, export_ops")
except ImportError as e:
    print(f"  ERROR importing export modules: {e}")
    traceback.print_exc()

try:
    from .support import support_panel, support_links
    modules_to_register.append(support_panel)
    modules_to_register.append(support_links)
    print("  Found: support_panel, support_links")
except ImportError as e:
    print(f"  ERROR importing support modules: {e}")
    traceback.print_exc()

print(f"Tidy Monkey: src/__init__.py - Found {len(modules_to_register)} modules to potentially register classes from.")

# --- Registration Function --- 
def register():
    print("\n--- Tidy Monkey: src.register() called ---")
    registered_classes = []
    
    for module in modules_to_register:
        module_name = module.__name__
        print(f"  Processing module: {module_name}")
        if hasattr(module, 'classes') and isinstance(module.classes, (list, tuple)):
            print(f"    Found {len(module.classes)} classes in {module_name}.classes")
            for cls in module.classes:
                class_name = cls.__name__
                try:
                    if cls not in registered_classes:
                        print(f"      Attempting to register: {class_name}")
                        bpy.utils.register_class(cls)
                        registered_classes.append(cls)
                        print(f"      SUCCESS: Registered {class_name}")
                    else:
                        print(f"      INFO: Class {class_name} already registered, skipping.")
                except Exception as e:
                    print(f"      ERROR registering class {class_name} from {module_name}: {e}")
                    traceback.print_exc()
        else:
            print(f"    INFO: Module {module_name} does not have a 'classes' list/tuple.")
            
        # Handle module-specific registration functions (like cleanup_panel, support_links)
        if hasattr(module, 'register') and callable(module.register):
            try:
                # Avoid calling the main src.register recursively
                if module_name != __name__:
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
                 
    print(f"--- Tidy Monkey: src.register() finished. Total classes registered in this call: {len(registered_classes)} ---")

# --- Unregistration Function --- 
def unregister():
    print("\n--- Tidy Monkey: src.unregister() called ---")
    unregistered_classes_count = 0
    modules_to_unregister = list(reversed(modules_to_register)) # Process in reverse
    
    for module in modules_to_unregister:
        module_name = module.__name__
        print(f"  Processing module for unregistration: {module_name}")
        
        # Handle module-specific unregistration functions first
        if hasattr(module, 'unregister') and callable(module.unregister):
            try:
                # Avoid calling the main src.unregister recursively
                if module_name != __name__:
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
        
        # Unregister classes from the module
        if hasattr(module, 'classes') and isinstance(module.classes, (list, tuple)):
            print(f"    Found {len(module.classes)} classes in {module_name}.classes to unregister")
            for cls in reversed(module.classes): # Unregister classes in reverse order too
                class_name = cls.__name__
                try:
                    print(f"      Attempting to unregister: {class_name}")
                    bpy.utils.unregister_class(cls)
                    unregistered_classes_count += 1
                    print(f"      SUCCESS: Unregistered {class_name}")
                except RuntimeError as e:
                     # Catch runtime errors which often indicate the class wasn't registered
                     print(f"      INFO: Could not unregister {class_name} (may not have been registered): {e}")
                except Exception as e:
                    print(f"      ERROR unregistering class {class_name} from {module_name}: {e}")
                    traceback.print_exc()
        else:
             print(f"    INFO: Module {module_name} does not have a 'classes' list/tuple.")
             
    print(f"--- Tidy Monkey: src.unregister() finished. Total classes unregistered in this call: {unregistered_classes_count} ---") 