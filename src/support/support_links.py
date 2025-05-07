import bpy
import random
import webbrowser
from bpy.types import Operator
import time

# Copyright © 2023-2024 spark-games.co.uk. All rights reserved.

# Support links URLs and categories with messages
URLS = {
    "github": "https://github.com/muammar-yacoob/Tidy-Monkey",
    "donate": "https://www.buymeacoffee.com/spark88"
}

CATEGORIES = {
    "github": {
        "title": "Star on GitHub",
        "emoji": "🌟",
        "messages": [
            "Star us today!",
            "Stars wanted, apply!",
            "Star power needed!",
            "Give us stars!",
            "Stars fuel development!",
            "Please star us!",
            "Stars make smiles!",
            "Star-t supporting us!",
        ]
    },
    "donate": {
        "title": "Support Us",
        "emoji": "☕",
        "messages": [
            "Bean there, donated?",
            "Coffee fuels code!",
            "Espresso your support!",
            "Buy developer juice!",
            "Feeling brew-tiful today?",
            "Code needs caffeine!",
            "Donut deny us!",
            "Latte love appreciated!",
        ]
    }
}

# Cache for current message
_cache = {
    "key": None,
    "message": None,
    "last_update": 0
}

def get_random_support_message():
    """Get a random support message and category"""
    keys = list(CATEGORIES.keys())
    key = random.choice(keys)
    category = CATEGORIES[key]
    message = random.choice(category["messages"])
    return key, category, message

def create_support_section(layout, options=None):
    """Create the support section in the UI"""
    global _cache
    current_time = time.time()
    
    if _cache["key"] is None or current_time - _cache["last_update"] > 300:
        key, category, message = get_random_support_message()
        _cache["key"] = key
        _cache["category"] = category
        _cache["message"] = message
        _cache["last_update"] = current_time
    
    row = layout.row()
    row.alignment = 'CENTER'
    row.label(text=_cache["message"])
    
    row = layout.row()
    row.scale_y = 1.1
    url = URLS[_cache["key"]]
    op = row.operator("wm.url_open", text=f"{_cache['category']['title']} {_cache['category']['emoji']}", icon='URL')
    op.url = url

class TDMK_OT_Share(Operator):
    bl_idname = "sharelove.share"
    bl_label = "Share the love"
    bl_description = "Support Tidy Monkey development"
    
    shareType: bpy.props.StringProperty(default="YT")
    
    def execute(self, context):
        if self.shareType == "YT":
            webbrowser.open("https://www.youtube.com/@SparkGamesUK?sub_confirmation=1")
        elif self.shareType == "WB":
            webbrowser.open("https://spark-games.co.uk")
        return {'FINISHED'}

classes = (TDMK_OT_Share,)

def register():
    pass

def unregister():
    pass

def register_support_handlers():
    # Initialize the message on first load
    if _cache["key"] is None:
        key, category, message = get_random_support_message()
        _cache["key"] = key
        _cache["category"] = category
        _cache["message"] = message
        _cache["last_update"] = time.time()

def unregister_support_handlers():
    pass 