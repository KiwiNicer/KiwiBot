from loguru import logger as logging

from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from init import bot, db, dp, engine, main, api
from keyboards.keyboard import (Count_ReplyKeyboard, GeneralMenu,
                                Source_Keyboard)


@dp.message_handler(commands=['settings'])
@dp.throttled(rate=1)
async def settings_command(message: types.Message):
    for item in engine.connect().execute(main.select().where(main.c.Id == message.from_user.id)):
        await message.reply("Настройте бота под себя!\nНастройки на данный момент:\n\
        Источник: " + item.Source + "\n\
        Количество артов за один запрос: " + str(item.Count), reply_markup=GeneralMenu, disable_web_page_preview=True)
    logging.info(str(message.from_user.username) + ' | ' + message.text)


@dp.message_handler(lambda c: c.text in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
async def Count_Checker(message):
    conn = engine.connect()
    conn.execute(db.update(main).where(main.c.Id == message.from_user.id).values(Count=int(message.text)))
    await bot.send_message(message.chat.id, "Успешно изменено", reply_markup=ReplyKeyboardRemove())


@dp.callback_query_handler(lambda c: c.data == 'Source')
async def Source_callback(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=Source_Keyboard)


@dp.callback_query_handler(lambda c: c.data == 'Counts')
async def Counts_callback(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.message.chat.id,
                           "Выберите количество артов, которые бот будет отправлять за раз\n",
                           reply_markup=Count_ReplyKeyboard)


@dp.callback_query_handler(lambda c: c.data in api)
async def SourceContent_callback(callback_query: types.CallbackQuery):
    conn = engine.connect()
    conn.execute(db.update(main).where(main.c.Id == callback_query.from_user.id).values(Source=callback_query.data))
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id,
                                        reply_markup=GeneralMenu)


@dp.callback_query_handler(lambda c: c.data == 'Close')
async def Close_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)


@dp.message_handler(lambda c: c.text == 'Закрыть')
async def Close_message(message):
    await message.answer('Удаляю~~', reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(message.chat.id, message.message_id + 1)


@dp.message_handler(commands=['send'])
async def send_command(message):
    if message.from_user.username == 'CakesTwix':
        for row in engine.connect().execute(db.select([main])):
            try:
                await bot.send_message(row.Id, message.text[5:])
            except:
                logging.info(str(row.Nickname) + " забанил бота у себя")
