import bpy
from bpy.types import Panel
from .export_fbx import EXPORT_OT_operator
from .share_love import SHARE_OT_operator

class EXPORT_PT_panel(bpy.types.Panel):
    bl_label = "Export FBX"
    bl_idname = "ExportPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'TitlePanel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout 
        try:
            layout.separator()
            
            active_obj = context.active_object
            if active_obj and active_obj.type == 'MESH' and len(context.selected_objects) == 1:
                mesh_data = {
                    "verts": len(active_obj.data.vertices),
                    "mats": len(active_obj.material_slots) if active_obj.material_slots else 0,
                    "acts": len(active_obj.animation_data.nla_tracks) if active_obj.animation_data and active_obj.animation_data.nla_tracks else 0,
                    "keys": len(active_obj.data.shape_keys.key_blocks) if active_obj.data.shape_keys and active_obj.data.shape_keys.key_blocks else 0
                }
                
                row = layout.row()
                row.label(text=active_obj.name + " details", icon='INFO')
                
                row = layout.row()
                row.label(text=f"Verts: {mesh_data['verts']}")
                row.label(text=f"Mats: {mesh_data['mats']}")
                
                row = layout.row()
                row.label(text=f"Acts: {mesh_data['acts']}")
                row.label(text=f"Keys: {mesh_data['keys']}")
            elif len(context.selected_objects) > 1:
                row = layout.row()
                row.label(text="Multiple Objects", icon='INFO')

            row = layout.row()        
            row.operator("exportfbxxx.export", text=f"FBX Export {len(context.selected_objects)} Objects", icon='AUTO')
            row.enabled = len(context.selected_objects) > 0
            
        except Exception as e:
            print(f'Error in EXPORT_PT_panel: {str(e)}')

classes = (
    EXPORT_PT_panel,
) 