import bpy
from bpy.types import Operator



import os
import bpy.ops
import bmesh



class ORG_SELECTED_OT_operator(bpy.types.Operator):
    bl_label = "Origin to Selected"
    bl_idname = "origin.toselected"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.view3d.snap_cursor_to_selected()
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        bpy.ops.object.editmode_toggle()
        return {"FINISHED"}




class ORG_CENTER_OT_operator(bpy.types.Operator):
    import bpy
    context = bpy.context
        
    #objCount = bpy.props.IntProperty()
    bl_label = "Center Origins"# of " + str(objCount) #str(self.objCount)
    bl_idname = "centerregions.center"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        sel_objs = [obj for obj in bpy.context.selected_objects]# if obj.type == 'MESH']
        #bpy.ops.object.select_all(action='DESELECT')
        for obj in sel_objs:
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')    
            
        self.report({'INFO'},  str(len(sel_objs)) + " Origins were Centered")        
        return {"FINISHED"}

class BUTTS_OT_operator(bpy.types.Operator):
    bl_label = "Select Bottom"
    bl_idname = "bottoms.select"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
         #bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action = 'DESELECT')

        object = bpy.context.active_object
        vcount = len(object.data.vertices)
        currentMesh = bmesh.from_edit_mesh(object.data)

        if (vcount > 0):
            lowest = currentMesh.verts[0]
            for i in range(vcount):
                if (lowest.co.z > currentMesh.verts[i].co.z):
                    lowest = currentMesh.verts[i]

            for v in currentMesh.verts:
                if (v.co.z == lowest.co.z):
                    v.select = True
                else:
                    v.select = False

        #bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        return {"FINISHED"}

class SELECT_SAME_OT_operator(bpy.types.Operator):
    bl_label = "Select Similar Mesh"
    bl_idname = "samemesh.similar"
    bl_options = {'REGISTER', 'UNDO'}
        
    similar = bpy.props.StringProperty(name="Similar:")
  
    def execute(self, context):

        active_object = bpy.context.view_layer.objects.active
        active_verts = len(active_object.data.vertices)
        
        for all_objects in  bpy.context.view_layer.objects:
            if all_objects.type == 'MESH':
                all_objects_verts = len(all_objects.data.vertices)           
                if all_objects_verts == active_verts:
                    all_objects.select_set(state = True)
                    
        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        self.report({'INFO'},  str(len(sel_objs)) + " Objects were found")
        return {"FINISHED"}

class CLEAR_MATS_OT_operator(bpy.types.Operator):
    bl_label = "Clear Unused Materials"
    bl_idname = "clearmats.clear"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        #bpy.ops.object.select_all(action='DESELECT')
        for obj in sel_objs:
            bpy.ops.object.material_slot_remove_unused()
        
        self.report({'INFO'}, "Unused Materials were removed from " + str(len(sel_objs)) + " Objects")
        return {"FINISHED"}

class GEN_ACTS_OT_operator(bpy.types.Operator):
    bl_label = "Generate Actions"
    bl_idname = "generate.actions"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        #bpy.ops.object.select_all(action='DESELECT')
        #for obj in sel_objs:
        #    obj.action_pushdown
        #bpy.ops.action.push_down()




        for obj in sel_objs:
            if obj.animation_data is not None:
                action = obj.animation_data.action
                if action is not None:
                    #obj.animation_data.nla_tracks.
                    
                    track = obj.animation_data.nla_tracks.new()
                    track.strips.new(action.name, action.frame_range[0], action)
                    obj.animation_data.action = None # to avoid pushing the same animation more than once
                

        #for a in bpy.data.actions:
            #print(a.name)
#        for obj in sel_objs:
#            #bpy.ops.nla.selected_objects_add()
#            if obj.animation_data is not None:
#                action = obj.animation_data.action
#                if action is not None:
#                    action.push_down


        
        self.report({'INFO'}, "Actions Generated for " + str(len(sel_objs)) + "")
        return {"FINISHED"}

class CLEAN_TEX_OT_operator(bpy.types.Operator):
    bl_label = "Delete Unused Textures"
    bl_idname = "deletetextures.delete"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #bpy.ops.outliner.id_remap(id_type='TEXTURE', old_id='myTexture.001', new_id='myTexture.001')
        purgedCount = bpy.ops.outliner.orphans_purge()
        self.report({'INFO'}, str(purgedCount) + " Unused Objects were Purged")
        
        for block in bpy.data.materials:
            if block.users == 0:
                bpy.data.materials.remove(block)

        for block in bpy.data.textures:
            if block.users == 0:
                bpy.data.textures.remove(block)

        for block in bpy.data.images:
            if block.users == 0:
                bpy.data.images.remove(block)
        return {"FINISHED"}

class REN_BONES_OT_operator(bpy.types.Operator):
    bl_label = "Rename Mixamo Bones"
    bl_idname = "renamebones.rename"
    bl_options = {'REGISTER', 'UNDO'}
    
    rename = bpy.props.StringProperty(name="Rename:")
    
    def execute(self, context):

        for bone in bpy.context.active_object.pose.bones:
            bone.name = bone.name.replace("mixamorig:","")


        return {"FINISHED"}

class ALIGN_OT_operator(bpy.types.Operator):
    bl_label = "Aligne Objects"
    bl_idname = "alignobjects.align"
    bl_options = {'REGISTER', 'UNDO'}
    
    algnmnt = bpy.props.StringProperty(name="Alignment:")
    
    def execute(self, context):
        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        bpy.ops.object.align(align_axis={self.algnmnt})
        return {"FINISHED"}

class EXPORT_OT_operator(bpy.types.Operator):
    bl_label = "Export FBX"
    bl_idname = "exportfbxxx.export"
    
    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        blend_file_path = bpy.data.filepath
        directory = os.path.dirname(blend_file_path) + "\\FBXs"
        
        try:
            if not os.path.exists(directory):
                os.mkdir("FBXs")
        except:
            self.report({'ERROR'}, "could not create " + directory + "\nMake sure file is saved first and restart blender" )
            return {'FINISHED'}
            
        sel_objs = [obj for obj in bpy.context.selected_objects]# if obj.type == 'MESH']
        bpy.ops.object.select_all(action='DESELECT')
        
        #prepare textures
        bpy.ops.outliner.orphans_purge()
        
        try:
            bpy.ops.file.pack_all()
        except Exception as e:
            self.report({'ERROR'}, "Could Not Pack All Textures\n" + str(e))
        
        try:
            bpy.ops.file.unpack_all(method='WRITE_LOCAL')
            bpy.ops.file.make_paths_absolute()
        except:
            self.report({'ERROR'}, "Error Packing Textures" )
            
        #---
        
            currentFrame = bpy.context.scene.frame_current
            bpy.ops.screen.animation_cancel(restore_frame=True)
            bpy.context.scene.frame_set(bpy.context.scene.frame_start)
            
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
            
            bpy.context.scene.frame_set(currentFrame) 
        
        for obj in sel_objs:
            bpy.ops.object.select_all(action='DESELECT')                
            obj_path = os.path.join(directory ,obj.name + "." + "fbx") #make sure the .blend file is saved first or you get an error

            obj.select_set(True)
            #obj.select_set(state=True)
            #obj.transform_apply(location=False, rotation=True, scale=True)

            originalLoc = obj.location.copy()
            obj.location = (0,0,0)
            
     

            #except:
                #self.report({'ERROR'}, "Error Applying Rotation & Scale" )
                #---
                
                                
            hasShapeKey = False
            try:
                hasShapeKey = len(obj.data.shape_keys.key_blocks)
            except:
                hasShapeKey = False
                
            hasShapeKey = bool(obj.type == 'ARMATURE') or bool(hasShapeKey)
            

            for child in obj.children:
                child.select_set(state=True)
            

            
            bpy.ops.export_scene.fbx(
            filepath=obj_path,
            use_selection=True,
            check_existing=False,
            
            global_scale=1.0,
            use_mesh_modifiers=True,
            axis_forward='Z', axis_up='Y',
            apply_scale_options = 'FBX_SCALE_UNITS',
            bake_space_transform=True, #Remove if broken <<<<<<<<<<<<<<
            #-----------
            
            filter_glob="*.fbx",

            bake_anim_use_all_bones=True,
            use_armature_deform_only=True,              
            add_leaf_bones=False,
            
            bake_anim=True,
            bake_anim_use_nla_strips=True,
            bake_anim_use_all_actions=False #hasShapeKey  #True for shape keys and armatures 
            )

            #obj.select_set(False)
            #bpy.ops.object.select_all(action='DESELECT')

            obj.location = originalLoc        
            os.system("start "+ directory)
        
             
            
        #reselect
        for obj in sel_objs:
            obj.select_set(True)
        self.report({'INFO'}, str(len(sel_objs)) + " Objects were Exported to "+ directory )
        return {'FINISHED'}

class SHARE_OT_operator(bpy.types.Operator):
    bl_label = ""
    bl_idname = "sharelove.share"
    
    donate = bpy.props.StringProperty(name="Donate:")
    
    
    def execute(self, context):
        url = "https://paypal.me/PanettoneGames?locale.x=en_GB"
        if self.donate == "TW":
            url =  "https://twitter.com/intent/tweet?text=I%20Support%20TidyMonkey%20Blender%20Addon%20for%20Artists%20and%20Game%20Developers%0D%0Ahttp://www.PanettoneGames.com%20pic.twitter.com/1RuB2tqJrJ%20%0D%0A@88Spark"
        os.system("start "+ url)

        return{"FINISHED"}
