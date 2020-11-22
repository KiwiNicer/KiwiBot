import logging

from pybooru import Moebooru, Danbooru
from aiogram import executor, types
from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton

import Token as Tg
from init import bot, dp
from init import engine, db, main
from init import moebooru, booru, rating


@dp.message_handler(commands=["last"])
@dp.message_handler(lambda c: c.text == 'Последний арт')
async def last_art(message: types.Message):
    global source
    for item in engine.connect().execute(main.select().where(main.c.Id==message.from_user.id)):
        if item.Source in moebooru:
            rating_tag = 'rating:' + item.Rating
            source = Moebooru(item.Source)
        elif item.Source in booru:
            if item.Rating != 'n':
                rating_tag = ' rating:' + rating[item.Rating]
            else:
                rating_tag = ''
            source = Danbooru(item.Source)
        try:
            for source_item in source.post_list(limit=item.Count, tags=rating_tag):
                await bot.send_chat_action(message.chat.id, 'upload_photo')
                tag = ''
                if item.Source in moebooru:
                    for tags in source_item["tags"].split():
                        tag += '#' + tags + ' '
                    Download_Keyboard=InlineKeyboardMarkup()
                    Download_Keyboard.row( 
                        InlineKeyboardButton('Без сжатия', callback_data=item.Source + ' ' + str(source_item["id"])))
                    await message.reply_photo(photo=source_item["sample_url"], caption=tag, reply_markup=Download_Keyboard)
                elif item.Source in booru:
                    for tags in source_item["tag_string"].split():
                        tag += '#' + tags + ' '
                    Download_Keyboard=InlineKeyboardMarkup()
                    Download_Keyboard.row( 
                        InlineKeyboardButton('Без сжатия', callback_data=item.Source + ' ' + str(source_item["id"])))
                    await message.reply_photo(photo=source_item["large_file_url"], caption=str(tag), reply_markup=Download_Keyboard)
            logging.info(str(message.from_user.username) + ' | ' + message.text)
        except Exception as err:
            logging.error(str(message.from_user.username) + ' | ' + message.text + ' | ' + str(err))
