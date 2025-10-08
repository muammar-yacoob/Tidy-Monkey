"""AI-powered 3D modeling operators."""
import bpy
from bpy.types import Operator
from bpy.props import StringProperty
from ..utils.ai_service import AIService

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class AI_MODELING_OT_operator(Operator):
    """Use AI to generate 3D models based on text description"""
    bl_idname = "ai.modeling"
    bl_label = "AI 3D Modeling"
    bl_options = {'REGISTER', 'UNDO'}

    prompt: StringProperty(
        name="Description",
        description="Describe what you want to create",
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

        system_prompt = """You are an expert Blender Python programmer. Generate clean, efficient Python code to create 3D models.

Guidelines:
- Use bpy.ops and bpy.data APIs
- Create objects with proper materials when relevant
- Position objects sensibly in the scene
- Clean up any existing objects if needed
- Add comments explaining key steps
- Only return executable Python code in a code block, no explanations
- Assume the code runs in Blender 4.x context

Example format:
```python
import bpy
import math

# Your code here
```
"""

        user_prompt = f"Create a 3D model: {self.prompt}\n\nGenerate complete Blender Python code to create this."

        self.report({'INFO'}, "Generating 3D model with AI...")

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
            exec(code, {'bpy': bpy, 'math': __import__('math')})
            self.report({'INFO'}, "AI model created successfully!")
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


class AI_QUICK_MODEL_OT_operator(Operator):
    """Quick AI modeling with predefined prompts"""
    bl_idname = "ai.quick_model"
    bl_label = "Quick AI Model"
    bl_options = {'REGISTER', 'UNDO'}

    model_type: StringProperty(
        name="Model Type",
        description="Type of model to create",
        default=""
    )

    def execute(self, context):
        # Check if API key is configured
        api_key = AIService.get_api_key()
        if not api_key:
            self.report({'ERROR'}, "Please configure your AI API key in preferences")
            return {'CANCELLED'}

        prompts = {
            'chair': 'A simple modern chair with 4 legs and a backrest',
            'table': 'A rectangular table with 4 legs',
            'lamp': 'A desk lamp with a base, arm, and lampshade',
            'tree': 'A stylized low-poly tree with trunk and foliage',
            'house': 'A simple house with walls, roof, door, and windows'
        }

        prompt = prompts.get(self.model_type, self.model_type)

        # Use the main modeling operator
        bpy.ops.ai.modeling('EXEC_DEFAULT', prompt=prompt)

        return {'FINISHED'}


classes = (
    AI_MODELING_OT_operator,
    AI_QUICK_MODEL_OT_operator,
)
