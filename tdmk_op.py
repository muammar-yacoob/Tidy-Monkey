#https://panettonegames.com/
#https://gumroad.com/l/CpQAM

import bpy
from bpy.types import Operator

import os
import bpy.ops
import bmesh

###########################

        
        
class SELECT_MAT_OT_operator(bpy.types.Operator):
    bl_label = "Similar Material"
    bl_idname = "material.select"
    bl_description ="Select Similar Faces"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE') 
            modes = ['MATERIAL','PERIMETER','NORMAL','AREA','COPLANAR']
            currentTrait = modes[0]
            bpy.ops.mesh.select_similar(type=currentTrait, threshold=0.01) 
        except:
            bpy.ops.mesh.select_mode(type='FACE')
            self.report({'ERROR'}, "Select a face first" ) 
        return {"FINISHED"}  

class SELECT_PER_OT_operator(bpy.types.Operator):
    bl_label = "Similar Perimeter"
    bl_idname = "perimeter.select"
    bl_description ="Select Similar Faces"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE') 
            modes = ['MATERIAL','PERIMETER','NORMAL','AREA','COPLANAR']
            currentTrait = modes[1]
            bpy.ops.mesh.select_similar(type=currentTrait, threshold=0.01) 
        except:
            bpy.ops.mesh.select_mode(type='FACE')
            self.report({'ERROR'}, "Select a face first" ) 
        return {"FINISHED"}  

class SELECT_NORM_OT_operator(bpy.types.Operator):
    bl_label = "Similar Normal"
    bl_idname = "normal.select"
    bl_description ="Select Similar Faces"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE') 
            modes = ['MATERIAL','PERIMETER','NORMAL','AREA','COPLANAR']
            currentTrait = modes[2]
            bpy.ops.mesh.select_similar(type=currentTrait, threshold=0.01) 
        except:
            bpy.ops.mesh.select_mode(type='FACE')
            self.report({'ERROR'}, "Select a face first" ) 
        return {"FINISHED"}  

class SELECT_AREA_OT_operator(bpy.types.Operator):
    bl_label = "Similar Area"
    bl_idname = "area.select"
    bl_description ="Select Similar Faces"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE') 
            modes = ['MATERIAL','PERIMETER','NORMAL','AREA','COPLANAR']
            currentTrait = modes[3]
            bpy.ops.mesh.select_similar(type=currentTrait, threshold=0.01) 
        except:
            bpy.ops.mesh.select_mode(type='FACE')
            self.report({'ERROR'}, "Select a face first" ) 
        return {"FINISHED"}  
    
class SELECT_COPLANAR_OT_operator(bpy.types.Operator):
    bl_label = "Similar Coplanner"
    bl_idname = "coplanar.select"
    bl_description ="Select Similar Faces"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE') 
            modes = ['MATERIAL','PERIMETER','NORMAL','AREA','COPLANAR']
            currentTrait = modes[4]
            bpy.ops.mesh.select_similar(type=currentTrait, threshold=0.01) 
        except:
            bpy.ops.mesh.select_mode(type='FACE')
            self.report({'ERROR'}, "Select a face first" ) 
        return {"FINISHED"}  
         
class CHECKER_EDGE_OT_operator(bpy.types.Operator):
    bl_label = "Checker Edge"
    bl_idname = "checker.edge"
    bl_description ="Checker Select Edges"
    bl_options = {'REGISTER', 'UNDO'}
    

    def execute(self, context):
        try:
            bpy.ops.mesh.loop_multi_select(ring=True)
            bpy.ops.mesh.select_nth(offset=1)
            bpy.ops.mesh.loop_multi_select(ring=False)
        except:
            self.report({'ERROR'},'No Uniformal Edges Detected')
           
        return {"FINISHED"}

##################### 
#selectIndex =  0
#currentTrait = 'MATERIAL'
class xSELECT_TRAIT_OT_operator(bpy.types.Operator):
    bl_label = "Select Trait"
    bl_idname = "selecttrait.select"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):


# #        for prop_id in prop_names:
# #            print(prop_id)  
# #            getattr(average_type)
        # #me = bpy.context.object.data
        # #bm = bmesh.from_edit_mesh(me)
        # #bm.select_history[-1]
# #        global cashedVerts
# #        cashedVerts = [elem.index for elem in bm.select_history if isinstance(elem, bmesh.types.BMVert)]
# #        ([v for v in cashedVerts if v.select])        

        # #switch to face mode    
        # bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE') 
        # modes = ['MATERIAL','PERIMETER','NORMAL','AREA','COPLANAR']
        # #for i in range(len(words):
        # global selectIndex
        # global currentTrait
       
        # if(selectIndex >= len(modes)-1):
            # selectIndex = -1
        # #else:

        # currentTrait = modes[selectIndex]
        # bpy.ops.mesh.select_similar(type=currentTrait, threshold=0.01) 
        # selectIndex += 1  

        # currentTrait = modes[selectIndex] 
        # print(modes[selectIndex])
        return {"FINISHED"}    

class FIX_NORMALS_OT_operator(bpy.types.Operator):
    bl_label = "Fix Normals"
    bl_idname = "fixnormals.fix"
    bl_description ="Fixes common Normals issues"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')    

        bpy.ops.mesh.normals_make_consistent(inside=False)

        bpy.ops.object.mode_set(mode='OBJECT') 
        bpy.ops.object.shade_flat()
        bpy.context.object.data.use_auto_smooth = True

        bpy.ops.object.mode_set(mode='EDIT')    
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
        bpy.ops.mesh.edges_select_sharp()
        bpy.ops.mesh.mark_sharp()
            
        bpy.ops.mesh.select_all(action='SELECT')            
        bpy.ops.mesh.average_normals(average_type='FACE_AREA')
        
        bpy.ops.object.mode_set(mode='OBJECT') 
        
        return {"FINISHED"}
  

class ORG_SELECTED_OT_operator(bpy.types.Operator):
    bl_label = "Origin to Selected"
    bl_idname = "origin.toselected"
    bl_description ="Sets object origin to selection"
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
    bl_description ="Centers the origin"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        sel_objs = [obj for obj in bpy.context.selected_objects]# if obj.type == 'MESH']
        #bpy.ops.object.select_all(action='DESELECT')
        for obj in sel_objs:
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')    
            
        self.report({'INFO'},  str(len(sel_objs)) + " Origins were Centered")        
        return {"FINISHED"}
        
class ORG_ALIGNTOVIEW_OT_operator(bpy.types.Operator):
    bl_label = "Align to View"
    bl_idname = "align.toview"
    bl_description ="Aligns object to view "
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        regData = context.region_data
        context.object.rotation_euler = regData.view_rotation.to_euler()
        return {"FINISHED"}

class ORG_FIXROTATION_OT_operator(bpy.types.Operator):
    bl_label = "Fix Rotation"
    bl_idname = "fix.rotation"
    bl_description ="Fixes Object Rotation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try:    
            regData = context.region_data
            
            bpy.ops.view3d.snap_cursor_to_selected()
            
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    override = bpy.context.copy()
                    override['area'] = area

                    bpy.ops.view3d.view_axis(override, type='BOTTOM', align_active=True, relative=False)
                    break
            
            
            bpy.ops.object.mode_set(mode='OBJECT')    
            obj = bpy.context.active_object
            bpy.ops.mesh.primitive_cube_add( align='VIEW')
            plane = bpy.context.selected_objects[0]

            
            #bad parenting 101
            bpy.ops.object.select_all(action='DESELECT')

            obj.select_set(True) 
            plane.select_set(True)    
            print("obj :" + obj.name)
            print("pln :" + plane.name)
            bpy.context.view_layer.objects.active = plane

            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
            bpy.ops.object.rotation_clear(clear_delta=False)
            
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True) 
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)

            bpy.ops.object.select_all(action='DESELECT')
            plane.select_set(True) 
            bpy.ops.object.delete(use_global=False)
            
            for area in bpy.context.screen.areas:
                if area.type == 'VIEW_3D':
                    override = bpy.context.copy()
                    override['area'] = area

                    bpy.ops.view3d.view_axis(override, type='FRONT', align_active=True, relative=False)
                    break
        except:
            self.report({'ERROR'}, "Please select a face first" )
        
        return {"FINISHED"}
    
class BUTTS_OT_operator(bpy.types.Operator):
    bl_label = "Select Bottom"
    bl_idname = "bottoms.select"
    bl_description ="Selects lower most vertices"
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
    bl_description ="Selects objects with similar vertex count"
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
    bl_description ="Clears unused materials"
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
    bl_description ="Pushes Animations to the NLA Stack"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):

        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        #bpy.ops.object.select_all(action='DESELECT')
        #for obj in sel_objs:
        #    obj.action_pushdown
        #bpy.ops.action.push_down()


        original_context = bpy.context.area.type
        bpy.context.area.type = "NLA_EDITOR"
        bpy.ops.anim.channels_clean_empty()
        bpy.context.area.type = original_context

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
    bl_description ="Removes unused textures"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        #bpy.ops.outliner.id_remap(id_type='TEXTURE', old_id='myTexture.001', new_id='myTexture.001')
        #purgedCount = bpy.ops.outliner.orphans_purge()
        
        try: 
            purgedCount = purgedCount = bpy.ops.outliner.orphans_purge()
            if(purgedCount > 0):
                self.report({'INFO'}, str(purgedCount) + " Unused Objects were Purged")
        except:
            purgedCount =0
            self.report({'INFO'}, "Nothing to clean. You're all set!")
        

        
        
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
    bl_description ="Removes the word Mixamo from all bones"
    bl_options = {'REGISTER', 'UNDO'}
    
    rename = bpy.props.StringProperty(name="Rename:")
    def execute(self, context):
        for bone in bpy.context.active_object.pose.bones:
            bone.name = bone.name.replace("mixamorig:","")
        return {"FINISHED"}
    
class REN_VERT_OT_operator(bpy.types.Operator):
    bl_label = "Rename Mixamo Vert Groups"
    bl_idname = "renamevertgroups.rename"
    bl_description ="Removes the word Mixamo from all vertex groups"
    bl_options = {'REGISTER', 'UNDO'}
        
    rename = bpy.props.StringProperty(name="Rename:")
    def execute(self, context):
        v_groups = bpy.context.active_object.vertex_groups
        for vn in v_groups:
            vn.name = vn.name.replace("mixamorig:","")
        return {"FINISHED"}
    
class ALIGN_OT_operator(bpy.types.Operator):
    bl_label = "Aligne Objects"
    bl_idname = "alignobjects.align"
    bl_description ="Aligns object to view"
    bl_options = {'REGISTER', 'UNDO'}
    
    algnmnt = bpy.props.StringProperty(name="Alignment:")
    
    def execute(self, context):
        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        bpy.ops.object.align(align_axis={self.algnmnt})
        return {"FINISHED"}

class EXPORT_OT_operator(bpy.types.Operator):
    bl_label = "Export FBX"
    bl_idname = "exportfbxxx.export"
    bl_description ="Exports selected Objects as FBX"
    
    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        blend_file_path = bpy.data.filepath
        directory = os.path.dirname(blend_file_path) + "\\FBXs"
        
        try:
            if not os.path.exists(directory):
                os.mkdir(directory)
        except:
            self.report({'ERROR'}, "could not create " + directory + " - Make sure file is saved first and restart blender" )
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
                
            #os.system("start "+ directory)
            os.system("start "+ os.path.dirname(blend_file_path))
        
             
            
        #reselect
        for obj in sel_objs:
            obj.select_set(True)
        self.report({'INFO'}, str(len(sel_objs)) + " Objects were Exported to "+ directory )
        return {'FINISHED'}

class SHARE_OT_operator(bpy.types.Operator):
    bl_label = ""
    bl_idname = "sharelove.share"
    bl_description ="Contribute"
    
    donate = bpy.props.StringProperty(name="Donate:")
    
    
    def execute(self, context):
        url = "https://paypal.me/PanettoneGames?locale.x=en_GB"
        if self.donate == "TW":
            url =  "https://twitter.com/intent/tweet?text=I%20Support%20TidyMonkey%20Blender%20Addon%20for%20Artists%20and%20Game%20Developers%0D%0Ahttp://www.PanettoneGames.com%20pic.twitter.com/1RuB2tqJrJ%20%0D%0A@88Spark"
        os.system("start "+ url)

        return{"FINISHED"}


class CLEAN_VERTS_OT_operator(bpy.types.Operator):
    bl_label = "Dessolve Similar Verts"
    bl_idname = "clean.verts"
    bl_description ="Dessolves Verts with similar connections:)"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        try:
            object = bpy.context.active_object
            bm = bmesh.from_edit_mesh(object.data)
            
            bpy.ops.mesh.select_similar(type='EDGE')
            bpy.ops.mesh.dissolve_verts()
    

            
#            for v in bm.verts:
#                if v.select == True:
#                    if len(v.link_edges) == 2:
#                        print(str(len(v.link_edges)))
#                        v.select = True
#                        #bm.verts.remove(v)
#                    else:
#                        v.select = False                        


            #verts2 = [v for v in bm.verts if len(v.link_edges) == 2]

            self.report({'INFO'},'Verts Dessolved')
        except:
            self.report({'ERROR'},'No Selected Vertices')
            
        return {"FINISHED"}