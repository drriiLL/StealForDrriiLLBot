import aiogram
from aiogram import Dispatcher, Bot
from BotForStill.config import TOKEN
from aiogram.filters import Command, CommandStart
import asyncio
from aiogram.types import Message
from pyexpat.errors import messages
from aiogram.exceptions import TelegramBadRequest
from BotForStill.utils import search_one_word
from aiogram import F



bot = Bot(TOKEN)
dp = Dispatcher()
CHAT_ID = "964584467"

@dp.message(CommandStart())
async def start(message: Message):
    print(message.chat.id)
    

@dp.message(Command('find'))
async def com_search(message: Message):
    await message.answer("Введите, что хотите найти")


@dp.message(F.text)
async def handle_text(message: Message):
    user_text = (message.text).split()
    search_word = [user_text[0]] if user_text else []
    founded_files, other_dirs, other_files  = search_one_word(search_word)
    
    if founded_files:
        result_founded_str = "\n".join(founded_files)
        result_other_str = "\n".join(other_files)
        try:
            await message.answer("Искомый файл: ")
            await message.answer(result_founded_str)
            await message.answer("Остальные файлы в этой папке: ")
            await message.answer(result_other_str)
        except TelegramBadRequest as e:
            if "message is too long" in str(e):
                await message.answer(f"Найдено {len(other_files)} файлов, но список слишком длинный для отправки")
                await message.answer("Первые 5 файлов:")
                short_list = "\n".join(other_files[:5])
                await message.answer(short_list)
            else:
                await message.answer("Ошибка отправки сообщения")
    else:
        await message.answer("Файлы не найдены")
    
    # await bot.send_message(chat_id=CHAT_ID, text = result_str)



async def main():
    await bot.send_message(chat_id=CHAT_ID, text = "Bot was started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Произошла ошибка {e}")