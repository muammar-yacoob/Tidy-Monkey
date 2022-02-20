bl_info = {
    "name" : "Tidy Monkey",
    "author" : "Muammar Yacoob",
    "descrtion" : "Scene Organization Tool",
    "blender" : (3, 0, 0),
    "version" : (1, 4, 0),
    "location" : "Tidy Monkey",
    "warning" : "For the Export FBX to work, make sure you save the .blend file first",   
    "category" : "Scene Organization"
}
#https://panettonegames.com/
#https://blendermarket.com/products/tidy-monkey

#region Registeration
classes = (TITLE_PT_panel, ORGANIZE_PT_panel, CLEANUP_PT_panel, EXPORT_PT_panel, ORG_SELECTED_OT_operator, ORG_ALIGNTOVIEW_OT_operator, ORG_CENTER_OT_operator, BUTTS_OT_operator, ALIGN_OT_operator, REN_BONES_OT_operator,REN_VERT_OT_operator, SELECT_SAME_OT_operator, CLEAR_MATS_OT_operator, CLEAN_TEX_OT_operator, GEN_ACTS_OT_operator, EXPORT_OT_operator, SHARE_OT_operator,ORG_FIXROTATION_OT_operator, FIX_NORMALS_OT_operator,SELECT_MAT_OT_operator,SELECT_PER_OT_operator,SELECT_NORM_OT_operator,SELECT_AREA_OT_operator,SELECT_COPLANAR_OT_operator,CHECKER_EDGE_OT_operator,CLEAN_VERTS_OT_operator,APPLY_MODS_OT_operator)

register, unregister = bpy.utils.register_classes_factory(classes)
    
if __name__ == "__main__":
    register()
#endregion