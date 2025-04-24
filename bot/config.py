import os
from dotenv import load_dotenv

# загружаем переменные из .env
load_dotenv()  # не перезаписывает уже установленные :contentReference[oaicite:11]{index=11}

# читаем конфигурацию
TG_TOKEN        = os.getenv("TG_TOKEN")
MAYTAPI_PRODUCT = os.getenv("MAYTAPI_PRODUCT")
MAYTAPI_PHONE   = os.getenv("MAYTAPI_PHONE")
MAYTAPI_KEY     = os.getenv("MAYTAPI_KEY")
BOT_OWNER_ID    = os.getenv("BOT_OWNER_ID")

# простая валидация
if not all([TG_TOKEN, MAYTAPI_PRODUCT, MAYTAPI_PHONE, MAYTAPI_KEY]):
    raise RuntimeError("Не все обязательные переменные окружения установлены")
