from loguru import logger as logging

from aiogram import types
from init import add_new_user, dp
from keyboards.keyboard import Start_ReplyKeyboard


@dp.message_handler(commands=["start"])
@dp.message_handler(lambda c: c.text == 'Показать клавиатуру')
@dp.throttled(rate=1)
async def start_command(message: types.Message):
    add_new_user(message)
    await message.answer("Хай, будь нежнее со мной, сэмпай~~", reply_markup=Start_ReplyKeyboard)
    logging.info(str(message.from_user.username) + ' | ' + message.text)
