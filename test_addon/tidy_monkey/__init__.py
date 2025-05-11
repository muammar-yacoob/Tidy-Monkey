import bpy

# Simple panel class for testing
class TIDYMONKEY_PT_panel(bpy.types.Panel):
    bl_label = "Tidy Monkey Test"
    bl_idname = "TIDYMONKEY_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Tidy Monkey Test Addon")

# Registration functions
classes = (TIDYMONKEY_PT_panel,)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    print("Tidy Monkey Test: Registered successfully!")

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    print("Tidy Monkey Test: Unregistered successfully!")

if __name__ == "__main__":
    register() 