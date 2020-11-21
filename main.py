import asyncio
import logging

from aiogram import executor, types
from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove

from find_art import find_art
from init import add_new_user, booru, bot, db, dp, engine, main, moebooru
from keyboard import (Count_ReplyKeyboard, GeneralMenu, Sex_Keyboard,
                      Source_Keyboard, Start_ReplyKeyboard)
from last_art import last_art
from random_art import random_art


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    add_new_user(message)
    await message.answer("Хай, будь нежнее со мной, сэмпай~~", reply_markup=Start_ReplyKeyboard)
    logging.info(str(message.from_user.username) + ' | ' + message.text)


@dp.message_handler(commands=['settings'])
async def settings_command(message: types.Message):
    logging.info(str(message.from_user.username) + ' | ' + message.text)
    for item in engine.connect().execute(main.select().where(main.c.Id==message.from_user.id)):
        await message.reply("Настройте бота под себя!\nНастройки на данный момент:\n\
        Источник: "+item.Source + "\n\
        Тип артов: "+item.Rating + "\n\
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
    await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
    await bot.send_message(callback_query.message.chat.id, 'Выберите источник: ', reply_markup=Source_Keyboard)

@dp.callback_query_handler(lambda c: c.data == 'Counts')
async def Counts_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
    await bot.send_message(callback_query.message.chat.id, "Выберите количество артов, которые бот будет отправлять за раз\n", reply_markup=Count_ReplyKeyboard)


@dp.callback_query_handler(lambda c: c.data in moebooru)
@dp.callback_query_handler(lambda c: c.data in booru)
async def SourceContent_callback(callback_query: types.CallbackQuery):
    conn = engine.connect()
    conn.execute(db.update(main).where(main.c.Id == callback_query.from_user.id).values(Source=callback_query.data))
    await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
    await bot.send_message(callback_query.message.chat.id, 'Успешно изменено\nЕще что-то хотите поменять?', reply_markup=GeneralMenu)


@dp.callback_query_handler(lambda c: c.data == 'Sex')
async def Sex_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
    await bot.send_message(callback_query.message.chat.id, 'Выберите то, что хотите посмотреть и не только :)', reply_markup=Sex_Keyboard)


@dp.callback_query_handler(lambda c: c.data in ['s','e','q', 'n'])
async def SexContent_callback(callback_query: types.CallbackQuery):
    conn = engine.connect()
    conn.execute(db.update(main).where(main.c.Id == callback_query.from_user.id).values(Rating=callback_query.data))
    await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)
    await bot.send_message(callback_query.message.chat.id, 'Успешно изменено\nЕще что-то хотите поменять?', reply_markup=GeneralMenu)


@dp.callback_query_handler(lambda c: c.data == 'Close')
async def Close_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id,callback_query.message.message_id)


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True, fast=False)
