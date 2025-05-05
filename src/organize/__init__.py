# This file makes 'organize' a Python package
# It imports the necessary modules so they can be accessed via src.organize

print("  Importing src.organize submodules...")

try:
    from . import organize_panel
except ImportError as e:
     print(f"    ERROR importing organize_panel: {e}")

# Attempt to import operator modules - errors here might indicate deeper issues
# but we remove the direct dependency on organize_ops for the circular import
try:
    # from . import organize_ops # <-- Commented out to break potential cycle
    from . import origin_to_selected
    from . import center_origins
    from . import origin_to_bottom
    from . import align
    from . import fix_rotation
    from . import apply_modifiers
    from . import select_similar
    from . import checker_edge
    from . import select_bottom
    from . import select_similar_mesh
    print("    Imported organize ops modules (excluding self-import check)." )
except ImportError as e:
     print(f"    ERROR importing organize operator modules: {e}")

# Removed the 'classes' tuple definition - registration is handled by src/__init__.py
print(f"    Organize __init__.py finished.") 