import logging

from aiogram import executor, types
from aiogram.types import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton
from pybooru import Danbooru, Moebooru

import Token as Tg
from init import booru, bot, db, dp, engine, main, moebooru, rating
from keyboard import Help_tags


@dp.message_handler(commands=["find"])
async def find_art(message: types.Message):
    global source
    for item in engine.connect().execute(main.select().where(main.c.Id==message.from_user.id)):
        if item.Source in moebooru:
            rating_tag = ' order:random rating:' + item.Rating
            source = Moebooru(item.Source)
        elif item.Source in booru:
            if item.Rating != 'n':
                rating_tag = ' order:random rating:' + rating[item.Rating]
            else:
                rating_tag = ' order:random'
            source = Danbooru(item.Source)
        try:
            if message.get_args() == '':
                await message.answer("Поиск по тегам, гайд", reply_markup=Help_tags)
                break
            if source.post_list(limit=item.Count, tags=message.get_args() + rating_tag, random=True) == []:
                await message.answer("Ничего не найдено")
                break
            for source_item in source.post_list(limit=item.Count, tags=message.get_args() + rating_tag, random=True):
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

