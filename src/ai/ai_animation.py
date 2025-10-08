"""AI-powered animation operators."""
import bpy
from bpy.types import Operator
from bpy.props import StringProperty, IntProperty
from ..utils.ai_service import AIService

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class AI_ANIMATION_OT_operator(Operator):
    """Use AI to generate animations based on text description"""
    bl_idname = "ai.animation"
    bl_label = "AI Animation"
    bl_options = {'REGISTER', 'UNDO'}

    prompt: StringProperty(
        name="Description",
        description="Describe the animation you want",
        default=""
    )

    duration: IntProperty(
        name="Duration (frames)",
        description="Animation duration in frames",
        default=120,
        min=1,
        max=10000
    )

    def execute(self, context):
        if not self.prompt:
            self.report({'ERROR'}, "Please enter a description")
            return {'CANCELLED'}

        # Check if there's a selected object
        if not context.selected_objects:
            self.report({'ERROR'}, "Please select an object to animate")
            return {'CANCELLED'}

        # Check if API key is configured
        api_key = AIService.get_api_key()
        if not api_key:
            self.report({'ERROR'}, "Please configure your AI API key in preferences")
            return {'CANCELLED'}

        system_prompt = """You are an expert Blender Python animator. Generate clean, efficient Python code to animate objects.

Guidelines:
- Use keyframe animation with bpy.context.object or specific objects
- Create smooth, natural animations
- Use proper interpolation
- Set keyframes at appropriate intervals
- Add comments explaining animation steps
- Only return executable Python code in a code block, no explanations
- Assume the code runs in Blender 4.x context with selected objects

Example format:
```python
import bpy

obj = bpy.context.active_object
# Your animation code here
```
"""

        obj_names = [obj.name for obj in context.selected_objects]
        user_prompt = f"""Create animation for objects: {', '.join(obj_names)}
Animation: {self.prompt}
Duration: {self.duration} frames

Generate complete Blender Python code for this animation."""

        self.report({'INFO'}, "Generating animation with AI...")

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
            self.report({'INFO'}, "AI animation created successfully!")
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
        layout.prop(self, "duration")


class AI_QUICK_ANIMATION_OT_operator(Operator):
    """Quick AI animation with predefined types"""
    bl_idname = "ai.quick_animation"
    bl_label = "Quick AI Animation"
    bl_options = {'REGISTER', 'UNDO'}

    animation_type: StringProperty(
        name="Animation Type",
        description="Type of animation to create",
        default=""
    )

    def execute(self, context):
        if not context.selected_objects:
            self.report({'ERROR'}, "Please select an object to animate")
            return {'CANCELLED'}

        # Check if API key is configured
        api_key = AIService.get_api_key()
        if not api_key:
            self.report({'ERROR'}, "Please configure your AI API key in preferences")
            return {'CANCELLED'}

        animations = {
            'bounce': 'Bouncing animation with smooth ease in/out',
            'rotate': 'Smooth 360-degree rotation around Z axis',
            'float': 'Gentle floating up and down motion',
            'pulse': 'Pulsing scale animation (grow and shrink)',
            'swing': 'Pendulum-like swinging motion'
        }

        prompt = animations.get(self.animation_type, self.animation_type)

        # Use the main animation operator
        bpy.ops.ai.animation('EXEC_DEFAULT', prompt=prompt, duration=120)

        return {'FINISHED'}


classes = (
    AI_ANIMATION_OT_operator,
    AI_QUICK_ANIMATION_OT_operator,
)
