bl_info = {
    "name": "Tidy Monkey",
    "author": "Spark Games",
    "description": "Scene Organization Tool",
    "blender": (4, 4, 0),
    "version": (2, 0, 0),
    "location": "View3D > Sidebar > Tidy Monkey",
    "warning": "For the Export FBX to work, make sure you save the .blend file first",
    "doc_url": "https://spark-games.co.uk",
    "category": "Scene Organization"
}

#https://blendermarket.com/products/tidy-monkey

#region Imports
import bpy
import traceback
#endregion

#region Registration
# Root module delegates registration to the src module.

# These functions are required by Blender 4.x extension system
def __register__():
    print("\n--- Tidy Monkey: Root __register__ called ---")
    register()
    print("--- Tidy Monkey: Root __register__ finished ---")

def __unregister__():
    print("\n--- Tidy Monkey: Root __unregister__ called ---")
    unregister()
    print("--- Tidy Monkey: Root __unregister__ finished ---")

def register():
    print("Tidy Monkey: Root register() function started.")
    print("  Delegating registration to src module...")
    try:
        # Import and call src register dynamically
        from . import src
        # Check if src has a register function before calling
        if hasattr(src, 'register') and callable(src.register):
            print("    Imported src module successfully.")
            src.register()
            print("    Called src.register successfully.")
            print("Tidy Monkey: Root register() finished successfully.")
        else:
             print("    ERROR: src module found, but does not have a callable register() function.")
    except ImportError as e:
        print(f"    FATAL ERROR importing src module: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"    FATAL ERROR during registration delegation: {e}")
        traceback.print_exc()

def unregister():
    print("Tidy Monkey: Root unregister() function started.")
    print("  Delegating unregistration to src module...")
    try:
        # Import and call src unregister dynamically
        from . import src
         # Check if src has an unregister function before calling
        if hasattr(src, 'unregister') and callable(src.unregister):
            print("    Imported src module successfully.")
            src.unregister()
            print("    Called src.unregister successfully.")
            print("Tidy Monkey: Root unregister() finished successfully.")
        else:
             print("    ERROR: src module found, but does not have a callable unregister() function.")
    except ImportError as e:
        print(f"    FATAL ERROR importing src module: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"    FATAL ERROR during unregistration delegation: {e}")
        traceback.print_exc()
    
if __name__ == "__main__":
    # This part should ideally not run when installed as an addon
    print("\n--- Tidy Monkey: Running as main script (should not happen in addon mode) ---")
    # Attempt registration for standalone testing, might fail without full Blender context
    try:
        register()
    except Exception as e:
        print(f"Error running register() in __main__: {e}")
#endregion