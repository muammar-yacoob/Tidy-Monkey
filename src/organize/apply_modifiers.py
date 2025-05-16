import bpy
from bpy.types import Operator

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class APPLY_MODS_OT_operator(bpy.types.Operator):
    bl_label = "Apply Modifiers"
    bl_idname = "organize.applymodifiers"
    bl_description = "Apply all modifiers on selected objects while preserving shape keys when possible"
    bl_options = {'REGISTER', 'UNDO'}
    
    def apply_non_armature_modifiers(self, obj):
        """Helper method to apply all non-armature modifiers on an object"""
        for mod in obj.modifiers[:]:  # Iterate over a copy
            if mod.type == 'ARMATURE': continue
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                self.report({'WARNING'}, f"Could not apply {mod.name}: {str(e)}")
                try:
                    obj.modifiers.remove(mod)
                except Exception as e_rem:
                    self.report({'WARNING'}, f"Also failed to remove modifier {mod.name} after apply error: {str(e_rem)}")
        
    def execute(self, context):
        original_selection = context.selected_objects.copy()
        original_active = context.active_object
        processed = 0
        
        for obj in [o for o in context.selected_objects if o.type == 'MESH' and len(o.modifiers) > 0]:
            orig_matrix = obj.matrix_world.copy()
            
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            context.view_layer.objects.active = obj
            
            has_shape_keys = obj.data.shape_keys is not None and len(obj.data.shape_keys.key_blocks) > 0
            
            if has_shape_keys:
                shape_keys_data = []
                if obj.data.shape_keys:
                    reference_key = None
                    
                    for kb in obj.data.shape_keys.key_blocks:
                        verts_co = [v.co.copy() for v in kb.data]
                        shape_keys_data.append({
                            'name': kb.name,
                            'verts': verts_co,
                            'value': kb.value,
                            'relative_key': kb.relative_key.name if kb.relative_key else None,
                            'mute': kb.mute,
                            'slider_min': kb.slider_min,
                            'slider_max': kb.slider_max
                        })
                        if kb.name == 'Basis':
                            reference_key = kb
                
                obj.shape_key_clear()
                
                # Apply modifiers (except Armature)
                self.apply_non_armature_modifiers(obj)
                
                if len(shape_keys_data) > 0 and len(obj.data.vertices) == len(shape_keys_data[0]['verts']):
                    basis_key = obj.shape_key_add(name='Basis')
                    
                    for sk_data in shape_keys_data:
                        if sk_data['name'] == 'Basis':
                            continue

                        key = obj.shape_key_add(name=sk_data['name'])
                        key.value = sk_data['value']
                        key.mute = sk_data['mute']
                        key.slider_min = sk_data['slider_min']
                        key.slider_max = sk_data['slider_max']
                        
                        for i, co in enumerate(sk_data['verts']):
                            if i < len(key.data):
                                key.data[i].co = co
                    
                    self.report({'INFO'}, f"Successfully restored shape keys for {obj.name}")
                else:
                    self.report({'WARNING'}, f"Shape keys could not be preserved for {obj.name} - vertex count changed")
                
                processed += 1
            else:
                # Apply modifiers (except Armature)
                self.apply_non_armature_modifiers(obj)
                processed += 1
            
            obj.matrix_world = orig_matrix
        
        bpy.ops.object.select_all(action='DESELECT')
        for obj in original_selection:
            if obj:
                obj.select_set(True)
                
        if original_active:
            context.view_layer.objects.active = original_active
        
        self.report({'INFO'}, f"Applied modifiers on {processed} objects")
        return {"FINISHED"}

classes = (APPLY_MODS_OT_operator,) 