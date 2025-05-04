import bpy
from . import src
from .src.support.support_links import register_support_handlers, unregister_support_handlers

def register():
    src.register()
    
    register_support_handlers()

def unregister():
    unregister_support_handlers()
    
    src.unregister()

__all__ = ["register", "unregister"] 