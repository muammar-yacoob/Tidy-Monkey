# This file makes 'organize' a Python package
# It imports the necessary modules so they can be accessed via src.organize

import bpy

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

print("  Importing src.organize submodules...")

try:
    from . import organize_panel
except ImportError as e:
     print(f"    ERROR importing organize_panel: {e}")

try:
    from . import origin_to_selected
    from . import center_origins
    from . import origin_to_bottom
    from . import align_to_view
    from . import align_objects
    from . import apply_modifiers
    from . import select_similar
    from . import checker_edge
    from . import select_bottom
    from . import select_similar_mesh
    from . import space_objects
    print("    Imported organize ops modules (excluding self-import check)." )
except ImportError as e:
     print(f"    ERROR importing organize operator modules: {e}")

print(f"    Organize __init__.py finished.") 