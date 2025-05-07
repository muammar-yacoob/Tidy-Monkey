import bpy

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

print("  Importing src.export submodules...")

try:
    from . import export_panel
except ImportError as e:
     print(f"    ERROR importing export_panel: {e}")

try:
    from . import export_fbx
    from . import export_glb
    print("    Imported export ops modules (excluding self-import check)." )
except ImportError as e:
     print(f"    ERROR importing export operator modules: {e}")

print(f"    Export __init__.py finished.") 