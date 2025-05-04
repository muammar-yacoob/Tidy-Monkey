import bpy
from . import src

class TIDYMONKEY_PT_MinimalPanel(bpy.types.Panel):
    bl_label = "Tidy Monkey"
    bl_idname = "TIDYMONKEY_PT_minimal_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tidy Monkey"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Tidy Monkey is ready!")

def register():
    print("Registering Tidy Monkey")
    bpy.utils.register_class(TIDYMONKEY_PT_MinimalPanel)
    src.register()
    
def unregister():
    print("Unregistering Tidy Monkey")
    src.unregister()
    bpy.utils.unregister_class(TIDYMONKEY_PT_MinimalPanel)

if __name__ == "__main__":
    register() 