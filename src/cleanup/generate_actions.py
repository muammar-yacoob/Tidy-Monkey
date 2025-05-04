import bpy
from bpy.types import Operator

class GEN_ACTS_OT_operator(bpy.types.Operator):
    bl_label = "Generate Actions"
    bl_idname = "generate.actions"
    bl_description = "Pushes Animations to the NLA Stack"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        for obj in context.selected_objects:
            if obj.animation_data and obj.animation_data.action:
                if obj.animation_data.nla_tracks:
                    already_in_nla = False
                    for track in obj.animation_data.nla_tracks:
                        if track.strips and track.strips[0].action == obj.animation_data.action:
                            already_in_nla = True
                            break
                    if not already_in_nla:
                        return True
                else:
                    return True
        return False
    
    def execute(self, context):
        original_context = bpy.context.area.type
        bpy.context.area.type = "NLA_EDITOR"
        bpy.ops.anim.channels_clean_empty()
        bpy.context.area.type = original_context

        processed_count = 0
        for obj in context.selected_objects:
            if not obj.animation_data or not obj.animation_data.action:
                continue
                
            action = obj.animation_data.action
            already_in_nla = False
            if obj.animation_data.nla_tracks:
                for track in obj.animation_data.nla_tracks:
                    if track.strips and track.strips[0].action == action:
                        already_in_nla = True
                        break
            
            if not already_in_nla:
                track_name = f"{obj.name}_Action"
                track = obj.animation_data.nla_tracks.new()
                track.name = track_name
                strip_name = f"{obj.name}_{action.name}"
                strip = track.strips.new(strip_name, int(action.frame_range[0]), action)
                obj.animation_data.action = None
                processed_count += 1
        
        if processed_count > 0:
            self.report({'INFO'}, f"Actions generated for {processed_count} objects")
        else:
            self.report({'INFO'}, "No new actions to push to NLA stack")
            
        return {"FINISHED"}

classes = (GEN_ACTS_OT_operator,) 