import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardRemove
from init import add_new_user, booru, bot, db, dp, engine, main, moebooru
from keyboards.keyboard import (Count_ReplyKeyboard, GeneralMenu,
                                Source_Keyboard, Start_ReplyKeyboard)


@dp.message_handler(commands=['settings'])
@dp.throttled(rate=1)
async def settings_command(message: types.Message):
    logging.info(str(message.from_user.username) + ' | ' + message.text)
    for item in engine.connect().execute(main.select().where(main.c.Id==message.from_user.id)):
        await message.reply("Настройте бота под себя!\nНастройки на данный момент:\n\
        Источник: "+item.Source + "\n\
        Количество артов за один запрос: "+str(item.Count), reply_markup=GeneralMenu)


@dp.message_handler(lambda c: c.text in [str(i) for i in range(1,11)])
async def Count_Checker(message):
    conn = engine.connect()
    conn.execute(db.update(main).where(main.c.Id == message.from_user.id).values(Count=int(message.text)))
    await bot.send_message(message.chat.id, "Успешно изменено", reply_markup=Start_ReplyKeyboard)


@dp.callback_query_handler(lambda c: c.data == 'Source')
async def Source_callback(callback_query: types.CallbackQuery):
    await bot.edit_message_reply_markup(callback_query.message.chat.id, callback_query.message.message_id, reply_markup=Source_Keyboard)


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
