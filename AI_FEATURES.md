# AI Features for Tidy Monkey

Tidy Monkey now includes powerful AI capabilities to assist with 3D modeling, animation, and lighting setup!

## Prerequisites

### 1. Install Python Requests Library

The AI features require the `requests` library. Install it in Blender's Python environment:

**Windows:**
```bash
cd "C:\Program Files\Blender Foundation\Blender 4.4\4.4\python\bin"
python.exe -m pip install requests
```

**macOS:**
```bash
cd /Applications/Blender.app/Contents/Resources/4.4/python/bin
./python3.11 -m pip install requests
```

**Linux:**
```bash
cd /path/to/blender/4.4/python/bin
./python3.11 -m pip install requests
```

### 2. Get an AI API Key

Choose one of the supported AI providers:

#### Anthropic (Claude) - Recommended
1. Visit https://console.anthropic.com
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

#### OpenAI (GPT)
1. Visit https://platform.openai.com
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (starts with `sk-`)

### 3. Configure API Key in Blender

1. Open Blender
2. Go to `Edit > Preferences > Add-ons`
3. Search for "Tidy Monkey"
4. Expand the add-on preferences
5. Select your AI provider (Anthropic or OpenAI)
6. Paste your API key
7. (Optional) Enter a specific model name, or leave empty for default

## Features

### 🎨 AI 3D Modeling

Generate 3D models from text descriptions!

**Quick Models:**
- Chair
- Table
- Lamp
- Tree
- House

**Custom Models:**
Click "Custom Model" and describe what you want:
- "A medieval castle with towers"
- "A modern sports car"
- "A coffee mug with steam"

### 🎬 AI Animation

Animate selected objects with AI!

**Quick Animations:**
- Bounce - Bouncing with smooth ease
- Rotate - 360° rotation
- Float - Gentle up/down motion
- Pulse - Scale pulsing
- Swing - Pendulum motion

**Custom Animations:**
1. Select object(s) to animate
2. Click "Custom Animation"
3. Describe the animation:
   - "Spin while moving in a circle"
   - "Slowly grow and change color"
   - "Wobble like jelly"

### 💡 AI Lighting

Create professional lighting setups instantly!

**Quick Lighting:**
- Studio - Three-point lighting
- Dramatic - High contrast shadows
- Sunset - Warm golden hour
- Night - Cool moonlight
- Soft - Even product lighting

**Custom Lighting:**
Click "Custom Lighting" and describe:
- "Moody blue lighting from above"
- "Warm campfire lighting"
- "Bright daylight through window"

## Tips for Best Results

1. **Be Specific**: More detailed descriptions yield better results
   - ❌ "make a chair"
   - ✅ "create a modern office chair with wheels and armrests"

2. **For Animation**: Always select the object first

3. **Check Console**: If something fails, check Blender's console (Window > Toggle System Console on Windows) for error messages

4. **Iterative Approach**: Start with quick presets, then use custom prompts for refinement

5. **API Costs**: Be aware that API calls cost money. Quick models are fast and cheap, complex requests take longer and cost more.

## Troubleshooting

### "Please configure your AI API key"
- Go to Edit > Preferences > Add-ons > Tidy Monkey
- Enter your API key

### "requests library not available"
- Install the requests library (see Prerequisites above)
- Restart Blender after installation

### "Error executing generated code"
- Check the console for detailed error
- Try simplifying your prompt
- The AI might have generated code incompatible with your Blender version

### Generated models/animations look wrong
- Try being more specific in your description
- Use quick presets as starting points
- Complex requests may require multiple attempts

## Security Note

Your API key is stored in Blender's preferences. Keep your API key secure and never share it. The add-on only sends your text prompts to the AI service - no scene data or files are uploaded.

## Examples

### Example 1: Create a Scene
1. Click "AI Tools" panel
2. Use "Table" quick model
3. Use "Chair" quick model 4 times
4. Position chairs around table
5. Use "Studio" lighting

### Example 2: Animate a Logo
1. Import/create your logo
2. Select it
3. Click "Custom Animation"
4. Enter: "Rotate 360 degrees while scaling up from 0, then pulse gently"
5. Set duration: 120 frames

### Example 3: Product Shot
1. Import product model
2. Use "Soft" lighting
3. Adjust camera angle
4. Use "Custom Lighting" to add rim light: "Add a subtle blue rim light from the back right"

## Support

For issues and feature requests, visit: https://github.com/muammar-yacoob/Tidy-Monkey/issues

---
Copyright © 2023-2024 spark-games.co.uk. All rights reserved.
