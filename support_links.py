import bpy
import random
import os
import time

_support_cache = {
    "category_key": None,
    "category": None,
    "message": None,
    "last_update": 0,
    "sidebar_visible": False
}

display_options = {
    "show_daily": True,  
    "link_color": "#00BFFF",
    "cache_lifetime": 3600  
}

URLS = {
    "rate": "https://blendermarket.com/products/tidy-monkey/ratings",
    "github": "https://github.com/muammar-yacoob/Tidy-Monkey",
    "website": "https://spark-games.co.uk",
    "donate": "https://www.buymeacoffee.com/spark88"
}

support_categories = {
    "rate": {
        "title": "Rate Addon",
        "emoji": "⭐",
        "messages": [
            "Please Rate & feed my ego! 🧠",
            "Dev stayed up late. Please Rate! 🦉",
            "5 stars = fewer bugs, happier monkeys 🐒",
            "Every star delays AI stealing my job 🤖⭐",
            "Your rating keeps this monkey tidy 🐵",
            "Be the smile behind the code. Please Rate 😁"
        ]
    },

    "github": {
        "title": "Star on GitHub",
        "emoji": "🌟",
        "messages": [
            "One GitHub star = one coder smile 😄",
            "GitHub stars = free dev snacks 🍩",
            "Give repo stars, I power up like Mario ⭐",
            "Found it useful? Star the repo to share! ✨"
        ]
    },

    "website": {
        "title": "More Awesome Tools",
        "emoji": "🚀",
        "messages": [
            "More tools? Visit my site for free goodies! 🎁",
            "Like this? I've got more at my website 🔎",
            "Don't stop here. Browse more Blender tools 🚀",
        ]
    },

    "donate": {
        "title": "Support Development",
        "emoji": "☕",
        "messages": [
            "Help a dev eat more than ramen! 🍜",
            "The AI didn't write this msg & I need to eat 🍔",
            "Dev low on fuel! Donate coffee? ⛽",
            "Human devs need snacks too 🍪",
            "Each donation = human > AI 🏆",
            "Fuel my code, fund my sanity ☕🧘‍♂️"
        ]
    }
}

# Function to get a random message from an array
def get_random_message(messages): return messages[random.randint(0, len(messages) - 1)]

# Function to get a random category from the available options
def get_random_category(options):
    available_categories = [key for key in options if key in support_categories]
    if not available_categories: return None
    
    random_key = available_categories[random.randint(0, len(available_categories) - 1)]
    return {
        "key": random_key,
        "category": support_categories[random_key]
    }

# Determine if support section should be shown today
def should_show_support_section():
    if display_options["show_daily"]: return True
    import datetime
    return datetime.datetime.now().day % 3 == 0

# Reset the cache when needed
def reset_support_cache():
    global _support_cache
    _support_cache = {
        "category_key": None,
        "category": None,
        "message": None,
        "last_update": 0,
        "sidebar_visible": _support_cache.get("sidebar_visible", False)
    }

def check_sidebar_state(scene, depsgraph):
    global _support_cache
    
    sidebar_visible = False
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type != 'VIEW_3D': continue
            for region in area.regions:
                if region.type == 'UI' and region.width > 1:
                    sidebar_visible = True
                    break
    
    if sidebar_visible and not _support_cache["sidebar_visible"]: reset_support_cache()
    
    _support_cache["sidebar_visible"] = sidebar_visible

def create_support_section(layout, options=["rate", "github", "website", "donate"]):
    if not should_show_support_section(): return
    
    global _support_cache
    current_time = time.time()
    
    cache_expired = (current_time - _support_cache["last_update"]) > display_options["cache_lifetime"]
    
    if cache_expired or _support_cache["category"] is None:
        random_category_info = get_random_category(options)
        if not random_category_info: return
        
        _support_cache["category_key"] = random_category_info["key"]
        _support_cache["category"] = random_category_info["category"]
        _support_cache["message"] = get_random_message(random_category_info["category"]["messages"])
        _support_cache["last_update"] = current_time
    
    category_key = _support_cache["category_key"]
    category = _support_cache["category"]
    message = _support_cache["message"]
    
    col = layout.column(align=True)
    col.scale_y = 0.9
    col.label(text=message)
    
    row = col.row(align=True)
    row.scale_y = 1.2
    
    url = URLS[category_key]
    op = row.operator("wm.url_open", text=f"{category['title']} {category['emoji']}", icon='COMMUNITY')
    op.url = url

# Called on register
def register_support_handlers(): bpy.app.handlers.depsgraph_update_post.append(check_sidebar_state)

# Called on unregister
def unregister_support_handlers(): if check_sidebar_state in bpy.app.handlers.depsgraph_update_post: bpy.app.handlers.depsgraph_update_post.remove(check_sidebar_state) 