import logging

import requests
from aiogram import Dispatcher, executor, types
from aiogram.types import InlineQueryResultPhoto

from API.Imageboards import Imageboards

from init import bot, dp, engine, main, initBot
import Token
from handlers.last_art import last_art
from handlers.random_art import random_art
from handlers.settings import (Close_callback, Close_message, Count_Checker,
                               Source_callback, SourceContent_callback,
                               settings_command, send_command)
from keyboards.keyboard import (Count_ReplyKeyboard, GeneralMenu,
                                Source_Keyboard, Start_ReplyKeyboard)
from handlers.start import start_command
from handlers.get_art import get_command
from handlers.find_art import find_art


@dp.callback_query_handler(lambda c: len(c.data.split()) == 2)
async def Download_callback(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.send_chat_action(callback_query.message.chat.id, 'upload_document')
    await bot.send_document(callback_query.message.chat.id, Imageboards(callback_query.data.split()[0]).getFileUrl(id=callback_query.data.split()[1]))
    logging.info(str(callback_query.from_user.username) + ' | Отправление арта без сжатия')


@dp.inline_handler()
async def in_last(query):
    if query.query == '':
        PhotoTemp = []
        for item in engine.connect().execute(main.select().where(main.c.Id == query.from_user.id)):
            if item.Source == 'https://gelbooru.com':
                random = ' sort:random'
            else:
                random = ' order:random'
            obj = Imageboards(syte=item.Source)
            for source_item in obj.getImagesUrl(limit=20, tags=random, s='random'):
                PhotoTemp.append(InlineQueryResultPhoto(
                    id=source_item["id"],
                    thumb_url=source_item["url"],
                    photo_url=source_item["url"]))
        logging.info(str(query.from_user.username) + ' | Инлайн режим | Рандом')
        await bot.answer_inline_query(query.id, results=PhotoTemp, cache_time=10)
    else:
        PhotoTemp = []
        for item in engine.connect().execute(main.select().where(main.c.Id == query.from_user.id)):
            if item.Source == 'https://gelbooru.com':
                random = ' sort:random'
            else:
                random = ' order:random'
            obj = Imageboards(syte=item.Source)
            for source_item in obj.getImagesUrl(limit=20, tags=query.query + random):
                PhotoTemp.append(InlineQueryResultPhoto(
                    id=source_item["id"],
                    thumb_url=source_item["url"],
                    photo_url=source_item["url"]))
        logging.info(str(query.from_user.username) + ' | Инлайн режим | Поиск по тегу ' + query.query)
        await bot.answer_inline_query(query.id, results=PhotoTemp, cache_time=10)


async def shutdown(dispatcher: Dispatcher):
    # Если вы не я - замените chat_id на свое. Я предупредил :)
    return requests.get('https://api.telegram.org/bot' + Token.token + '/sendMessage?chat_id=360862309&text=Я упаль')



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown, on_startup=initBot)
