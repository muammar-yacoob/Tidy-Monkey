import bpy
import random
import webbrowser
from bpy.types import Operator

# This cache will store the current support message
_support_cache = {
    "category_key": None,
    "category": None,
    "message": None,
    "sidebar_visible": False,  # Track if the sidebar was visible in previous frame
    "last_check_time": 0       # Track when we last checked visibility
}

# Support links URLs
URLS = {
    "rate": "https://blendermarket.com/products/tidy-monkey/ratings",
    "github": "https://github.com/muammar-yacoob/Tidy-Monkey",
    "website": "https://spark-games.co.uk",
    "donate": "https://www.buymeacoffee.com/spark88"
}

# Support categories with their messages
support_categories = {
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

def get_random_message(messages):
    return messages[random.randint(0, len(messages) - 1)]

def get_random_category(options):
    available_categories = [key for key in options if key in support_categories]
    if not available_categories:
        return None
    
    random_key = available_categories[random.randint(0, len(available_categories) - 1)]
    return {
        "key": random_key,
        "category": support_categories[random_key]
    }

def is_sidebar_visible():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type != 'VIEW_3D':
                continue
            for region in area.regions:
                if region.type == 'UI' and region.width > 1:
                    return True
    return False

def update_support_message():
    global _support_cache
    # Choose a random support category
    category_info = get_random_category(["rate", "github", "website", "donate"])
    if not category_info:
        return
        
    _support_cache["category_key"] = category_info["key"]
    _support_cache["category"] = category_info["category"]
    _support_cache["message"] = get_random_message(category_info["category"]["messages"])

def create_support_section(layout, options=["rate", "github", "website", "donate"]):
    global _support_cache
    
    # Force message update on every draw
    current_time = bpy.context.scene.frame_current  # Use as a proxy for time
    
    # Check if sidebar is currently visible
    current_visibility = is_sidebar_visible()
    
    # Update message when:
    # 1. Sidebar is visible and wasn't before, OR
    # 2. Sidebar is visible and it's been a while since last check (handles N key toggle)
    if (current_visibility and not _support_cache["sidebar_visible"]) or \
       (current_visibility and current_time != _support_cache["last_check_time"]):
        update_support_message()
    
    # Update tracking variables
    _support_cache["sidebar_visible"] = current_visibility
    _support_cache["last_check_time"] = current_time
    
    # If we have no message yet, generate one
    if _support_cache["message"] is None:
        update_support_message()
    
    # Get the current support info
    category_key = _support_cache["category_key"]
    category = _support_cache["category"]
    message = _support_cache["message"]
    
    if not category or not message:
        return
        
    # Create a simple compact UI
    row = layout.row()
    row.alignment = 'CENTER'
    row.label(text=message)
    
    row = layout.row()
    row.scale_y = 1.1
    url = URLS[category_key]
    op = row.operator("wm.url_open", text=f"{category['title']} {category['emoji']}", icon='URL')
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

classes = (
    TDMK_OT_Share,
)

def register():
    pass

def unregister():
    pass

def register_support_handlers():
    # No need for handlers with this simpler approach
    pass

def unregister_support_handlers():
    # No need for handlers cleanup
    pass 