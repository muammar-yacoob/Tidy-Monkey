"""AI panel for Tidy Monkey."""
import bpy
from bpy.types import Panel
from ..base_panel import TITLE_PT_panel
from ..utils.ai_service import AIService

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class AI_PT_panel(bpy.types.Panel):
    """AI Tools Panel"""
    bl_label = "AI Tools"
    bl_idname = "AI_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_parent_id = TITLE_PT_panel.bl_idname

    def draw(self, context):
        layout = self.layout

        # Check if API key is configured
        api_key = AIService.get_api_key()
        provider = AIService.get_provider()

        if not api_key:
            box = layout.box()
            box.label(text="⚠ API Key Required", icon='ERROR')
            col = box.column()
            col.label(text="Configure your AI API key in:")
            col.label(text="Edit > Preferences > Add-ons")
            col.label(text="Search 'Tidy Monkey'")
            return

        # Show current provider
        row = layout.row()
        row.label(text=f"Provider: {AIService.SUPPORTED_PROVIDERS[provider]['name']}", icon='LIGHTPROBE_SPHERE')

        # 3D Modeling Section
        box = layout.box()
        box.label(text="3D Modeling", icon='MESH_CUBE')

        col = box.column(align=True)
        col.operator("ai.modeling", text="Custom Model", icon='MESH_DATA')

        # Quick model buttons
        row = col.row(align=True)
        op = row.operator("ai.quick_model", text="Chair")
        op.model_type = "chair"
        op = row.operator("ai.quick_model", text="Table")
        op.model_type = "table"

        row = col.row(align=True)
        op = row.operator("ai.quick_model", text="Lamp")
        op.model_type = "lamp"
        op = row.operator("ai.quick_model", text="Tree")
        op.model_type = "tree"

        # Animation Section
        box = layout.box()
        box.label(text="Animation", icon='ANIM')

        selection_count = len(context.selected_objects)

        col = box.column(align=True)
        row = col.row()
        row.operator("ai.animation", text="Custom Animation", icon='KEYFRAME')
        row.enabled = selection_count > 0

        if selection_count == 0:
            col.label(text="Select object to animate", icon='INFO')
        else:
            # Quick animation buttons
            row = col.row(align=True)
            op = row.operator("ai.quick_animation", text="Bounce")
            op.animation_type = "bounce"
            op = row.operator("ai.quick_animation", text="Rotate")
            op.animation_type = "rotate"

            row = col.row(align=True)
            op = row.operator("ai.quick_animation", text="Float")
            op.animation_type = "float"
            op = row.operator("ai.quick_animation", text="Pulse")
            op.animation_type = "pulse"

        # Lighting Section
        box = layout.box()
        box.label(text="Lighting", icon='LIGHT')

        col = box.column(align=True)
        col.operator("ai.lighting", text="Custom Lighting", icon='LIGHT_SUN')

        # Quick lighting buttons
        row = col.row(align=True)
        op = row.operator("ai.quick_lighting", text="Studio")
        op.lighting_type = "studio"
        op = row.operator("ai.quick_lighting", text="Dramatic")
        op.lighting_type = "dramatic"

        row = col.row(align=True)
        op = row.operator("ai.quick_lighting", text="Sunset")
        op.lighting_type = "sunset"
        op = row.operator("ai.quick_lighting", text="Night")
        op.lighting_type = "night"

        # Help section
        box = layout.box()
        box.label(text="Tips", icon='HELP')
        col = box.column()
        col.scale_y = 0.8
        col.label(text="• Be specific in your descriptions")
        col.label(text="• Select objects before animating")
        col.label(text="• Check console for errors")


classes = (AI_PT_panel,)
