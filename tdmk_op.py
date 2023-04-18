#https://panettonegames.com/
#https://blendermarket.com/products/tidy-monkey

import bpy
from bpy.types import Operator

import os
import bpy.ops
import bmesh

class APPLY_MODS_OT_operator(bpy.types.Operator):
    bl_label = "Apply Modifiers"
    bl_idname = "apply.mods"
    bl_options = {'REGISTER', 'UNDO'}
        
    def execute(self, context):
        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        #bpy.ops.object.select_all(action='DESELECT')
        scn = bpy.context.scene
        for obj in sel_objs:
            #scn.objects.active = obj
            #bpy.context.scene.objects.active = obj
            bpy.ops.object.convert(target='MESH')

            #obj.convert(target='MESH')

        
        self.report({'INFO'}, "Mods applied to " + str(len(sel_objs)) + " Objects")
        return {"FINISHED"}         
        
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
            bpy.ops.mesh.select_nth(offset=3)
            bpy.ops.mesh.loop_multi_select(ring=False)
        except:
            self.report({'ERROR'},'No Uniformal Edges Detected')
            
        return {"FINISHED"}

class FIX_NORMALS_OT_operator(bpy.types.Operator):
    bl_label = "Beautify"
    bl_idname = "fixnormals.fix"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        try:
            mod_types = {'WeightedNormal'}
            sel_objs = [obj for obj in bpy.context.selected_objects]# if obj.type == 'MESH']
            for obj in sel_objs:
            
                bpy.context.view_layer.objects.active = obj #sets the obj accessible to bpy.ops
                
                bpy.ops.mesh.customdata_custom_splitnormals_clear()

                

                if 'WeightedNormal' in obj.modifiers: 
                    bpy.context.object.modifiers["WeightedNormal"].show_viewport = True
                else:
                    bpy.ops.object.modifier_add(type='WEIGHTED_NORMAL')
                    bpy.context.object.modifiers["WeightedNormal"].keep_sharp = True
                    
                if 'Weld' in obj.modifiers: 
                    bpy.context.object.modifiers["Weld"].show_viewport = True
                else:
                    bpy.ops.object.modifier_add(type='WELD')
                    bpy.context.object.modifiers["Weld"].merge_threshold = 0.007


                bpy.context.object.data.use_auto_smooth = True
                bpy.context.object.data.auto_smooth_angle = 60*22/7/180

                bpy.ops.object.mode_set(mode='EDIT')    
                bpy.ops.mesh.select_all(action='DESELECT')               
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
                bpy.ops.mesh.select_all(action='SELECT')    
                bpy.ops.mesh.normals_make_consistent(inside=False)               
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
                bpy.ops.mesh.select_all(action='DESELECT')  
                bpy.ops.mesh.edges_select_sharp(sharpness=75*22/7/180)
                bpy.ops.mesh.mark_sharp()
                #bpy.ops.object.mode_set(mode='OBJECT') 
                
                
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
                bpy.ops.mesh.select_all(action='SELECT')   
                
                # geo clean up 
                bpy.ops.mesh.dissolve_degenerate(threshold=0.0001) 
                bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=False)

                bpy.ops.mesh.normals_make_consistent(inside=False)

                bpy.ops.object.mode_set(mode='OBJECT') 
                bpy.ops.object.shade_flat()
                bpy.context.object.data.use_auto_smooth = True

                bpy.ops.object.mode_set(mode='EDIT')    
                bpy.ops.mesh.select_all(action='DESELECT')
                bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
                           
                bpy.ops.mesh.select_all(action='SELECT')            
                #bpy.ops.mesh.average_normals(average_type='FACE_AREA')
                
                bpy.ops.object.mode_set(mode='OBJECT') 
                bpy.ops.object.shade_smooth()

                        
        except:
            self.report({'ERROR'},'Error Fixing Normals')
        
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
        
    similar = bpy.props.StringProperty(name="Similar:" , options={'HIDDEN'})
  
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
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        original_context = bpy.context.area.type
        bpy.context.area.type = "NLA_EDITOR"
        bpy.ops.anim.channels_clean_empty()
        bpy.context.area.type = original_context

        for obj in selected_objects:
            if obj.animation_data is not None:
                action = obj.animation_data.action
                if action is not None:
                    # Check if the action is already in an NLA track
                    in_nla = False
                    for track in obj.animation_data.nla_tracks:
                        if track.strips[0].action == action:
                            in_nla = True
                            break
                    
                    if not in_nla:
                        track = obj.animation_data.nla_tracks.new()
                        track.strips.new(action.name, int(action.frame_range[0]), action)
                        obj.animation_data.action = None # to avoid pushing the same animation more than once
        
        self.report({'INFO'}, f"Actions generated for {len(selected_objects)} objects")
        bpy.context.area.type = 'NLA_EDITOR'

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
    bl_label = "Rename Bones"
    bl_idname = "renamebones.rename"
    bl_description ="Removes a certain text from all bones"
    bl_options = {'REGISTER', 'UNDO'}
    
    old_text: bpy.props.StringProperty(name="old_text")
    new_text: bpy.props.StringProperty(name="new_text")
    match_case: bpy.props.BoolProperty(name="match_case", default=False)
    
    def execute(self, context):
        props = context.scene.rename_bones_props
        old_text = props.old_text
        new_text = props.new_text
        match_case = props.match_case

        self.report({'INFO'}, "Replacing " + old_text + " with " + new_text)

        # Rename Armatures
        selected_armatures = [obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE']
        for armature in selected_armatures:
            
            bpy.ops.object.mode_set(mode='EDIT')
            for bone in armature.data.bones:
                text = bone.name
                if not match_case:
                    text = text.lower()
                    old_text = old_text.lower()

                text = text.replace(old_text, new_text, 1 if match_case else -1)
                bone.name = text

            bpy.ops.object.mode_set(mode='POSE')
            for pose_bone in armature.pose.bones:
                text = pose_bone.name
                if not match_case:
                    text = text.lower()
                    old_text = old_text.lower()

                text = text.replace(old_text, new_text, 1 if match_case else -1)
                pose_bone.name = text

        # Rename Meshes
        selected_meshes = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        for obj in selected_meshes:
            bpy.ops.object.mode_set(mode='EDIT')

            # Loop through all mesh data blocks in the object
            for mesh in obj.data.meshes:
                if old_text in mesh.name:
                    mesh.name = mesh.name.replace(old_text, new_text)

            bpy.ops.object.mode_set(mode='OBJECT')
        return {"FINISHED"}
    
class REN_VERT_OT_operator(bpy.types.Operator):
    bl_label = "Rename Mixamo Vert Groups"
    bl_idname = "renamevertgroups.rename"
    bl_description ="Removes the word Mixamo from all vertex groups"
    bl_options = {'REGISTER', 'UNDO'}
        
    bl_idname = "text_input.operator"
    bl_label = "Text Input Operator"

    text_input: bpy.props.StringProperty(name="Text Input")

    def execute(self, context):

        return {"FINISHED"}
    
class ALIGN_OT_operator(bpy.types.Operator):
    bl_label = "Aligne Objects"
    bl_idname = "alignobjects.align"
    bl_description ="Aligns object to view"
    bl_options = {'REGISTER', 'UNDO'}
    
    algn: bpy.props.StringProperty(default = 'Z', options={'HIDDEN'})
    
    def execute(self, context):
        sel_objs = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        self.report({'INFO'}, "Aligned at " + str(self.algn) + " axis")
        print((self.algn))
        bpy.ops.object.align(align_axis={self.algn})
        return {"FINISHED"}

class EXPORT_OT_operator(bpy.types.Operator):
    bl_idname = "exportfbxxx.export"
    bl_label = "Export FBX"
    bl_description = "Exports selected objects as FBX files"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        blend_file_path = bpy.data.filepath
        directory = os.path.dirname(blend_file_path) + "/FBXs"
        if not os.path.exists(directory):
            os.mkdir(directory)

        sel_objs = [obj for obj in bpy.context.selected_objects]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.outliner.orphans_purge()
        try:
            bpy.ops.file.pack_all()
        except Exception as e:
            self.report({'ERROR'}, "Could not pack all textures\n" + str(e))
        try:
            bpy.ops.file.unpack_all(method='USE_LOCAL')
            bpy.ops.file.make_paths_absolute()
        except:
            self.report({'ERROR'}, "Error packing textures")

        current_frame = bpy.context.scene.frame_current
        bpy.ops.screen.animation_cancel(restore_frame=True)
        bpy.context.scene.frame_set(bpy.context.scene.frame_start)

        for obj in sel_objs:
            bpy.ops.object.select_all(action='DESELECT')
            obj_path = os.path.join(directory, obj.name + ".fbx")

            obj.select_set(True)
            bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)

            original_loc = obj.location.copy()
            obj.location = (0, 0, 0)

            has_shape_key = bool(obj.type == 'ARMATURE')
            if not has_shape_key:
                try:
                    has_shape_key = len(obj.data.shape_keys.key_blocks) > 0
                except:
                    pass

            try:
                bpy.ops.export_scene.fbx(
                    filepath=obj_path,
                    use_selection=True,
                    check_existing=False,
                    global_scale=1.0,
                    apply_scale_options='FBX_SCALE_UNITS',
                    axis_forward='-Z',
                    axis_up='Y',
                    use_mesh_modifiers=True,
                    mesh_smooth_type='FACE',
                    use_mesh_edges=False,
                    use_tspace=True,
                    use_custom_props=True,
                    bake_space_transform=True,
                    bake_anim=True,
                    bake_anim_use_nla_strips=True,
                    bake_anim_use_all_actions=True,
                    add_leaf_bones=False,
                    primary_bone_axis='Y',
                    secondary_bone_axis='X',
                    use_armature_deform_only=True,
                    path_mode='AUTO',
                    batch_mode='OFF',
                    use_metadata=True,
                )
            except Exception as e:
                self.report({'ERROR'}, "Could not export FBX file\n" + str(e))

            obj.location = original_loc
            obj.select_set(False)

        bpy.context.scene.frame_set(current_frame)
        for obj in sel_objs:
            obj.select_set(True)
        self.report({'INFO'}, f"{len(sel_objs)} objects were exported to {directory}")
        os.system("start "+ os.path.dirname(blend_file_path))
        return {'FINISHED'}

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

            self.report({'INFO'},'Verts Dessolved')
        except:
            self.report({'ERROR'},'No Selected Vertices')
            
        return {"FINISHED"}

class SHARE_OT_operator(bpy.types.Operator):
    bl_label = ""
    bl_idname = "sharelove.share"
    bl_description ="Share"   
    
    shareType: bpy.props.StringProperty(default = 'YT', options={'HIDDEN'})
    
    def execute(self, context):
        print("self.shareType:",self.shareType)
        self.report({"INFO"},"%s "%(self.shareType))
        
        url = "https://blendermarket.com/products/tidy-monkey"
        if self.shareType == "YT":
            url =  "https://twitter.com/intent/tweet?text=I%20Support%20TidyMonkey%20Blender%20Addon%20for%20Artists%20and%20Game%20Developers%0D%0Ahttp://www.PanettoneGames.com%20pic.twitter.com/1RuB2tqJrJ%20%0D%0A@88Spark"
        os.system("start "+ url)

        return{"FINISHED"}
