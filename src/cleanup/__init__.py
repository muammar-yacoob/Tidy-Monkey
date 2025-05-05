# This file makes 'cleanup' a Python package

print("  Importing src.cleanup submodules...")

try:
    from . import cleanup_panel
except ImportError as e:
     print(f"    ERROR importing cleanup_panel: {e}")

try:
    # from . import cleanup_ops # <-- Commented out to break potential cycle
    from . import fix_normals
    from . import clear_materials
    from . import generate_actions
    from . import clean_textures
    from . import rename_bones
    from . import rename_vertex_groups
    from . import clean_verts
    print("    Imported cleanup ops modules (excluding self-import check)." )
except ImportError as e:
     print(f"    ERROR importing cleanup operator modules: {e}")

# Removed the 'classes' tuple definition - registration is handled by src/__init__.py
print(f"    Cleanup __init__.py finished.")

# Keep register/unregister ONLY if rename_bones NEEDS them for PropertyGroups
# Ensure these don't cause cycles themselves
def register():
    # Ensure rename_bones was imported before trying to use its register
    if 'rename_bones' in locals() and hasattr(rename_bones, 'register'):
        print("    Calling rename_bones.register() from cleanup/__init__")
        rename_bones.register()
    else:
        print("    ERROR: Could not call rename_bones.register() in cleanup/__init__")

def unregister():
    if 'rename_bones' in locals() and hasattr(rename_bones, 'unregister'):
        print("    Calling rename_bones.unregister() from cleanup/__init__")
        rename_bones.unregister()
    else:
        print("    ERROR: Could not call rename_bones.unregister() in cleanup/__init__") 