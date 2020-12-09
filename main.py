import logging

import requests
from aiogram import Dispatcher, executor, types
from aiogram.types import InlineQueryResultPhoto

from pybooru import Danbooru, Moebooru

from init import booru, bot, dp, engine, main, moebooru
import Token
from handlers.last_art import last_art
from handlers.random_art import random_art
from handlers.settings import (Close_callback, Close_message, Count_Checker,
                               Source_callback, SourceContent_callback,
                               settings_command, send_command)
from keyboards.keyboard import (Count_ReplyKeyboard, GeneralMenu,
                                Source_Keyboard, Start_ReplyKeyboard)
from handlers.start import start_command
from handlers.find_art import find_art


@dp.callback_query_handler(lambda c: len(c.data.split()) == 2)
async def Download_callback(callback_query: types.CallbackQuery):
    if callback_query.data.split()[0] in booru:
        source = Danbooru(callback_query.data.split()[0])
        post = source.post_show(callback_query.data.split()[1])["file_url"]
    elif callback_query.data.split()[0] in moebooru:
        source = Moebooru(callback_query.data.split()[0])
        post = source.post_list(tags="id:" + callback_query.data.split()[1])[0]["file_url"]
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.send_chat_action(callback_query.message.chat.id, 'upload_document')
    await bot.send_document(callback_query.message.chat.id, post)
    logging.info(str(callback_query.from_user.username) + ' | Отправление арта без сжатия')


@dp.inline_handler()
async def in_last(query):
    if query.query == '':
        PhotoTemp = []
        for item in engine.connect().execute(main.select().where(main.c.Id == query.from_user.id)):
            if item.Source in moebooru:
                source = Moebooru(item.Source)
            elif item.Source == 'danbooru':
                rating_tag = 'rating:safe ' + query.query
                source = Danbooru(item.Source)
            for source_item in source.post_list(limit=20, tags='order:random rating:s', random=True):
                if 'large_file_url' in source_item:
                    PhotoTemp.append(InlineQueryResultPhoto(
                        id=source_item["id"],
                        thumb_url=source_item["large_file_url"],
                        photo_url=source_item["large_file_url"]))
                else:
                    PhotoTemp.append(InlineQueryResultPhoto(
                        id=source_item["id"],
                        thumb_url=source_item["sample_url"],
                        photo_url=source_item["sample_url"]))
        logging.info(str(query.from_user.username) + ' | Инлайн режим | Рандом')
        await bot.answer_inline_query(query.id, results=PhotoTemp, cache_time=10)
    else:
        PhotoTemp = []
        for item in engine.connect().execute(main.select().where(main.c.Id == query.from_user.id)):
            if item.Source in moebooru:
                rating_tag = 'rating:s ' + query.query
                source = Moebooru(item.Source)
            elif item.Source == 'danbooru':
                rating_tag = 'rating:safe ' + query.query
                source = Danbooru(item.Source)
            for source_item in source.post_list(limit=20, tags=rating_tag):
                if 'large_file_url' in source_item:
                    PhotoTemp.append(InlineQueryResultPhoto(
                        id=source_item["id"],
                        thumb_url=source_item["large_file_url"],
                        photo_url=source_item["large_file_url"]))
                else:
                    PhotoTemp.append(InlineQueryResultPhoto(
                        id=source_item["id"],
                        thumb_url=source_item["sample_url"],
                        photo_url=source_item["sample_url"]))
        logging.info(str(query.from_user.username) + ' | Инлайн режим | Поиск по тегу ' + query.query)
        await bot.answer_inline_query(query.id, results=PhotoTemp, cache_time=10)


async def shutdown(dispatcher: Dispatcher):
    # Если вы не я - замените chat_id на свое. Я предупредил :)
    return requests.get('https://api.telegram.org/bot' + Token.token + '/sendMessage?chat_id=360862309&text=Я упаль')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
