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
        row.label(text= "Mode: " + context.active_object.mode)





#-----Sub Panels----------------------------------------------        
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
            row = layout.row()
            row.operator("origin.toselected",icon='DOT')
            row.enabled = context.active_object.mode == 'EDIT' and context.active_object is not None # and active_object.type == 'MESH': 
            
            row = layout.row()
            row.operator("align.toview",icon='ORIENTATION_GIMBAL')
            row.enabled = context.active_object.mode == 'EDIT' and context.active_object is not None # and active_object.type == 'MESH': 
  
               
            row = layout.row()
            if context.mode == 'EDIT_MESH':
                row.operator("bottoms.select",text ="Select Bottom", icon='TRIA_DOWN_BAR') #.selectedObjectsCount = 3
                row.enabled = context.active_object.mode == 'EDIT' and context.active_object is not None  # context.active_object is not None
            
            row = layout.row()
            if context.mode != 'EDIT_MESH':
                row.operator("centerregions.center",text ="Center Origins of " + str(len(context.selected_objects)), icon='SNAP_FACE_CENTER') #.selectedObjectsCount = 3
                row.enabled = context.active_object.mode == 'OBJECT' and len(context.selected_objects) > 0  # context.active_object is not None
            
            
            row = layout.row()
            if context.mode != 'EDIT_MESH': 
                row.operator("samemesh.similar",icon='PARTICLEMODE')
                row.enabled = context.active_object.type == 'MESH' and len(context.selected_objects) == 1 # context.active_object is not None
                row = layout.row()


                row.label(text="Alignment",icon='MOD_ARRAY')
                row = layout.row()
                row.operator("alignobjects.align", text = 'X' ).algnmnt = 'X'
                row.operator("alignobjects.align", text = 'Y' ).algnmnt = 'Y'
                row.operator("alignobjects.align", text = 'Z' ).algnmnt = 'Z'
                row.enabled = len(context.selected_objects) > 1 # context.active_object is not None

        except:
            print('err')  

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
                row.operator("clearmats.clear", text = "Clear Unused Mats from "+ str(len(context.selected_objects)) ,icon='NODE_MATERIAL')
                row.enabled = context.active_object.type == 'MESH' and len(context.selected_objects) > 0 # context.active_object is not None        
                row = layout.row()
                row.operator("generate.actions",text ="Generate Actions for " + str(len(context.selected_objects)), icon='ARMATURE_DATA') #.selectedObjectsCount = 3
                row.enabled = context.active_object.mode == 'OBJECT' and len(context.selected_objects) > 0  # context.active_object is not None
                row = layout.row()
                row.operator("deletetextures.delete",icon='RENDER_RESULT')
                row.enabled = context.active_object.type == 'MESH'
                row = layout.row()
                row.operator("renamebones.rename",icon='BONE_DATA')
                row.enabled = context.active_object.type == 'ARMATURE' and len(context.selected_objects) > 0 # context.active_object is not None
                
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
                    row.label(text="Acts: " + str(nlaCount))
                    row.label(text="Keys: " + str(shapeKeyCount))

                if len(context.selected_objects) >1:
                    row.label(text="Multiple Objects",icon='INFO')
                    #row = layout.row()
                    #row.label(text="Mats: " + str(len(bpy.data.materials) if bpy.data.materials is not None else 0))
                    #row.label(text="Acts: " + str(len(bpy.data.animation_data) if bpy.data.animation_data is not None else 0))
                    #row.label(text="Keys: " + str(len(bpy.data.shape_keys.key_blocks) if bpy.data.shape_keys.key_blocks is not None else 0))
                
                

            row = layout.row()        
            row.operator("exportfbxxx.export",text ="FBX Export " + str(len(context.selected_objects))+ " Objects",icon='AUTO' ) 
            row.enabled = len(context.selected_objects) > 0  # context.active_object is not None
            row = layout.split()
            layout.separator()
            row = layout.row()
            row = layout.row()
            
            row.label(text="Share the Love")
            row.operator("sharelove.share",text="",icon='COMMUNITY').donate ='TW'
            row.operator("sharelove.share",text="",icon='FUND').donate ='PPL'
        except:
            print('err')  
