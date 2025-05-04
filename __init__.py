bl_info = {
    "name": "Tidy Monkey",
    "author": "Spark Games",
    "description": "Scene Organization Tool",
    "blender": (4, 0, 0),
    "version": (2, 0, 0),
    "location": "View3D > Sidebar > Tidy Monkey",
    "warning": "For the Export FBX to work, make sure you save the .blend file first",
    "doc_url": "https://spark-games.co.uk",
    "category": "Scene Organization"
}

#https://blendermarket.com/products/tidy-monkey

#region Imports
import bpy
from . import src
from .src.support.support_links import register_support_handlers, unregister_support_handlers
#endregion

#region Registration
def register():
    src.register()
    
    register_support_handlers()

def unregister():
    unregister_support_handlers()
    
    src.unregister()

__register__ = register
__unregister__ = unregister

if __name__ == "__main__":
    register()
#endregion