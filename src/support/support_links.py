import bpy
import random
import webbrowser
from bpy.types import Operator
import time

URLS = {
    "rate": "https://blendermarket.com/products/tidy-monkey/ratings",
    "github": "https://github.com/muammar-yacoob/Tidy-Monkey",
    "website": "https://spark-games.co.uk",
    "donate": "https://www.buymeacoffee.com/spark88"
}

CATEGORIES = {
    "rate": {
        "title": "Rate Addon",
        "emoji": "⭐",
        "messages": [
            "Please rate on Blender Market!",
            "Rate the addon to support future updates",
            "Enjoying Tidy Monkey? Please rate!",
        ]
    },
    "github": {
        "title": "Star on GitHub",
        "emoji": "🌟",
        "messages": [
            "Star us on GitHub!",
            "Find the code on GitHub",
            "Report issues on our GitHub repo",
        ]
    },
    "website": {
        "title": "Visit Website",
        "emoji": "🚀",
        "messages": [
            "Check more tools on our website!",
            "Visit our website for more addons",
            "Need help? Visit our website",
        ]
    },
    "donate": {
        "title": "Support Us",
        "emoji": "☕",
        "messages": [
            "Support development with a coffee!",
            "Buy us a coffee to fuel development",
            "Help support future updates",
        ]
    }
}

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
    
    if _cache["key"] is None or current_time - _cache["last_update"] > 120:
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
    pass

def unregister_support_handlers():
    pass 