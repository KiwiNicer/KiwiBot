from aiogram import executor
from aiogram import types
from misc import dp, bot, markup_, tags
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging
import requests

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Чтобы посмотреть арты, воспользуйся командой /last")

@dp.message_handler(commands=["last"])
async def last_command(message: types.Message):
    response = requests.get('https://yande.re/post.json?limit=1')
    json = response.json()
    global photo
    photo = json[0]["sample_url"]

    if json[0]["tags"] == 'tagme':
        await message.answer('Прости, но я не могу отправить арт в текущий момент, так как он не прошел '
                                          'постановку тегов. Это нужно мне, чтобы фильтровать 18+ контент', reply_markup=markup_())
        logging.warning(message.from_user.username + ' | ' + 'Арт с тегом tagme! Игнорирую...' + ' /last')
    else:
        is_18 = False
        for tag in tags:
            if tag in json[0]["tags"].split():
                is_18 = True
                break

        if is_18:
            print(json[0]["sample_url"])
            await message.answer(text="Ага, 18+", reply_markup=markup_())
            logging.warning(message.from_user.username + ' | ' + '18+ арт' + ' /last')
            logging.warning('Теги: ' + json[0]["tags"])
        else:
            try:
                await message.answer_photo(json[0]["sample_url"])
                logging.info(message.from_user.username + ' | ' + '/last')
            except Exception:
                await message.answer("Чет тг не понрав")

@dp.callback_query_handler(lambda callback_query: True)
async def callback(query: CallbackQuery):
    if query.data == '18':
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text="Назад", callback_data="back"))
        await query.message.delete()
        await query.message.answer_photo(photo, reply_markup=markup)
    elif query.data == 'back':
        await query.message.delete()
        #await query.message.answer(text="Чтобы посмотреть арты, воспользуйся командой /last")

if __name__ == "__main__":
	executor.start_polling(dp, skip_updates=True)