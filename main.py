import asyncio
import logging

import requests
from aiogram import executor, types
from keyboard import GeneralMenu, Source_Keyboard, Sex_Keyboard

from init import bot, dp, add_new_user, Sources, engine, db, main
from last_art import last_art
from random_art import random_art


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    add_new_user(message)
    await message.answer("Чтобы посмотреть арты, воспользуйся командой /last")


@dp.message_handler(commands=['settings'])
async def settings_command(message: types.Message):
    logging.info(str(message.from_user.username) + ' | ' + message.text)
    await message.reply("Настройте бота под себя!", reply_markup=GeneralMenu)


@dp.callback_query_handler(lambda c: c.data == 'Source')
async def Source_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Выберите источник: ', reply_markup=Source_Keyboard)


@dp.callback_query_handler(lambda c: c.data in Sources)
async def SourceContent_callback(callback_query: types.CallbackQuery):
    conn = engine.connect()
    conn.execute(db.update(main).where(main.c.Id == callback_query.from_user.id).values(Source=callback_query.data))
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Успешно изменено', reply_markup=GeneralMenu)


@dp.callback_query_handler(lambda c: c.data == 'Sex')
async def Sex_callback(callback_query: types.CallbackQuery):
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Выберите то, что хотите посмотреть и не только :)', reply_markup=Sex_Keyboard)


@dp.callback_query_handler(lambda c: c.data in ['s','e','q'])
async def SexContent_callback(callback_query: types.CallbackQuery):
    conn = engine.connect()
    conn.execute(db.update(main).where(main.c.Id == callback_query.from_user.id).values(Rating=callback_query.data))
    await bot.delete_message(callback_query.from_user.id,callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Успешно изменено', reply_markup=GeneralMenu)


if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)
