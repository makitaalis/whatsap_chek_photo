# bot/handlers.py

import re
import os
import phonenumbers
import httpx

from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command

from bot.maytapi_client import get_profile_image_url

router = Router()

RAW_PHONE_RE    = re.compile(r"[^\d+]")
PHONE_FILTER_RE = re.compile(r"\+?\d{7,15}")

# папка для сохранённых фото
IMG_DIR = "downloaded_avatars"
os.makedirs(IMG_DIR, exist_ok=True)


def to_e164(text: str) -> str | None:
    clean = RAW_PHONE_RE.sub("", text)
    if not clean.startswith("+"):
        clean = "+" + clean
    try:
        pn = phonenumbers.parse(clean, None)
        if phonenumbers.is_possible_number(pn):
            return phonenumbers.format_number(
                pn, phonenumbers.PhoneNumberFormat.E164
            )
    except phonenumbers.NumberParseException:
        pass
    return None


@router.message(Command("start"))
async def cmd_start(msg: Message):
    await msg.answer(
        "👋 Отправьте номер телефона (например, +79001234567 или 9001234567), "
        "я сохраню его аватар WhatsApp и перешлю вам."
    )


@router.message(F.text.regexp(PHONE_FILTER_RE))
async def profile_photo_handler(msg: Message):
    num = to_e164(msg.text)
    if not num:
        return await msg.reply(
            "❌ Не смог распознать номер. Попробуйте ещё раз."
        )

    # 1) Получаем URL из Maytapi
    url = await get_profile_image_url(num)
    if not url:
        return await msg.reply("👀 Фото недоступно или контакт скрыт.")

    # 2) Скачиваем картинку и сохраняем на диск
    filename = f"{num.lstrip('+')}.jpg"
    filepath = os.path.join(IMG_DIR, filename)

    try:
        async with httpx.AsyncClient(timeout=20) as dl:
            resp = await dl.get(url)
            resp.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(resp.content)
    except httpx.HTTPError as e:
        return await msg.reply(f"⚠️ Ошибка при загрузке фото: {e}")

    # 3) Отправляем файл в Telegram через FSInputFile
    try:
        file = FSInputFile(filepath)
        await msg.answer_photo(
            photo=file,
            caption=f"Фото профиля WhatsApp для {num}"
        )
    except Exception as e:
        await msg.reply(f"⚠️ Не удалось отправить фото из файла: {e}")

    # 4) (Опционально) удалить файл после отправки
    # try:
    #     os.remove(filepath)
    # except OSError:
    #     pass


@router.message()
async def fallback(msg: Message):
    await msg.reply(
        "❌ Я понимаю только номера телефонов. "
        "Пример: +12345678901 или 12345678901."
    )
