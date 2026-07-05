from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("🖼 Generate Placeholder", callback_data="nav_create_place")],
        [InlineKeyboardButton("📚 Creation History", callback_data="nav_view_history"),
         InlineKeyboardButton("❓ Help Manual", callback_data="nav_view_help")]
    ]
    return InlineKeyboardMarkup(keyboard)

