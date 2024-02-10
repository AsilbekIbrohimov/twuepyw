from aiogram import *
import keyboard as key
import time
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
from aiogram.types import InputFile
from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                      CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                      MessageTextIsEmpty, RetryAfter,
                                      CantParseEntities, MessageCantBeDeleted)
BOT_TOKEN = ("5204190868:AAGdR_cSlHjxw8S1nkkSUyoCr3lTMivjgMw")  # Bot toekn
ADMINS = ['1024522810']  # adminlar ro'yxati type list
IP = ("ip")  # Xosting ip manzili str

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Running")

        except Exception as err:
            logging.exception(err)

async def on_sturtup_send_document(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_document(chat_id=admin, document=InputFile('d:/tdiu.txt'))

        except Exception as err:
            pass


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("sendfile", "get txt file"),
        ]
    )


@dp.errors_handler()
async def errors_handler(update, exception):
    """
    Exceptions handler. Catches all exceptions within task factory tasks.
    :param dispatcher:
    :param update:
    :param exception:
    :return: stdout logging
    """

    if isinstance(exception, CantDemoteChatCreator):
        logging.exception("Can't demote chat creator")
        return True

    if isinstance(exception, MessageNotModified):
        logging.exception('Message is not modified')
        return True
    if isinstance(exception, MessageCantBeDeleted):
        logging.exception('Message cant be deleted')
        return True

    if isinstance(exception, MessageToDeleteNotFound):
        logging.exception('Message to delete not found')
        return True

    if isinstance(exception, MessageTextIsEmpty):
        logging.exception('MessageTextIsEmpty')
        return True

    if isinstance(exception, Unauthorized):
        logging.exception(f'Unauthorized: {exception}')
        return True

    if isinstance(exception, InvalidQueryID):
        logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
        return True

    if isinstance(exception, TelegramAPIError):
        logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, RetryAfter):
        logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
        return True
    if isinstance(exception, CantParseEntities):
        logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
        return True
    
    logging.exception(f'Update: {update} \n{exception}')


@dp.message_handler(state=None, commands=['sendfile'])
async def bot_echo(message: types.Message):
    try:
        await message.answer_document(InputFile(r'd:/tdiu.txt'))
    except Exception as e:
        await message.answer(str(e))
async def on_startup(dispatcher):
    ##### Birlamchi komandalar, (/star va /help)
    await set_default_commands(dispatcher)
    await on_sturtup_send_document(dispatcher)
    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
