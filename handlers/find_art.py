from loguru import logger as logging

from aiogram import types
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, InputFile)
from API.Imageboards import Imageboards

from init import bot, dp, engine, main


@dp.message_handler()
@dp.throttled(rate=1)
async def find_art(message: types.Message):
    for item in engine.connect().execute(main.select().where(main.c.Id == message.from_user.id)):
        obj = Imageboards(syte=item.Source)
        try:
            for source_item in obj.getImagesUrl(limit=item.Count, tags=message.text + ' order:random', s='random'):
                await bot.send_chat_action(message.chat.id, 'upload_photo')
                Download_Keyboard = InlineKeyboardMarkup()
                Download_Keyboard.row(
                    InlineKeyboardButton('Без сжатия', callback_data=item.Source + ' ' + str(source_item["id"])))
                await message.reply_photo(photo=InputFile.from_url(source_item["url"]), caption=obj.getTags(id=source_item["id"]),
                                            reply_markup=Download_Keyboard) 
            logging.info(str(message.from_user.username) + ' | ' + message.text)
        except Exception as err:
            logging.error(str(message.from_user.username) + ' | ' + message.text + ' | ' + str(err))
