# made by @Beingcat
from typing import List
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def chunk_list(lst: List, n: int) -> List[List]:
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def create_pagination_keyboard(modules: List[str], current_page: int, total_pages: int, texts: dict) -> InlineKeyboardMarkup:
    keyboard = []
    
    
    for i in range(0, len(modules), 3):
        row = [InlineKeyboardButton(m, callback_data=f"help_module_{m}") for m in modules[i:i + 3]]
        keyboard.append(row)

    
    nav_row = []
    if current_page > 1:
        nav_row.append(InlineKeyboardButton(texts["prev_button"], callback_data=f"help_prev_{current_page}"))
    if current_page < total_pages:
        nav_row.append(InlineKeyboardButton(texts["next_button"], callback_data=f"help_next_{current_page}"))
    
    if nav_row:
        keyboard.append(nav_row)
    
    
    if texts.get("support_as_callback") and texts.get("support_c_back_name"):
        keyboard.append([InlineKeyboardButton(texts["support_button"], callback_data=texts["support_c_back_name"])])
    else:
        keyboard.append([InlineKeyboardButton(texts["support_button"], url=texts["support_url"])])
    
    return InlineKeyboardMarkup(keyboard)
