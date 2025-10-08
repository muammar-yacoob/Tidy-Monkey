"""AI Service for making API calls to various AI models."""
import bpy
import json
from typing import Optional, Dict, Any

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

class AIService:
    """Handles communication with AI model APIs."""

    SUPPORTED_PROVIDERS = {
        'anthropic': {
            'name': 'Anthropic (Claude)',
            'base_url': 'https://api.anthropic.com/v1/messages',
            'default_model': 'claude-3-5-sonnet-20241022'
        },
        'openai': {
            'name': 'OpenAI (GPT)',
            'base_url': 'https://api.openai.com/v1/chat/completions',
            'default_model': 'gpt-4'
        }
    }

    @staticmethod
    def get_api_key() -> Optional[str]:
        """Get API key from addon preferences."""
        try:
            addon_prefs = bpy.context.preferences.addons.get(__package__.split('.')[0])
            if addon_prefs and hasattr(addon_prefs.preferences, 'ai_api_key'):
                return addon_prefs.preferences.ai_api_key
        except Exception as e:
            print(f"Error getting API key: {e}")
        return None

    @staticmethod
    def get_provider() -> str:
        """Get selected AI provider from addon preferences."""
        try:
            addon_prefs = bpy.context.preferences.addons.get(__package__.split('.')[0])
            if addon_prefs and hasattr(addon_prefs.preferences, 'ai_provider'):
                return addon_prefs.preferences.ai_provider
        except Exception as e:
            print(f"Error getting provider: {e}")
        return 'anthropic'

    @staticmethod
    def get_model() -> str:
        """Get selected AI model from addon preferences."""
        try:
            addon_prefs = bpy.context.preferences.addons.get(__package__.split('.')[0])
            if addon_prefs and hasattr(addon_prefs.preferences, 'ai_model'):
                model = addon_prefs.preferences.ai_model
                if model:
                    return model
        except Exception as e:
            print(f"Error getting model: {e}")

        # Return default model for selected provider
        provider = AIService.get_provider()
        return AIService.SUPPORTED_PROVIDERS.get(provider, {}).get('default_model', 'claude-3-5-sonnet-20241022')

    @staticmethod
    def make_request(prompt: str, system_prompt: Optional[str] = None) -> Optional[str]:
        """
        Make a request to the AI API.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt for context

        Returns:
            The AI response text or None if failed
        """
        try:
            import requests
        except ImportError:
            print("Error: requests library not available. Install it with: pip install requests")
            return None

        api_key = AIService.get_api_key()
        if not api_key:
            print("Error: No API key configured")
            return None

        provider = AIService.get_provider()
        model = AIService.get_model()
        provider_info = AIService.SUPPORTED_PROVIDERS.get(provider)

        if not provider_info:
            print(f"Error: Unknown provider {provider}")
            return None

        try:
            if provider == 'anthropic':
                headers = {
                    'x-api-key': api_key,
                    'anthropic-version': '2023-06-01',
                    'content-type': 'application/json'
                }

                messages = [{'role': 'user', 'content': prompt}]

                data = {
                    'model': model,
                    'max_tokens': 4096,
                    'messages': messages
                }

                if system_prompt:
                    data['system'] = system_prompt

                response = requests.post(
                    provider_info['base_url'],
                    headers=headers,
                    json=data,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    return result.get('content', [{}])[0].get('text', '')
                else:
                    print(f"API Error {response.status_code}: {response.text}")
                    return None

            elif provider == 'openai':
                headers = {
                    'Authorization': f'Bearer {api_key}',
                    'Content-Type': 'application/json'
                }

                messages = []
                if system_prompt:
                    messages.append({'role': 'system', 'content': system_prompt})
                messages.append({'role': 'user', 'content': prompt})

                data = {
                    'model': model,
                    'messages': messages,
                    'max_tokens': 4096
                }

                response = requests.post(
                    provider_info['base_url'],
                    headers=headers,
                    json=data,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()
                    return result.get('choices', [{}])[0].get('message', {}).get('content', '')
                else:
                    print(f"API Error {response.status_code}: {response.text}")
                    return None

        except Exception as e:
            print(f"Error making AI request: {e}")
            return None

        return None

    @staticmethod
    def parse_python_code(response: str) -> Optional[str]:
        """
        Extract Python code from AI response.
        Code is expected to be in ```python code blocks.
        """
        if not response:
            return None

        # Look for code blocks
        if '```python' in response:
            parts = response.split('```python')
            if len(parts) > 1:
                code = parts[1].split('```')[0]
                return code.strip()
        elif '```' in response:
            parts = response.split('```')
            if len(parts) > 1:
                code = parts[1].split('```')[0]
                return code.strip()

        return response.strip()
