import bpy
from . import src

# Add bl_info for Blender's addon system (for backward compatibility)
bl_info = {
    "name": "Tidy Monkey",
    "author": "Spark Games",
    "description": "Scene Organization Tool for Artists and Game Developers",
    "blender": (4, 0, 0),
    "version": (2, 0, 0),
    "location": "View3D > Sidebar > Tidy Monkey",
    "warning": "",
    "doc_url": "https://spark-games.co.uk",
    "category": "Scene Organization"
}

class TIDYMONKEY_PT_MinimalPanel(bpy.types.Panel):
    bl_label = "Tidy Monkey"
    bl_idname = "TIDYMONKEY_PT_minimal_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tidy Monkey"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Tidy Monkey is ready!")
        layout.label(text="Version 2.0")

def register():
    print("Registering Tidy Monkey - Starting")
    try:
        bpy.utils.register_class(TIDYMONKEY_PT_MinimalPanel)
        src.register()
        print("Tidy Monkey - Registration Complete")
    except Exception as e:
        print(f"Tidy Monkey - Error during registration: {str(e)}")
    
def unregister():
    print("Unregistering Tidy Monkey - Starting")
    try:
        src.unregister()
        bpy.utils.unregister_class(TIDYMONKEY_PT_MinimalPanel)
        print("Tidy Monkey - Unregistration Complete")
    except Exception as e:
        print(f"Tidy Monkey - Error during unregistration: {str(e)}")

# Register this module directly for testing as an extension
if __name__ == "__main__":
    register() 