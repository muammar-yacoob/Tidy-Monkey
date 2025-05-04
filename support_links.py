import bpy
import random
import os
import time

# Cache for the support message to prevent regeneration on every UI refresh
_support_cache = {
    "category_key": None,
    "category": None,
    "message": None,
    "last_update": 0,
    "sidebar_visible": False
}

# Display options
display_options = {
    # Set to True to show the support section every day
    # Set to False to only show on days divisible by 3
    "show_daily": True,
    
    "link_color": "#00BFFF",
    
    # Time in seconds before refreshing the message (86400 = 1 day)
    # For testing, you can set this to a lower value
    "cache_lifetime": 3600  # 1 hour by default
}

# Configuration
config = {
    # Your personal/project details
    "author": "Spark Games",
    "project_name": "Tidy Monkey",
    "project_repo": "Spark-Games/TidyMonkey",
    "website": "https://spark-games.co.uk",    
    
    # Your donation details
    "buy_me_coffee_username": "spark88",
}

# Link categories with their associated messages and URLs
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

# Custom URL functions for Blender
def get_rate_url():
    # For Blender addon, use the Blender Market page
    return "https://blendermarket.com/products/tidy-monkey/ratings"

def get_github_url():
    return f"https://github.com/{config['project_repo']}"

def get_website_url():
    return config["website"]

def get_donate_url(type="coffee"):
    links = {
        "coffee": f"https://www.buymeacoffee.com/{config['buy_me_coffee_username']}"
    }
    return links[type] if type in links else links["coffee"]

# Function to get a random message from an array
def get_random_message(messages):
    return messages[random.randint(0, len(messages) - 1)]

# Function to get a random category from the available options
def get_random_category(options):
    available_categories = [key for key in options if key in support_categories]
    if len(available_categories) == 0:
        return None
    
    random_key = available_categories[random.randint(0, len(available_categories) - 1)]
    return {
        "key": random_key,
        "category": support_categories[random_key]
    }

# Determine if support section should be shown today
def should_show_support_section():
    # If show_daily is True, always show the support section
    if display_options["show_daily"]:
        return True
    
    # Otherwise only show on days divisible by 3
    import datetime
    today = datetime.datetime.now()
    day = today.day
    return day % 3 == 0

# Get URL for a specific category
def get_url_for_category(category_key, url_type=None):
    if category_key == "rate":
        return get_rate_url()
    elif category_key == "github":
        return get_github_url()
    elif category_key == "website":
        return get_website_url()
    elif category_key == "donate":
        return get_donate_url(url_type)
    return ""

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

# This function will be called when the addon is registered
def register_support_handlers():
    # We'll use the depsgraph_update_post handler to detect when the sidebar state changes
    bpy.app.handlers.depsgraph_update_post.append(check_sidebar_state)

# This function will be called when the addon is unregistered
def unregister_support_handlers():
    # Remove our handler when the addon is disabled
    if check_sidebar_state in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(check_sidebar_state)

# Check if the sidebar state has changed and reset the cache if needed
def check_sidebar_state(scene, depsgraph):
    global _support_cache
    
    # Check if the sidebar is visible by looking for regions in the 3D view
    sidebar_visible = False
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'UI' and region.width > 1:
                        sidebar_visible = True
                        break
    
    # If the sidebar visibility has changed from hidden to visible, reset the cache
    if sidebar_visible and not _support_cache["sidebar_visible"]:
        reset_support_cache()
    
    # Update the sidebar visibility state
    _support_cache["sidebar_visible"] = sidebar_visible

# Create a support section in the Blender UI
def create_support_section(layout, options=["rate", "github", "website", "donate"]):
    if not should_show_support_section():
        return
    
    global _support_cache
    current_time = time.time()
    
    # Check if we need to refresh the cache
    cache_expired = (current_time - _support_cache["last_update"]) > display_options["cache_lifetime"]
    
    if cache_expired or _support_cache["category"] is None:
        # Get a random category
        random_category_info = get_random_category(options)
        if not random_category_info:
            return
        
        category_key = random_category_info["key"]
        category = random_category_info["category"]
        
        # Get a random message for this category
        message = get_random_message(category["messages"])
        
        # Update the cache
        _support_cache["category_key"] = category_key
        _support_cache["category"] = category
        _support_cache["message"] = message
        _support_cache["last_update"] = current_time
    else:
        # Use cached values
        category_key = _support_cache["category_key"]
        category = _support_cache["category"]
        message = _support_cache["message"]
    
    # Create a compact support section directly
    col = layout.column(align=True)
    col.scale_y = 0.9
    col.label(text=message)
    
    # Create a button row with the action link
    row = col.row(align=True)
    row.scale_y = 1.2
    
    # For donation, use the coffee URL
    if category_key == "donate":
        url = get_url_for_category(category_key, "coffee")
        op = row.operator("wm.url_open", text=f"{category['title']} {category['emoji']}", icon='FUND')
        op.url = url
    elif category_key == "github":
        url = get_url_for_category(category_key)
        op = row.operator("wm.url_open", text=f"{category['title']} {category['emoji']}", icon='URL')
        op.url = url
    elif category_key == "website":
        url = get_url_for_category(category_key)
        op = row.operator("wm.url_open", text=f"{category['title']} {category['emoji']}", icon='WORLD')
        op.url = url
    else:
        url = get_url_for_category(category_key)
        op = row.operator("wm.url_open", text=f"{category['title']} {category['emoji']}", icon='SOLO_ON')
        op.url = url 