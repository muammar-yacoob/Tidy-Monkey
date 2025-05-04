import bpy
import os
from bpy.types import Operator

class SHARE_OT_operator(bpy.types.Operator):
    bl_label = ""
    bl_idname = "sharelove.share"
    bl_description = "Share"   
    
    shareType: bpy.props.StringProperty(default='YT', options={'HIDDEN'})
    
    def execute(self, context):
        url = "https://blendermarket.com/products/tidy-monkey"
        if self.shareType == "YT":
            url = "https://twitter.com/intent/tweet?text=I%20Support%20TidyMonkey%20Blender%20Addon%20for%20Artists%20and%20Game%20Developers%0D%0Ahttp://www.PanettoneGames.com%20pic.twitter.com/1RuB2tqJrJ%20%0D%0A@88Spark"
        os.system("start " + url)
        return {"FINISHED"}

classes = (SHARE_OT_operator,) 