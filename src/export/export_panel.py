import bpy
from bpy.types import Panel
from ..export.export_fbx import EXPORT_OT_operator
from ..export.export_glb import EXPORT_GLB_OT_operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

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
                
                try:
                    row = layout.row()
                    row.label(text=active_obj.name + " details", icon='INFO')
                    
                    box = layout.box()
                except Exception as e:
                    print(f"Error displaying mesh details: {e}")
                    box = layout.box()
                
                row = box.row()
                # Verts column
                split = row.split(factor=0.5)
                col1 = split.column()
                if mesh_data['verts'] > 10000:
                    col1.alert = True
                    col1.label(text=f"Verts: {mesh_data['verts']:,}")
                else:
                    col1.label(text=f"Verts: {mesh_data['verts']:,}")
                
                # Mats column
                col2 = split.column()
                if mesh_data['mats'] > 3:
                    col2.alert = True
                    col2.label(text=f"Mats: {mesh_data['mats']}")
                else:
                    col2.label(text=f"Mats: {mesh_data['mats']}")
                
                row = box.row()
                # Acts column
                split = row.split(factor=0.5)
                col1 = split.column()
                if mesh_data['acts'] > 10:
                    col1.alert = True
                    col1.label(text=f"Acts: {mesh_data['acts']}")
                else:
                    col1.label(text=f"Acts: {mesh_data['acts']}")
                
                # Keys column
                col2 = split.column()
                if mesh_data['keys'] > 10:
                    col2.alert = True
                    col2.label(text=f"Keys: {mesh_data['keys']}")
                else:
                    col2.label(text=f"Keys: {mesh_data['keys']}")
            elif len(context.selected_objects) > 1:
                row = layout.row()
                row.label(text="Multiple Objects", icon='INFO')

            # Export buttons
            selection_count = len(context.selected_objects)
            
            row = layout.row(align=True)
            if selection_count > 1: row.operator(EXPORT_OT_operator.bl_idname, text=f"FBX Export ({selection_count})", icon='MESH_CUBE')
            else: row.operator(EXPORT_OT_operator.bl_idname, text="FBX Export", icon='MESH_CUBE')
            row.enabled = False # selection_count > 0
            
            row = layout.row(align=True)
            if selection_count > 1: row.operator(EXPORT_GLB_OT_operator.bl_idname, text=f"GLB Export ({selection_count})", icon='FACE_MAPS')
            else: row.operator(EXPORT_GLB_OT_operator.bl_idname, text="GLB Export", icon='FACE_MAPS')
            row.enabled = selection_count > 0
            
        except Exception as e:
            pass

classes = (
    EXPORT_PT_panel,
) 