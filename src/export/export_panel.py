import bpy
from bpy.types import Panel
from ..export.export_fbx import EXPORT_OT_operator
from ..export.export_glb import EXPORT_GLB_OT_operator

class EXPORT_PT_panel(bpy.types.Panel):
    bl_label = "Export"
    bl_idname = "EXPORT_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'TITLE_PT_panel'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        return context.mode == 'OBJECT'

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
                
                box = layout.box()
                row = box.row()
                row.alignment = 'CENTER'
                row.label(text=active_obj.name + " details", icon='INFO')
                
                row = box.row()
                vert_text = f"Verts: {mesh_data['verts']:,}"
                if mesh_data['verts'] > 10000:
                    row.label(text=vert_text, icon='ERROR')
                else:
                    row.label(text=vert_text)
                    
                mat_text = f"Mats: {mesh_data['mats']}"
                if mesh_data['mats'] > 3:
                    row.label(text=mat_text, icon='ERROR')
                else:
                    row.label(text=mat_text)
                
                row = box.row()
                act_text = f"Acts: {mesh_data['acts']}"
                if mesh_data['acts'] > 10:
                    row.label(text=act_text, icon='ERROR')
                else:
                    row.label(text=act_text)
                    
                key_text = f"Keys: {mesh_data['keys']}"
                if mesh_data['keys'] > 10:
                    row.label(text=key_text, icon='ERROR')
                else:
                    row.label(text=key_text)
            elif len(context.selected_objects) > 1:
                row = layout.row()
                row.label(text="Multiple Objects", icon='INFO')

            row = layout.row()
            row.alignment = 'CENTER'
            row.label(text="EXPORT", icon='EXPORT')
            
            row = layout.row(align=True)
            row.operator(EXPORT_OT_operator.bl_idname, text=f"FBX Export ({len(context.selected_objects)})", icon='MESH_CUBE')
            row.enabled = len(context.selected_objects) > 0
            
            row = layout.row(align=True)
            row.operator(EXPORT_GLB_OT_operator.bl_idname, text=f"GLB Export ({len(context.selected_objects)})", icon='FACE_MAPS')
            row.enabled = len(context.selected_objects) > 0
            
        except Exception as e:
            pass

classes = (
    EXPORT_PT_panel,
) 