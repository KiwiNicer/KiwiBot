from loguru import logger as logging

import requests
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputFile
#from API.Imageboards import Imageboards
from bs4 import BeautifulSoup
from init import bot, dp, engine, main

@dp.message_handler(commands=["get"])
@dp.throttled(rate=1)
async def get_command(message: types.Message):
    try:
        soup = BeautifulSoup(requests.get(message.get_args().split()[0]).text, features="html5lib")
        images = soup.findAll(id="image")
        await bot.send_chat_action(message.chat.id, 'upload_document')
        await bot.send_document(message.chat.id, images[0]['src'], reply_to_message_id=message.message_id)
        logging.info(str(message.from_user.username) + ' | Отправление арта по ссылке')
    except Exception as err:
        logging.error(str(message.from_user.username) + ' | Отправление арта по ссылке | ' + str(err))
