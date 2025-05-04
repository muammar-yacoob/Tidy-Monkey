import bpy
from bpy.types import Operator, PropertyGroup

# Property group for bone renaming
class RenameBonesProps(bpy.types.PropertyGroup):
    old_text: bpy.props.StringProperty(name="Old Text", default="mixamo")
    new_text: bpy.props.StringProperty(name="New Text")
    match_case: bpy.props.BoolProperty(name="Match Case", default=False)

class REN_BONES_OT_operator(bpy.types.Operator):
    bl_label = "Rename Bones"
    bl_idname = "renamebones.rename"
    bl_description = "Removes a certain text from all bones"
    bl_options = {'REGISTER', 'UNDO'}
    
    old_text: bpy.props.StringProperty(name="old_text")
    new_text: bpy.props.StringProperty(name="new_text")
    match_case: bpy.props.BoolProperty(name="match_case", default=False)
    
    def execute(self, context):
        props = context.scene.rename_bones_props
        old_text = props.old_text
        new_text = props.new_text
        match_case = props.match_case
        
        if context.mode != 'OBJECT': 
            bpy.ops.object.mode_set(mode='OBJECT')
        
        selected_armatures = [obj for obj in context.selected_objects if obj.type == 'ARMATURE']
        if not selected_armatures:
            self.report({'WARNING'}, "No armature selected")
            return {'CANCELLED'}
            
        renamed_bones = []
            
        for armature in selected_armatures:
            context.view_layer.objects.active = armature
            
            bpy.ops.object.mode_set(mode='EDIT')
            for bone in armature.data.bones:
                old_name = bone.name
                compare_text = old_name if match_case else old_name.lower()
                compare_old = old_text if match_case else old_text.lower()
                if compare_old in compare_text:
                    new_name = old_name.replace(old_text, new_text, 1 if match_case else -1)
                    renamed_bones.append((old_name, new_name))
                    bone.name = new_name
            
            bpy.ops.object.mode_set(mode='POSE')
            for pose_bone in armature.pose.bones:
                old_name = pose_bone.name
                compare_text = old_name if match_case else old_name.lower()
                compare_old = old_text if match_case else old_text.lower()
                if compare_old in compare_text:
                    pose_bone.name = old_name.replace(old_text, new_text, 1 if match_case else -1)
        
        mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH' and obj.vertex_groups]
        group_count = 0
        
        for obj in mesh_objects:
            for old_name, new_name in renamed_bones:
                if old_name in obj.vertex_groups:
                    vgroup = obj.vertex_groups[old_name]
                    vgroup.name = new_name
                    group_count += 1
        
        action_count = 0
        for action in bpy.data.actions:
            old_action_name = action.name
            compare_action = old_action_name if match_case else old_action_name.lower()
            compare_old = old_text if match_case else old_text.lower()
            
            if compare_old in compare_action:
                action.name = old_action_name.replace(old_text, new_text, 1 if match_case else -1)
                action_count += 1
                
                for obj in bpy.data.objects:
                    if obj.animation_data and obj.animation_data.nla_tracks:
                        for track in obj.animation_data.nla_tracks:
                            for strip in track.strips:
                                if strip.name and compare_old in (strip.name.lower() if not match_case else strip.name):
                                    strip.name = strip.name.replace(old_text, new_text, 1 if match_case else -1)
                                if strip.action == action:
                                    if compare_old in (track.name.lower() if not match_case else track.name):
                                        track.name = track.name.replace(old_text, new_text, 1 if match_case else -1)
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        msg = f"Replaced '{old_text}' with '{new_text}' in {len(selected_armatures)} armatures"
        if group_count > 0:
            msg += f" and {group_count} vertex groups"
        if action_count > 0:
            msg += f" and {action_count} animations"
            
        self.report({'INFO'}, msg)
        return {"FINISHED"}

classes = (RenameBonesProps, REN_BONES_OT_operator)

def register():
    # Register property group
    bpy.types.Scene.rename_bones_props = bpy.props.PointerProperty(type=RenameBonesProps)

def unregister():
    # Unregister property group
    if hasattr(bpy.types.Scene, "rename_bones_props"):
        del bpy.types.Scene.rename_bones_props 