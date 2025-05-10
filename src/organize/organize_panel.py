import bpy
import bmesh
from bpy.types import Panel
from ..base_panel import TITLE_PT_panel
from ..organize.origin_to_selected import ORG_SELECTED_OT_operator
from ..organize.center_origins import ORG_CENTER_OT_operator
from ..organize.origin_to_bottom import ORG_BOTTOMCENTER_OT_operator
from ..organize.align_to_view import ORG_ALIGNTOVIEW_OT_operator
from ..organize.align_objects import ALIGN_OT_operator
from ..organize.apply_modifiers import APPLY_MODS_OT_operator
from ..organize.select_similar import (SELECT_MAT_OT_operator, SELECT_PER_OT_operator, SELECT_UV_OT_operator)
from ..organize.checker_edge import CHECKER_EDGE_OT_operator
from ..organize.select_bottom import BUTTS_OT_operator
from ..organize.select_similar_mesh import SELECT_SAME_OT_operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class ORGANIZE_PT_panel(bpy.types.Panel):
    bl_label = "Organize"
    bl_idname = "ORGANIZE_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = TITLE_PT_panel.bl_idname
    
    def draw(self, context):
        layout = self.layout
        in_object_mode = context.active_object is not None and context.active_object.mode == 'OBJECT'
        in_edit_mode = context.active_object is not None and context.active_object.mode == 'EDIT'
        selection_count = len(context.selected_objects)

        try:
            # OBJECT MODE SECTION
            if in_object_mode:
                # Origin tools group
                box = layout.box()
                # box.label(text="Origin Tools")
                
                row = box.row()
                if selection_count > 1:
                    row.operator("organize.centerorigins", text=f"Center Origins ({selection_count})", icon='ANCHOR_CENTER')
                else:
                    row.operator("organize.centerorigins", text="Center Origin", icon='ANCHOR_CENTER')
                row.enabled = selection_count > 0
                
                row = box.row()
                if selection_count > 1:
                    row.operator("organize.origintobottomcenter", text=f"Origin to Bottom ({selection_count})", icon='ANCHOR_BOTTOM')
                else:
                    row.operator("organize.origintobottomcenter", text="Origin to Bottom", icon='ANCHOR_BOTTOM')
                row.enabled = selection_count > 0
                
                # Alignment tools group
                box = layout.box()
                # box.label(text="Alignment Tools")
                
                row = box.row()
                if selection_count > 1:
                    row.operator("organize.aligntoview", text=f"Align to View ({selection_count})", icon='ORIENTATION_GIMBAL')
                else:
                    row.operator("organize.aligntoview", text="Align to View", icon='ORIENTATION_GIMBAL')
                row.enabled = selection_count > 0
                
                col = box.column(align=True)
                row = col.row(align=True)
                row.operator("organize.alignobjects", text="X").algn = 'X'
                row.operator("organize.alignobjects", text="Y").algn = 'Y'
                row.operator("organize.alignobjects", text="Z").algn = 'Z'
                row.enabled = selection_count > 1
                
                # Selection and Modifiers tools
                row = layout.row()
                row.operator("organize.selectsimilarmesh", icon='MOD_MESHDEFORM')
                row.enabled = context.active_object.type == 'MESH' and selection_count == 1
                
                row = layout.row()
                
                has_modifiers = False
                for obj in context.selected_objects:
                    if obj.type == 'MESH' and len(obj.modifiers) > 0:
                        has_modifiers = True
                        break
                
                if selection_count > 1:
                    row.operator("organize.applymodifiers", text=f"Apply Modifiers ({selection_count})", icon='MODIFIER_DATA')
                else:
                    row.operator("organize.applymodifiers", text="Apply Modifiers", icon='MODIFIER_DATA')
                row.enabled = has_modifiers
            
            # EDIT MODE SECTION
            if in_edit_mode:
                # Origin tool for edit mode
                row = layout.row()
                row.operator("organize.origintoselected", icon='PIVOT_CURSOR')
                
                obj = context.edit_object
                if obj and obj.type == 'MESH':
                    mesh = bmesh.from_edit_mesh(obj.data)
                    row.enabled = any(v.select for v in mesh.verts)
                else:
                    row.enabled = False
                
                # Selection Tools box
                box = layout.box()
                # box.label(text="Selection Tools")
                
                # Geometry-based selections
                row = box.row()
                row.operator("organize.selectbottom", text="Select Bottom", icon='TRIA_DOWN_BAR')
                
                row = box.row()
                row.operator("organize.selectperimeter", icon='RESTRICT_SELECT_OFF')
                
                # Topology-based selections
                if context.tool_settings.mesh_select_mode[1]:  # Edge select mode
                    row = box.row()
                    op = row.operator("organize.checkeredge", icon='ALIGN_JUSTIFY')
                    
                    obj = context.edit_object
                    if obj and obj.type == 'MESH':
                        mesh = bmesh.from_edit_mesh(obj.data)
                        selected_edges = sum(1 for e in mesh.edges if e.select)
                        row.enabled = selected_edges > 0 and selected_edges % 8 == 0
                    else:
                        row.enabled = False
                
                # Attribute-based selections
                row = box.row()
                row.operator("organize.selectuv", icon='RESTRICT_SELECT_OFF')
                
                row = box.row()
                op = row.operator("organize.selectmaterial", icon='RESTRICT_SELECT_OFF')
                
                if context.tool_settings.mesh_select_mode[2]:  # Face select mode
                    obj = context.edit_object
                    if obj and obj.type == 'MESH':
                        mesh = bmesh.from_edit_mesh(obj.data)
                        row.enabled = any(f.select for f in mesh.faces)
                    else:
                        row.enabled = False
                else:
                    row.enabled = False
                
        except Exception as e:
            print(f"ERROR in ORGANIZE_PT_panel.draw(): {str(e)}")
            layout.label(text=f"Error: {str(e)}")

classes = (ORGANIZE_PT_panel,) 