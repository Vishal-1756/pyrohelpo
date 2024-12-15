# Helpo 📚

![Image](https://socialify.git.ci/Vishal-1756/pyrohelpo/image?description=1&font=KoHo&name=1&owner=1&pattern=Charlie%20Brown&theme=Dark)

A powerful and flexible pagination library for Pyrogram bots that automatically handles help commands and module organization.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![PyPI Downloads](https://static.pepy.tech/badge/pyrohelpo)

## Features ✨

- 🔄 Automatic module discovery and help text organization
- 📱 Beautiful paginated help menus with inline buttons
- 🎯 Support for both command-based and button-based help
- 🎨 Customizable button layouts and texts
- 🔌 Easy integration with existing Pyrogram bots
- 📝 Support for rich media in help messages (photos, videos)
- 🔗 Deep linking support for direct access to help menus
- 🌐 Group chat support with private message options
- 🎭 Flexible parse mode selection
- 🖼️ Media support with photo and video options

## Installation 🚀

```bash
pip install pyrohelpo
```

## Usage ⚙️

### Basic Setup

```python
from pyrogram import Client
from Helpo import Helpo
from pyrogram.enums import ParseMode

# Initialize your Pyrogram client
app = Client("my_bot")

# Initialize Helpo
helpo = Helpo(
    client=app,
    modules_path="plugins",
    buttons_per_page=6
)
```

### Advanced Configuration

```python
json 
custom_texts = {
    "help_menu_title": "**🛠 Custom Help Menu**",
    "help_menu_intro": "Available modules ({count}):\n{modules}\n\nTap on a module to explore.",
    "module_help_title": "**🔍 Details for {module_name} Module**",
    "module_help_intro": "Description:\n{help_text}",
    "no_modules_loaded": "⚠️ No modules available at the moment.",
    "back_button": "◀️ Go Back",
    "prev_button": "⬅️ Previous Page",
    "next_button": "➡️ Next Page",
    "support_button": "💬 Contact Support",
    "support_url": "https://t.me/YourSupportBot",
    "short_help": True,
    "support_as_callback": True,
    "support_c_back_name": "say_hi"
}

helpo = Helpo(
    client=app,
    modules_path="plugins",
    buttons_per_page=6,
    texts=custom_texts,
    help_var="HELP",
    module_var="MODULE",
    photo="path/to/photo.jpg",  # Optional: Add photo to help messages
    video="path/to/video.mp4",  # Optional: Add video to help messages
    parse_mode=ParseMode.HTML,  # Optional: Change parse mode (default: MARKDOWN)
    disable_web_page_preview=False,  # Optional: Enable web preview (default: True)
    short_help=True  # Optional: Enable short help mode
)
```

### Module Setup

Create Python files in your modules directory with the following structure:

```python
MODULE = "Admin"  # Module name displayed in help menu
HELP = """
**Admin Commands**
/ban - Ban a user
/unban - Unban a user
/mute - Mute a user
/unmute - Unmute a user
"""
```

### Custom Class Implementation

```python
from pyrogram import Client
from Helpo import Helpo

class Bot(Client):
    def __init__(self):
        super().__init__(
            "my_bot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN
        )
        self.helpo = Helpo(
            client=self,
            modules_path="plugins",
            buttons_per_page=6,
            texts=custom_texts
        )

    async def start(self):
        await super().start()
        print("Bot Started")
        print(f"Loaded Modules: {', '.join(self.helpo.modules.keys())}")

    async def stop(self):
        await super().stop()
        print("Bot Stopped")
```

### Group Chat Support

Helpo automatically handles group chats by providing options to:

- View help menu in private chat
- View help menu directly in the group
- Customize group chat behavior through the texts dictionary

### Deep Linking Support

```python
@app.on_message(filters.command("start"))
async def start_command(client, message):
    if len(message.text.split()) > 1:
        param = message.text.split(None, 1)[1]
        if param == "help":
            await client.show_help_menu(message.chat.id)
    else:
        await message.reply("Welcome! Use /help to see available commands.")
```

### Monkeypatch Client

To automatically handle the `/help` command in your bot, you can use the `monkeypatch_client` method:

```python
from pyrogram import Client
from Helpo import Helpo

app = Client("my_bot")

helpo = Helpo(
    client=app,
    modules_path="plugins",
    buttons_per_page=6,
    texts=custom_texts
)

helpo.monkeypatch_client()

app.run()
```

## Methods and Attributes 📚

### Helpo Class

#### Attributes:

- `client`: Pyrogram Client instance
- `modules_path`: Path to modules directory
- `buttons_per_page`: Number of buttons per page
- `help_var`: Variable name for help text (default: "**HELP**")
- `module_var`: Variable name for module name (default: "**MODULE**")
- `photo`: Optional photo URL/path
- `video`: Optional video URL/path
- `parse_mode`: Message parse mode
- `disable_web_page_preview`: Web preview setting
- `texts`: Customizable text dictionary
- `short_help`: Boolean to enable short help mode

#### Methods:

- `load_modules()`: Loads all modules from the specified path
- `show_help_menu(chat_id: int, page: int = 1, message_id: int = None)`: Displays the main help menu
- `show_module_help(query_or_message, module_name: str)`: Shows help for a specific module
- `send_message(chat_id: int, text: str, reply_markup: InlineKeyboardMarkup = None, message_id: int = None)`: Sends a message with optional media and keyboard
- `monkeypatch_client()`: Patches the Pyrogram client to handle the `/help` command

## Error Handling

Helpo includes comprehensive error handling for:

- Invalid module files
- Missing required attributes
- Media loading failures
- Message sending errors
- Callback query processing

## Contributors 👥

- [vishal-1756](https://github.com/vishal-1756)
- [siyu-xd](https://github.com/siyu-xd)

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support 🤝

Need help? Join our [support chat](https://t.me/Blank_Advice) or create an issue on our [GitHub repository](https://github.com/Vishal-1756/Helpo).

## Image Gallery 🖼️

---

Made with ❤️ by the Helpo team
<!---
# made by @Beingcat
--->