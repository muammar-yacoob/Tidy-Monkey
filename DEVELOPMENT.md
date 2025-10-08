# Development Guide for TidyMonkey

## Setup Development Environment

### 1. Create Virtual Environment (Recommended)

```bash
# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install Development Dependencies

```bash
pip install -r dev-requirements.txt
```

This installs:
- **flake8**: Style guide enforcement
- **pylint**: Advanced code analysis
- **mypy**: Static type checking
- **black**: Code formatting
- **fake-bpy-module**: Blender Python API stubs for IDE/linting

## Linting & Testing

### Quick Syntax Check

```bash
# Linux/Mac
python3 -m py_compile __init__.py src/**/*.py

# Windows
python -m py_compile __init__.py src/**/*.py
```

### Run Full Lint Suite

```bash
# Linux/Mac
./lint.sh

# Windows
lint.bat
```

This will check:
1. ✅ Python syntax errors
2. ✅ PEP 8 style compliance (flake8)
3. ✅ Code quality issues (pylint)
4. ✅ Type hints (mypy)

### Individual Tools

```bash
# Flake8 - Style checking
flake8 .

# Pylint - Code analysis
pylint src/

# MyPy - Type checking
mypy src/

# Black - Auto-formatting
black src/ --check  # Check only
black src/           # Format files
```

## Common Issues & Fixes

### Import Errors for `bpy`

The `fake-bpy-module-4.4` package provides type stubs for Blender's `bpy` module. This allows linting outside of Blender.

### Line Length

Max line length is set to 120 characters in `.flake8` and `pyproject.toml`.

### Blender-Specific Naming

Pylint is configured to ignore:
- `bl_*` naming conventions (required by Blender)
- Single-letter variable names in specific contexts
- Missing docstrings in simple operator classes

## Testing in Blender

Since this is a Blender addon, real testing must be done inside Blender:

### 1. Install Add-on for Testing

```bash
# Create a symlink (recommended for development)
# Linux/Mac
ln -s /path/to/TidyMonkey ~/.config/blender/4.4/scripts/addons/TidyMonkey

# Windows (as Administrator)
mklink /D "%APPDATA%\Blender Foundation\Blender\4.4\scripts\addons\TidyMonkey" "C:\path\to\TidyMonkey"
```

### 2. Enable Blender Console

- Windows: `Window > Toggle System Console`
- Linux/Mac: Run Blender from terminal

### 3. Check for Errors

Watch the console for:
- Import errors
- Registration errors
- Operator execution errors

### 4. Reload Add-on

After code changes:
```python
# In Blender Python console
import importlib
import sys

# Remove all TidyMonkey modules
for module_name in list(sys.modules.keys()):
    if 'TidyMonkey' in module_name or 'tidy_monkey' in module_name:
        del sys.modules[module_name]

# Then disable and re-enable the addon in preferences
```

Or use the F3 search: "Reload Scripts"

## Code Style Guidelines

### Imports
```python
import bpy
from bpy.types import Operator
from bpy.props import StringProperty
```

### Operators
```python
class MY_OT_operator(Operator):
    """Tooltip description"""
    bl_idname = "my.operator"
    bl_label = "My Operator"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Implementation
        return {'FINISHED'}
```

### Panels
```python
class MY_PT_panel(Panel):
    """Panel description"""
    bl_label = "My Panel"
    bl_idname = "MY_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tidy Monkey'

    def draw(self, context):
        layout = self.layout
        # UI code
```

## File Structure

```
TidyMonkey/
├── __init__.py              # Root registration
├── src/
│   ├── __init__.py         # Main registration
│   ├── base_panel.py       # Base UI panel
│   ├── ai_preferences.py   # Addon preferences
│   ├── ai/                 # AI features
│   │   ├── __init__.py
│   │   ├── ai_modeling.py
│   │   ├── ai_animation.py
│   │   ├── ai_lighting.py
│   │   └── ai_panel.py
│   ├── cleanup/            # Cleanup operators
│   ├── organize/           # Organize operators
│   ├── export/             # Export operators
│   └── utils/              # Utilities
│       └── ai_service.py
├── .flake8                 # Flake8 config
├── pyproject.toml          # Tool configs
├── dev-requirements.txt    # Dev dependencies
└── requirements.txt        # Runtime dependencies
```

## Pre-Commit Checklist

Before committing code:

- [ ] Run `./lint.sh` (or `lint.bat`) - all checks pass
- [ ] Test in Blender - addon loads without errors
- [ ] Test features - operators execute successfully
- [ ] Check console - no Python errors or warnings
- [ ] Update documentation if needed

## Resources

- [Blender Python API](https://docs.blender.org/api/current/)
- [Blender Add-on Tutorial](https://docs.blender.org/manual/en/latest/advanced/scripting/addon_tutorial.html)
- [PEP 8 Style Guide](https://pep8.org/)
- [fake-bpy-module](https://github.com/nutti/fake-bpy-module)

---
Happy coding! 🐒✨
