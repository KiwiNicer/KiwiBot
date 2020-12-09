import logging

from aiogram import types
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup)
from pybooru import Danbooru, Moebooru

from init import booru, bot, dp, engine, main, moebooru


@dp.message_handler(commands=["last"])
@dp.message_handler(lambda c: c.text == 'Последний арт')
@dp.throttled(rate=1)
async def last_art(message: types.Message):
    for item in engine.connect().execute(main.select().where(main.c.Id == message.from_user.id)):
        if item.Source in moebooru:
            source = Moebooru(item.Source)
        elif item.Source in booru:
            source = Danbooru(item.Source)
        try:
            for source_item in source.post_list(limit=item.Count, tags='rating:s'):
                await bot.send_chat_action(message.chat.id, 'upload_photo')
                tag = ''
                if item.Source in moebooru:
                    for tags in source_item["tags"].split():
                        tag += '#' + tags + ' '
                    Download_Keyboard = InlineKeyboardMarkup()
                    Download_Keyboard.row(
                        InlineKeyboardButton('Без сжатия', callback_data=item.Source + ' ' + str(source_item["id"])))
                    await message.reply_photo(photo=source_item["sample_url"], caption=tag,
                                              reply_markup=Download_Keyboard)
                elif item.Source in booru:
                    for tags in source_item["tag_string"].split():
                        tag += '#' + tags + ' '
                    Download_Keyboard = InlineKeyboardMarkup()
                    Download_Keyboard.row(
                        InlineKeyboardButton('Без сжатия', callback_data=item.Source + ' ' + str(source_item["id"])))
                    await message.reply_photo(photo=source_item["large_file_url"], caption=str(tag),
                                              reply_markup=Download_Keyboard)
            logging.info(str(message.from_user.username) + ' | ' + message.text)
        except Exception as err:
            logging.error(str(message.from_user.username) + ' | ' + message.text + ' | ' + str(err))
