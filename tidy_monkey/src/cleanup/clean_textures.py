import bpy
from bpy.types import Operator

class CLEAN_TEX_OT_operator(bpy.types.Operator):
    bl_label = "Delete Unused Textures"
    bl_idname = "deletetextures.delete"
    bl_description = "Removes unused textures"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        try: 
            purgedCount = bpy.ops.outliner.orphans_purge()
            if purgedCount > 0:
                self.report({'INFO'}, f"{purgedCount} Unused Objects were Purged")
        except:
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

classes = (CLEAN_TEX_OT_operator,) 