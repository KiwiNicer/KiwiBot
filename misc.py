import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

bot = Bot(token='')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

tags = ["no_bra", "tits", "boobs", "anus", "pussy", "uncensored", "censored", "open_shirt", "trap", "yaoi", "cum",
        "penis", "milk", "pantsu", "sex", "cleavage"]

def markup_():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text="Показать 18+ 🤤", callback_data="18"))
    return markup
