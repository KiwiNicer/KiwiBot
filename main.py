import asyncio
import hashlib
import logging

import requests
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import (InlineKeyboardButton, InlineQuery,
                           InlineQueryResultPhoto, InputTextMessageContent,
                           ReplyKeyboardRemove)
from pybooru import Danbooru, Moebooru

import Token
from handlers.find_art import find_art
from handlers.last_art import last_art
from handlers.random_art import random_art
from init import add_new_user, booru, bot, db, dp, engine, main, moebooru
from keyboards.keyboard import (Count_ReplyKeyboard, GeneralMenu, Source_Keyboard,
                      Start_ReplyKeyboard)


@dp.message_handler(commands=["start"])
@dp.message_handler(lambda c: c.text == 'Показать клавиатуру')
@dp.throttled(rate=1)
async def start_command(message: types.Message):
    add_new_user(message)
    print(message.chat.id)
    await message.answer("Хай, будь нежнее со мной, сэмпай~~", reply_markup=Start_ReplyKeyboard)
    logging.info(str(message.from_user.username) + ' | ' + message.text)


@dp.message_handler(commands=['settings'])
@dp.throttled(rate=1)
async def settings_command(message: types.Message):
    logging.info(str(message.from_user.username) + ' | ' + message.text)
    for item in engine.connect().execute(main.select().where(main.c.Id==message.from_user.id)):
        await message.reply("Настройте бота под себя!\nНастройки на данный момент:\n\
        Источник: "+item.Source + "\n\
        Количество артов за один запрос: "+str(item.Count), reply_markup=GeneralMenu)


@dp.message_handler(commands=['send'])
async def send_command(message):
    if message.from_user.username=='CakesTwix':
        for row in engine.connect().execute(db.select([main])):
            try:
                await bot.send_message(row.Id, message.text[5:])
            except:
                logging.info(str(row.Nickname) + " забанил бота у себя")


@dp.message_handler(lambda c: c.text in [str(i) for i in range(1,11)])
async def Count_Checker(message):
    conn = engine.connect()
    conn.execute(db.update(main).where(main.c.Id == message.from_user.id).values(Count=int(message.text)))
    await bot.send_message(message.chat.id, "Успешно изменено", reply_markup=Start_ReplyKeyboard)


@dp.callback_query_handler(lambda c: c.data == 'Source')
async def Source_callback(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=Source_Keyboard)


@dp.callback_query_handler(lambda c: len(c.data.split()) == 2 )
async def Download_callback(callback_query: types.CallbackQuery):
    if callback_query.data.split()[0] in booru:
        source = Danbooru(callback_query.data.split()[0])
        post = source.post_show(callback_query.data.split()[1])["file_url"]
    elif callback_query.data.split()[0] in moebooru:
        source = Moebooru(callback_query.data.split()[0])
        post = source.post_list(tags="id:"+callback_query.data.split()[1])[0]["file_url"]
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.send_chat_action(callback_query.message.chat.id, 'upload_document')
    await bot.send_document(callback_query.message.chat.id, post)
    logging.info(str(callback_query.from_user.username) + ' | Отправление арта без сжатия')


@dp.callback_query_handler(lambda c: c.data == 'Counts')
async def Counts_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
    await bot.send_message(callback_query.message.chat.id, "Выберите количество артов, которые бот будет отправлять за раз\n", reply_markup=Count_ReplyKeyboard)


@dp.callback_query_handler(lambda c: c.data in moebooru)
@dp.callback_query_handler(lambda c: c.data in booru)
async def SourceContent_callback(callback_query: types.CallbackQuery):
    conn = engine.connect()
    conn.execute(db.update(main).where(main.c.Id == callback_query.from_user.id).values(Source=callback_query.data))
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=GeneralMenu)


@dp.callback_query_handler(lambda c: c.data == 'Close')
async def Close_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)


@dp.message_handler(lambda c: c.text == 'Закрыть')
async def Close_message(message):
    await message.answer('Удаляю~~', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, message.message_id+1)


@dp.inline_handler()
async def in_last(query):
    if query.query == '': 
        PhotoTemp = []
        for item in engine.connect().execute(main.select().where(main.c.Id==query.from_user.id)):
            if item.Source in moebooru:
                source = Moebooru(item.Source)
            elif item.Source in booru:
                break
            for source_item in source.post_list(limit=20, tags='order:random rating:s', random=True): 
                PhotoTemp.append(InlineQueryResultPhoto(
                    id=source_item["id"],
                    thumb_url=source_item["sample_url"],
                    photo_url=source_item["sample_url"]))
        await bot.answer_inline_query(query.id, results=PhotoTemp, cache_time=10)
    elif len(query.query.split()) > 1:
        if query.query.split()[0] == '.last':
            PhotoTemp = []
            for item in engine.connect().execute(main.select().where(main.c.Id==query.from_user.id)):
                if item.Source in moebooru:
                    rating_tag = 'rating:s'
                    source = Moebooru(item.Source)
                elif item.Source in booru:
                    break
                for source_item in source.post_list(limit=20, tags=rating_tag): 
                    PhotoTemp.append(InlineQueryResultPhoto(
                        id=source_item["id"],
                        thumb_url=source_item["sample_url"],
                        photo_url=source_item["sample_url"]))
            await bot.answer_inline_query(query.id, results=PhotoTemp, cache_time=10)


async def shutdown(dispatcher: Dispatcher):  
    #Если вы не я - замените chat_id на свое. Я предупредил :)
    return requests.get('https://api.telegram.org/bot' + Token.token + '/sendMessage?chat_id=360862309&text=Я упаль')


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True, on_shutdown=shutdown)
