# This file makes 'export' a Python package

print("  Importing src.export submodules...")

try:
    from . import export_panel
except ImportError as e:
     print(f"    ERROR importing export_panel: {e}")

try:
    # from . import export_ops # <-- Commented out to break potential cycle
    from . import export_fbx
    from . import share_love
    print("    Imported export ops modules (excluding self-import check)." )
except ImportError as e:
     print(f"    ERROR importing export operator modules: {e}")

# Removed the 'classes' tuple definition - registration is handled by src/__init__.py
print(f"    Export __init__.py finished.") 