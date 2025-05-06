import bpy
import bmesh

class CHECKER_EDGE_OT_operator(bpy.types.Operator):
    bl_label = "Checker Edge"
    bl_idname = "organize.checkeredge"
    bl_description = "Checker select edges (number of selected edges must be divisible by 3)"
    bl_options = {'REGISTER', 'UNDO'}
    
    initial_selection = []
    skip_count = 2  # Start at 2 so it skips on the first click
    
    def execute(self, context):
        obj = context.edit_object
        if not obj or obj.type != 'MESH':
            return {'CANCELLED'}
            
        bm = bmesh.from_edit_mesh(obj.data)
        
        current_selection = [e.index for e in bm.edges if e.select]
        if not current_selection:
            return {'CANCELLED'}
            
        cls = self.__class__
        
        if set(current_selection) != set(cls.initial_selection):
            cls.initial_selection = current_selection.copy()
            cls.skip_count = 2  # Start at 2 for a checker pattern on first click
        
        for e in bm.edges:
            e.select = False
        
        bm.edges.ensure_lookup_table()
        for i, idx in enumerate(cls.initial_selection):
            if i % cls.skip_count == 0:
                bm.edges[idx].select = True
        
        cls.skip_count += 1
        
        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}

classes = (CHECKER_EDGE_OT_operator,) 