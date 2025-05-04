bl_info = {
    "name": "Tidy Monkey",
    "author": "Spark Games",
    "description": "Scene Organization Tool",
    "blender": (4, 4, 0),
    "version": (2, 0, 0),
    "location": "View3D > Sidebar > Tidy Monkey",
    "warning": "For the Export FBX to work, make sure you save the .blend file first",
    "doc_url": "https://spark-games.co.uk",
    "category": "Scene Organization"
}

#https://blendermarket.com/products/tidy-monkey

#region Imports
import bpy
from . tdmk_pt import *
from . tdmk_op import *
from . support_links import register_support_handlers, unregister_support_handlers
#endregion

#region Registration
classes = (
    RenameBonesProps,
    TITLE_PT_panel,
    ORGANIZE_PT_panel,
    CLEANUP_PT_panel,
    EXPORT_PT_panel,
    SUPPORT_PT_panel,
    ORG_SELECTED_OT_operator,
    ORG_ALIGNTOVIEW_OT_operator,
    ORG_CENTER_OT_operator,
    ORG_BOTTOMCENTER_OT_operator,
    BUTTS_OT_operator,
    ALIGN_OT_operator,
    REN_BONES_OT_operator,
    REN_VERT_OT_operator,
    SELECT_SAME_OT_operator,
    CLEAR_MATS_OT_operator,
    CLEAN_TEX_OT_operator,
    GEN_ACTS_OT_operator,
    EXPORT_OT_operator,
    SHARE_OT_operator,
    ORG_FIXROTATION_OT_operator,
    FIX_NORMALS_OT_operator,
    SELECT_MAT_OT_operator,
    SELECT_PER_OT_operator,
    SELECT_NORM_OT_operator,
    SELECT_AREA_OT_operator,
    SELECT_COPLANAR_OT_operator,
    CHECKER_EDGE_OT_operator,
    CLEAN_VERTS_OT_operator,
    APPLY_MODS_OT_operator
)

def register():
    for cls in classes:
        try:
            bpy.utils.register_class(cls)
        except Exception as e:
            print(f"Failed to register {cls.__name__}: {str(e)}")
            
    bpy.types.Scene.rename_bones_props = bpy.props.PointerProperty(type=RenameBonesProps)
    
    # Register support handlers
    register_support_handlers()

def unregister():
    # Unregister support handlers
    unregister_support_handlers()
    
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except Exception as e:
            print(f"Failed to unregister {cls.__name__}: {str(e)}")
            
    if hasattr(bpy.types.Scene, "rename_bones_props"):
        del bpy.types.Scene.rename_bones_props

#register, unregister = bpy.utils.register_classes_factory(classes)
    
if __name__ == "__main__":
    register()
#endregion