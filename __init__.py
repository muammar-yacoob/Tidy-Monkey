bl_info = {
    "name": "Tidy Monkey",
    "author": "Spark Games",
    "description": "Scene Organization Tool",
    "blender": (4, 4, 0),
    "version": (2, 0, 0),
    "location": "View3D > Sidebar > Tidy Monkey",
    "doc_url": "https://spark-games.co.uk",
    "category": "Scene Organization"
}

#https://blendermarket.com/products/tidy-monkey

#region Imports
# Keep imports minimal here to reduce risk of load-time errors
try:
    import bpy
    import traceback
except Exception as e:
    # This is unlikely but critical if it fails
    raise e 
#endregion

#region Registration
# Root module delegates registration to the src module.

# These functions are required by Blender 4.x extension system
def __register__():
    register()

def __unregister__():
    unregister()

def register():
    try:
        # Import and call src register dynamically
        from . import src
        # Check if src has a register function before calling
        if hasattr(src, 'register') and callable(src.register):
            src.register()
        else:
             pass
    except ImportError as e:
        pass
    except Exception as e:
        pass

def unregister():
    try:
        # Import and call src unregister dynamically
        from . import src
         # Check if src has an unregister function before calling
        if hasattr(src, 'unregister') and callable(src.unregister):
            src.unregister()
        else:
             pass
    except ImportError as e:
        pass
    except Exception as e:
        pass
    
if __name__ == "__main__":
    # This part should ideally not run when installed as an addon
    # Attempt registration for standalone testing, might fail without full Blender context
    try:
        register()
    except Exception as e:
        pass

#endregion