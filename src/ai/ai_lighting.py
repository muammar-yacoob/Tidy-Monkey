"""AI-powered lighting setup operators."""
import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from ..utils.ai_service import AIService

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class AI_LIGHTING_OT_operator(Operator):
    """Use AI to generate lighting setups based on text description"""
    bl_idname = "ai.lighting"
    bl_label = "AI Lighting Setup"
    bl_options = {'REGISTER', 'UNDO'}

    prompt: StringProperty(
        name="Description",
        description="Describe the lighting setup you want",
        default=""
    )

    def execute(self, context):
        if not self.prompt:
            self.report({'ERROR'}, "Please enter a description")
            return {'CANCELLED'}

        # Check if API key is configured
        api_key = AIService.get_api_key()
        if not api_key:
            self.report({'ERROR'}, "Please configure your AI API key in preferences")
            return {'CANCELLED'}

        system_prompt = """You are an expert Blender lighting artist and Python programmer. Generate clean, efficient Python code to create lighting setups.

Guidelines:
- Use different light types (POINT, SUN, SPOT, AREA) as appropriate
- Set proper light strength/energy values
- Position lights effectively
- Set appropriate colors for mood
- Consider shadows and render engine settings
- Add comments explaining lighting choices
- Clean up existing lights if needed
- Only return executable Python code in a code block, no explanations
- Assume the code runs in Blender 4.x context

Example format:
```python
import bpy

# Your lighting setup code here
```
"""

        user_prompt = f"Create lighting setup: {self.prompt}\n\nGenerate complete Blender Python code for this lighting."

        self.report({'INFO'}, "Generating lighting setup with AI...")

        # Make AI request
        response = AIService.make_request(user_prompt, system_prompt)

        if not response:
            self.report({'ERROR'}, "Failed to get AI response")
            return {'CANCELLED'}

        # Extract code from response
        code = AIService.parse_python_code(response)

        if not code:
            self.report({'ERROR'}, "No valid code in AI response")
            return {'CANCELLED'}

        # Execute the generated code
        try:
            exec(code, {'bpy': bpy})
            self.report({'INFO'}, "AI lighting setup created successfully!")
            return {'FINISHED'}
        except Exception as e:
            self.report({'ERROR'}, f"Error executing generated code: {str(e)}")
            print(f"Generated code:\n{code}")
            print(f"Error: {e}")
            return {'CANCELLED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "prompt")


class AI_QUICK_LIGHTING_OT_operator(Operator):
    """Quick AI lighting with predefined setups"""
    bl_idname = "ai.quick_lighting"
    bl_label = "Quick AI Lighting"
    bl_options = {'REGISTER', 'UNDO'}

    lighting_type: StringProperty(
        name="Lighting Type",
        description="Type of lighting setup to create",
        default=""
    )

    def execute(self, context):
        # Check if API key is configured
        api_key = AIService.get_api_key()
        if not api_key:
            self.report({'ERROR'}, "Please configure your AI API key in preferences")
            return {'CANCELLED'}

        setups = {
            'studio': 'Three-point studio lighting setup with key, fill, and rim lights',
            'dramatic': 'Dramatic lighting with strong shadows and high contrast',
            'sunset': 'Warm sunset/golden hour lighting',
            'night': 'Night scene with cool moonlight',
            'soft': 'Soft, even lighting for product visualization'
        }

        prompt = setups.get(self.lighting_type, self.lighting_type)

        # Use the main lighting operator
        bpy.ops.ai.lighting('EXEC_DEFAULT', prompt=prompt)

        return {'FINISHED'}


classes = (
    AI_LIGHTING_OT_operator,
    AI_QUICK_LIGHTING_OT_operator,
)
