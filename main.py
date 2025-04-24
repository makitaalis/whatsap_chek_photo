import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config import TG_TOKEN
from bot.handlers import router

# логирование
logging.basicConfig(level=logging.INFO,
                    format="%(levelname)s:%(message)s")

bot = Bot(TG_TOKEN)               # создаём Bot
dp = Dispatcher()                 # создаём Dispatcher :contentReference[oaicite:15]{index=15}
dp.include_router(router)         # подключаем наши хэндлеры

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))  # запускаем polling
