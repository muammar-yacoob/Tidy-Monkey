#https://panettonegames.com/
#https://blendermarket.com/products/tidy-monkey

import bpy
from bpy.types import Panel

import os
import bpy.ops
import bmesh

class TITLE_PT_panel(bpy.types.Panel):
    bl_label = "Tidy Monkey"
    bl_idname = "TitlePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tidy Monkey'

    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        try: 
            row.label(text= "Mode: " + context.active_object.mode)
        except:
            row.label(text= "Mode: N/A")
            
#-----Sub Panels------   
class ORGANIZE_PT_panel(bpy.types.Panel):
    bl_label = "Organize"
    bl_idname = "OrganizePanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'TitlePanel'
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout


        try:
            
            #selectedVerts = len([v for v in bpy.context.active_object.data.vertices if v.select])
            row = layout.row()
            row.operator("origin.toselected", text="Origin to Selection", icon='PIVOT_CURSOR')
            row.enabled = context.active_object.mode == 'EDIT' and context.active_object is not None
            
            row = layout.row()
            if context.mode != 'EDIT_MESH':
                row.operator("align.toview", text="Align to View", icon='VIEW3D')
                row.enabled = context.active_object.mode == 'OBJECT' and len(context.selected_objects) == 1
            row = layout.row()
            if context.mode == 'EDIT_MESH':
                row.operator("bottoms.select", text="Select Bottom Verts", icon='SORT_ASC')
                row.enabled = context.active_object.mode == 'EDIT' and context.active_object is not None
            
            row = layout.row()
            row = layout.row()
            
            if context.mode == 'EDIT_MESH':
                row = layout.row()
                row.operator("material.select", text="Select by Material", icon='MATERIAL')
                row = layout.row()
                row.operator("perimeter.select", text="Select by Perimeter", icon='MESH_CIRCLE')
                row = layout.row()

  
            row = layout.row()
            if context.mode != 'EDIT_MESH':
                row.operator("centerregions.center", text="Center Origins", icon='PIVOT_BOUNDBOX    ')
                row.enabled = context.active_object.mode == 'OBJECT' and len(context.selected_objects) > 0
                
                row = layout.row()
                row.operator("origin.tobottomcenter", text="Origin to Bottom Center", icon='ANCHOR_BOTTOM')
                row.enabled = context.active_object.mode == 'OBJECT' and len(context.selected_objects) > 0
            
            
                row = layout.row()
                row.operator("samemesh.similar", text="Select Similar Meshes", icon='OUTLINER_OB_MESH')
                row.enabled = context.active_object.type == 'MESH' and len(context.selected_objects) == 1
                row = layout.row()
                
                row.operator("apply.mods", text="Apply All Modifiers", icon='CHECKMARK')
                row.enabled = context.active_object.type == 'MESH' and len(context.selected_objects) > 0

                col = layout.column(align=True)
                row = col.row(align=True)
                row.label(text="Align Objects:")
                row = col.row(align=True)
                row.operator("alignobjects.align", text="X").algn = 'X'
                row.operator("alignobjects.align", text="Y").algn = 'Y'
                row.operator("alignobjects.align", text="Z").algn = 'Z'
                row.enabled = context.active_object.mode == 'OBJECT' and len(context.selected_objects) > 1 
                

        except:
            print('err')  

class RenameBonesProps(bpy.types.PropertyGroup):
    old_text: bpy.props.StringProperty(name="Old Text", default = "mixamo")
    new_text: bpy.props.StringProperty(name="New Text")
    match_case: bpy.props.BoolProperty(name="Match Case", default=False)

class CLEANUP_PT_panel(bpy.types.Panel):
    bl_label = "Clean Up"
    bl_idname = "CleanUp"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = 'TitlePanel'
    bl_options = {'DEFAULT_CLOSED'}


    def draw(self, context):

        layout = self.layout
        try:
            if context.mode != 'EDIT_MESH':
                row = layout.row()
                row.operator("fixnormals.fix", text="Fix Normals", icon='MOD_NORMALEDIT')
                row.enabled = context.active_object.type == 'MESH' and len(context.selected_objects) > 0
                
                row = layout.row()
                row.operator("clearmats.clear", text="Remove Unused Materials", icon='MATERIAL_DATA')
                row.enabled = context.active_object.type == 'MESH' and len(context.selected_objects) > 0
                row = layout.row()
                row.operator("generate.actions", text="Push to NLA Stack", icon='ACTION_TWEAK')
                row = layout.row()
                row.operator("deletetextures.delete", text="Clean Unused Textures", icon='TEXTURE')
                row.enabled = context.active_object.type == 'MESH'
                row = layout.row()
###
                # Only show rename bones section if an armature is selected
                has_armature = False
                for obj in context.selected_objects:
                    if obj.type == 'ARMATURE':
                        has_armature = True
                        break
                
                if has_armature:
                    box = layout.box()
                    box.label(text="Rename Bones & Animations", icon='BONE_DATA')
                    props = context.scene.rename_bones_props
                    row = box.row()
                    row.prop(props, "old_text")
                    row = box.row()
                    row.prop(props, "new_text")
                    row = box.row()
                    row.prop(props, "match_case")
                    row = box.row()
                    op = row.operator("renamebones.rename", text="Replace Text", icon='OUTLINER_DATA_FONT')
                    op.old_text = props.old_text
                    op.new_text = props.new_text
                    op.match_case = props.match_case
                    op.enabled = context.active_object.type == 'ARMATURE' and len(context.selected_objects) > 0

###

                row = layout.row()
                row.operator("renamevertgroups.rename", text="Clean Mixamo Weights", icon='GROUP_VERTEX')
                row.enabled = context.active_object.type == 'MESH' and len(context.selected_objects) > 0
                
############ mesh only  
            if context.mode == 'EDIT_MESH':
                row = layout.row()
                row.operator("checker.edge", text="Checker Edge Selection", icon='EDGESEL')

                row = layout.row()
                row.operator("clean.verts", text="Dissolve Similar Vertices", icon='SNAP_VERTEX')
                
########## armature & mesh                
            if context.mode == 'EDIT_MESH' or context.mode == 'EDIT_ARMATURE':
                row = layout.row()
                row.operator("fix.rotation", text="Reset Rotation", icon='ORIENTATION_LOCAL')
                
        except:
            print('err')  

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
            
            materialCount = len(context.active_object.material_slots) \
            if context.active_object.material_slots is not None else 0
            
            try:
                nlaCount = len(context.active_object.animation_data.nla_tracks) \
                if context.active_object.animation_data.nla_tracks is not None else 0
            except:
                nlaCount = 0

            try: shapeKeyCount = len(bpy.context.active_object.data.shape_keys.key_blocks) \
                if bpy.context.active_object.data.shape_keys.key_blocks is not None else 0            
            except: shapeKeyCount =0
                
            
            if context.active_object.type == 'MESH':
                row = layout.row()

                if len(context.selected_objects) ==1:
                    row.label(text=context.active_object.name + " details",icon='INFO')
                    row = layout.row()

                    row.label(text="Verts: " + str(len(context.active_object.data.vertices)))
                    row.label(text="Mats: " + str(materialCount))
                    row = layout.row()
                    row.label(text="Acts: " + str(nlaCount))
                    row.label(text="Keys: " + str(shapeKeyCount))

                if len(context.selected_objects) >1:
                    row.label(text="Multiple Objects",icon='INFO')
                    #row = layout.row()
                    #row.label(text="Mats: " + str(len(bpy.data.materials) if bpy.data.materials is not None else 0))
                    #row.label(text="Acts: " + str(len(bpy.data.animation_data) if bpy.data.animation_data is not None else 0))
                    #row.label(text="Keys: " + str(len(bpy.data.shape_keys.key_blocks) if bpy.data.shape_keys.key_blocks is not None else 0))
                
                

            row = layout.row()        
            row.operator("exportfbxxx.export", text="Export Selected as FBX", icon='EXPORT')
            row.enabled = len(context.selected_objects) > 0
            row = layout.split()
            layout.separator()

            col = layout.column(align=True)
            row = col.row(align=True)
            row.label(text="Support Tidy Monkey", icon='HEART')
            
            row.operator("sharelove.share", text="", icon='URL').shareType = 'YT'
            row.operator("sharelove.share", text="", icon='FUND').shareType = 'WB'
      
            
        except:
            print('err')  
