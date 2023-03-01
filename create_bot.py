from config import TOKEN_API
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(TOKEN_API)
dp = Dispatcher(bot=bot,
                storage=storage,
                )

