"""Addon preferences for AI settings."""
import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty, EnumProperty

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class TidyMonkeyPreferences(AddonPreferences):
    """Preferences for Tidy Monkey addon."""
    bl_idname = __package__.split('.')[0]

    ai_provider: EnumProperty(
        name="AI Provider",
        description="Select the AI service provider",
        items=[
            ('anthropic', 'Anthropic (Claude)', 'Use Anthropic Claude models'),
            ('openai', 'OpenAI (GPT)', 'Use OpenAI GPT models'),
        ],
        default='anthropic',
    )

    ai_model: StringProperty(
        name="Model",
        description="AI model to use (leave empty for default)",
        default="",
    )

    ai_api_key: StringProperty(
        name="API Key",
        description="API key for the selected AI provider",
        default="",
        subtype='PASSWORD',
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="AI Settings", icon='LIGHTPROBE_SPHERE')

        col = box.column()
        col.prop(self, "ai_provider")
        col.prop(self, "ai_api_key")
        col.prop(self, "ai_model")

        # Show default models
        if self.ai_provider == 'anthropic':
            col.label(text="Default: claude-3-5-sonnet-20241022", icon='INFO')
        elif self.ai_provider == 'openai':
            col.label(text="Default: gpt-4", icon='INFO')

        # Help text
        box = layout.box()
        box.label(text="How to get an API key:", icon='QUESTION')
        if self.ai_provider == 'anthropic':
            box.label(text="1. Visit https://console.anthropic.com")
            box.label(text="2. Sign up or log in")
            box.label(text="3. Go to API Keys section")
            box.label(text="4. Create a new API key")
        elif self.ai_provider == 'openai':
            box.label(text="1. Visit https://platform.openai.com")
            box.label(text="2. Sign up or log in")
            box.label(text="3. Go to API Keys section")
            box.label(text="4. Create a new API key")


classes = (TidyMonkeyPreferences,)


def register():
    """Register preferences."""
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    """Unregister preferences."""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
