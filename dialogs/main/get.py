from aiogram.types import Message, ContentType
from aiogram_dialog import Dialog, DialogManager

from dialogs.main.parsers import PostCardData
from dialogs.main.states import Main
from src.utils import get_id_from_message, MEDIA


async def getter(dialog_manager: DialogManager, **kwargs):
    data: PostCardData = PostCardData.register(dialog_manager)
    return {
        "user": data.username,
        "dialog_error": data.dialog_error,
    }


async def user_data(m: Message, d: Dialog, dialog_manager: DialogManager):
    data: PostCardData = PostCardData.register(dialog_manager)
    if not m.text:
        data.dialog_error = 'Ошибка! Нет текста.'
        return

    data.username = m.text.strip()
    await dialog_manager.switch_to(Main.get_postcard)


async def postcard_data(m: Message, d: Dialog, dialog_manager: DialogManager):
    data: PostCardData = PostCardData.register(dialog_manager)
    text, photos, messages = data.text, data.photos, data.messages

    if m.content_type == ContentType.TEXT:
        text.append(m.text)
    elif m.content_type in MEDIA:
        if m.caption is not None:
            text.append(m.caption)
        photos.append(get_id_from_message(m))
    else:
        data.dialog_error = "Принимаем только текст, фото или видео"
        return

    data.dialog_error = ''
    data.message_id = m.message_id
    data.text = text
    data.photos = photos

    await dialog_manager.switch_to(Main.click_send)
