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
# Simple test panel to ensure visibility
class TIDYMONKEY_TEST_PT_panel(bpy.types.Panel):
    bl_label = "Tidy Monkey Test"
    bl_idname = "TIDYMONKEY_TEST_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tidy Monkey"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Tidy Monkey Test Panel")
        layout.label(text="If you see this, the addon is working!")

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
    try:
        # Register the test panel directly
        print("  Attempting to register TIDYMONKEY_TEST_PT_panel...")
        bpy.utils.register_class(TIDYMONKEY_TEST_PT_panel)
        print("  SUCCESS: TIDYMONKEY_TEST_PT_panel registered.")
        
        # Import and call src register
        print("  Attempting to import and call src.register...")
        try:
            from .src import register as src_register
            print("    Imported src.register successfully.")
            src_register()
            print("    Called src.register successfully.")
        except ImportError as e:
            print(f"    ERROR importing src module: {e}")
            traceback.print_exc()
        except Exception as e:
            print(f"    ERROR calling src.register: {e}")
            traceback.print_exc()
            
        print("Tidy Monkey: Root register() finished.")
    except Exception as e:
        print(f"Tidy Monkey - FATAL ERROR during root registration: {e}")
        traceback.print_exc()

def unregister():
    print("Tidy Monkey: Root unregister() function started.")
    try:
        # Import and call src unregister
        print("  Attempting to import and call src.unregister...")
        try:
            from .src import unregister as src_unregister
            print("    Imported src.unregister successfully.")
            src_unregister()
            print("    Called src.unregister successfully.")
        except ImportError as e:
            print(f"    ERROR importing src module: {e}")
            traceback.print_exc()
        except Exception as e:
            print(f"    ERROR calling src.unregister: {e}")
            traceback.print_exc()

        # Unregister the test panel
        print("  Attempting to unregister TIDYMONKEY_TEST_PT_panel...")
        try:
            bpy.utils.unregister_class(TIDYMONKEY_TEST_PT_panel)
            print("  SUCCESS: TIDYMONKEY_TEST_PT_panel unregistered.")
        except Exception as e:
            print(f"    ERROR unregistering test panel: {e}")
            traceback.print_exc()
            
        print("Tidy Monkey: Root unregister() finished.")
    except Exception as e:
        print(f"Tidy Monkey - FATAL ERROR during root unregistration: {e}")
        traceback.print_exc()
    
if __name__ == "__main__":
    print("\n--- Tidy Monkey: Running as main script ---")
    register()
#endregion