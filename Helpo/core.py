import os
import importlib
from typing import List, Dict, Any, Optional
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Message
from Helpo.helpers import chunk_list, create_pagination_keyboard
from pyrogram.enums import ParseMode, ChatType
from pyrogram import types

print(f"Helpo Working Perfectly! If You Liked Our Library Star our repo: https://github.com/Vishal-1756/Helpo")

class Helpo:
    def __init__(
        self,
        client: Client,
        modules_path: str,
        buttons_per_page: int = 6,
        help_var: str = "__HELP__",
        module_var: str = "__MODULE__",
        texts: Dict[str, str] = None,
        photo: Optional[str] = None,
        video: Optional[str] = None,
        parse_mode: Optional[ParseMode] = ParseMode.MARKDOWN,
        disable_web_page_preview: bool = True
    ):
        if photo and video:
            raise ValueError("You can only set either 'photo' or 'video' attribute to Helpo")
        self.client = client
        self.modules_path = modules_path
        self.buttons_per_page = buttons_per_page
        self.help_var = help_var
        self.module_var = module_var
        self.photo = photo
        self.video = video
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview
        self.texts = {
            "help_menu_title": "**📚 Help Menu**",
            "help_menu_intro": "Loaded {count} modules:\n{modules}\n\nClick on a module to see its help message.",
            "module_help_title": "**📘 {module_name} Module**",
            "module_help_intro": "{help_text}",
            "no_modules_loaded": "No modules loaded.",
            "back_button": "🔙 Back",
            "prev_button": "⬅️ Previous",
            "next_button": "Next ➡️",
            "support_button": "👥 Support",
            "support_url": "https://t.me/Xlzeo",
            "group_help_message": "Click The Button To Access Help",
            "group_pvt_button": "See In Pvt",
            "group_pvt_url": "https://t.me/{(self.client.get_me()).username}?start=help",
            "group_open_here": "Open Here"
        }
        if texts:
            self.texts.update(texts)
        self.modules: Dict[str, Dict[str, Any]] = {}
        self.short_help = texts.get("short_help", False)
        self.support_as_callback = texts.get("support_as_callback", False)
        self.support_c_back_name = texts.get("support_c_back_name", None)
        self.load_modules()
        self.monkeypatch_client()

    def load_modules(self):
        for filename in os.listdir(self.modules_path):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                try:
                    module = importlib.import_module(f"{self.modules_path.replace('/', '.')}.{module_name}")
                    if not hasattr(module, self.help_var) or not hasattr(module, self.module_var):
                        missing_attr = self.help_var if not hasattr(module, self.help_var) else self.module_var
                        raise ValueError(f"Module {module_name} is missing the required attribute '{missing_attr}'.")
                
                    self.modules[getattr(module, self.module_var)] = {
                        'name': getattr(module, self.module_var),
                        'help': getattr(module, self.help_var)
                    }
                except Exception as e:
                    print(f"Failed to load module {module_name}: {str(e)}")
        print(f"Loaded {len(self.modules)} modules: {', '.join(self.modules.keys())}")
    
    def monkeypatch_client(self):
        @self.client.on_message(filters.command("help"))
        async def help_command(client, message):
            args = message.text.split()[1:]
            if args and self.short_help:
                module_name = args[0]
                if module_name in self.modules:
                    await self.show_module_help(message, module_name)
                else:
                    await message.reply("Module not found.")
                return

            if message.chat.type in [ChatType.SUPERGROUP, ChatType.GROUP]:
                buttons = [
                    [
                        InlineKeyboardButton(
                            self.texts["group_pvt_button"],
                            url=self.texts["group_pvt_url"]
                        ),
                        InlineKeyboardButton(
                            self.texts["group_open_here"],
                            callback_data="global_help"
                        ),
                    ]
                ]
                keyboard = InlineKeyboardMarkup(buttons)
                await message.reply(
                    self.texts["group_help_message"],
                    reply_markup=keyboard
                )
            else:
                await self.show_help_menu(message.chat.id)
       
        @self.client.on_callback_query(filters.regex(r'^help_'))
        async def help_button(client, callback_query: CallbackQuery):
            data = callback_query.data.split('_')
            if data[1] == 'module':
                await self.show_module_help(callback_query, data[2])
            elif data[1] in ['next', 'prev']:
                page = int(data[2])
                if data[1] == 'next':
                    page += 1
                else:
                    page -= 1
                await self.show_help_menu(callback_query.message.chat.id, page, callback_query.message.id)
            elif data[1] == 'back':
                await self.show_help_menu(callback_query.message.chat.id, message_id=callback_query.message.id)
       
        @self.client.on_callback_query(filters.regex(r'^global_help$'))
        async def global_help(client, callback_query: CallbackQuery):
            await self.show_help_menu(callback_query.message.chat.id, message_id=callback_query.message.id)
              
        self.client.show_help_menu = self.show_help_menu
        
    async def show_help_menu(self, chat_id: int, page: int = 1, message_id: int = None):
        modules_list = list(self.modules.keys())
        chunks = list(chunk_list(modules_list, self.buttons_per_page))
        if not chunks:
            text = self.texts["no_modules_loaded"]
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(self.texts["support_button"], url=self.texts["support_url"])]]
            )
        else:
            if page > len(chunks):
                page = 1
            elif page < 1:
                page = len(chunks)

            keyboard = create_pagination_keyboard(
                chunks[page - 1], page, len(chunks), self.texts
            )

            text = f"{self.texts['help_menu_title']}\n\n{self.texts['help_menu_intro'].format(count=len(self.modules), modules=', '.join(self.modules.keys()))}"

        await self.send_message(chat_id, text, reply_markup=keyboard, message_id=message_id)

    async def show_module_help(self, query_or_message, module_name: str):
        module = self.modules.get(module_name)
        if module:
            text = f"{self.texts['module_help_title'].format(module_name=module['name'])}\n\n{self.texts['module_help_intro'].format(help_text=module['help'])}"
            keyboard = InlineKeyboardMarkup(
                [[InlineKeyboardButton(self.texts["back_button"], callback_data="help_back")]]
            )
            if isinstance(query_or_message, CallbackQuery):
                await query_or_message.edit_message_text(text, reply_markup=keyboard)
            else:
                await query_or_message.reply(text, reply_markup=keyboard)
        else:
            if isinstance(query_or_message, CallbackQuery):
                await query_or_message.answer("Module not found!", show_alert=True)
            else:
                await query_or_message.reply("Module not found!")

    async def send_message(self, chat_id: int, text: str, reply_markup: InlineKeyboardMarkup = None, message_id: int = None):
        try:
            if self.photo:
                if message_id:
                    await self.client.edit_message_media(
                        chat_id=chat_id,
                        message_id=message_id,
                        media=types.InputMediaPhoto(media=self.photo, caption=text),
                        reply_markup=reply_markup
                    )
                else:
                    await self.client.send_photo(
                        chat_id=chat_id,
                        photo=self.photo,
                        caption=text,
                        reply_markup=reply_markup,
                        parse_mode=self.parse_mode
                    )
            elif self.video:
                if message_id:
                    await self.client.edit_message_media(
                        chat_id=chat_id,
                        message_id=message_id,
                        media=types.InputMediaVideo(media=self.video, caption=text),
                        reply_markup=reply_markup
                    )
                else:
                    await self.client.send_video(
                        chat_id=chat_id,
                        video=self.video,
                        caption=text,
                        reply_markup=reply_markup,
                        parse_mode=self.parse_mode
                    )
            else:
                if message_id:
                    await self.client.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=text,
                        reply_markup=reply_markup,
                        parse_mode=self.parse_mode,
                        disable_web_page_preview=self.disable_web_page_preview
                    )
                else:
                    await self.client.send_message(
                        chat_id=chat_id,
                        text=text,
                        reply_markup=reply_markup,
                        parse_mode=self.parse_mode,
                        disable_web_page_preview=self.disable_web_page_preview
                    )
        except Exception as e:
            print(f"Failed to send help message to chat {chat_id}: {str(e)}") 
