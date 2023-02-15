import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode

from app.bot_loader import bot
from app.dialogs.main.states import Main
from app.dialogs.main.parsers import PostCardData
from app.config import CHAT_ID
from app.extensions.widgets import Button

logger = logging.getLogger(__name__)


async def postcard_send(c: CallbackQuery, button: Button, dialog_manager: DialogManager):
    data: PostCardData = PostCardData.register(dialog_manager)
    text = "\n".join(data.text) or None

    if len(data.photos):
        await bot.send_photo(CHAT_ID, data.photos[0], text, has_spoiler=True)
    else:
        if text is None:
            await c.message.answer("Что-то пошло не так, "
                                   "попробуйте заново или напишите разработчику "
                                   "@mindsweeper")
            return await dialog_manager.start(Main.menu, mode=StartMode.RESET_STACK)

        await bot.send_message(CHAT_ID, f"{text}")

    await dialog_manager.start(Main.sent, mode=StartMode.RESET_STACK)
