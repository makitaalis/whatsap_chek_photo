# bot/maytapi_client.py
import httpx
from typing import Optional
from bot.config import MAYTAPI_PRODUCT, MAYTAPI_PHONE, MAYTAPI_KEY

BASE_URL = "https://api.maytapi.com/api"


async def get_profile_image_url(num_e164: str) -> Optional[str]:
    """
    Запрашивает у Maytapi ссылку на аватар WhatsApp.
    Принимает номер вида +79001234567, в API передаёт только цифры.
    Если data — строка (URL), возвращаем её напрямую.
    """
    number = num_e164.lstrip("+")  # Maytapi ждёт только цифры

    url = f"{BASE_URL}/{MAYTAPI_PRODUCT}/{MAYTAPI_PHONE}/getProfileImage"
    headers = {"x-maytapi-key": MAYTAPI_KEY}
    params = {"number": number}

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(url, headers=headers, params=params)
        data = resp.json()
        # для отладки можно вывести:
        # print("Maytapi JSON:", data)

    # если вообще не удалось
    if not str(data.get("success")).lower() in ("true", "1"):
        return None

    payload = data.get("data")
    # 1) если это словарь с полем image
    if isinstance(payload, dict):
        return payload.get("image")
    # 2) если это строка — считаем, что это URL
    if isinstance(payload, str) and payload.startswith("http"):
        return payload
    # иначе — нет фото
    return None
