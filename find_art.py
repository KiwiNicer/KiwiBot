import logging

import requests
from aiogram import executor, types
from aiogram.types import InputMediaPhoto

import Token as Tg
from init import bot, dp
from init import engine, db, main
from keyboard import Help_tags


@dp.message_handler(commands=["find"])
async def find_art(message: types.Message):
    for item in engine.connect().execute(main.select().where(main.c.Id==message.from_user.id)):
        response = requests.get('https://' + item.Source + '/post.json?limit=' + str(item.Count) + '&tags=rating:'+item.Rating + ' order:random ' + message.get_args())
        json = response.json()
        if json == []:
            await message.answer("Ничего не найдено")
            break
        if message.get_args() == '':
            await message.answer("Поиск по тегам, гайд", reply_markup=Help_tags)
            break
        try:
            if len(json) == 1:
                tag_items = ""
                await bot.send_chat_action(message.chat.id, 'upload_photo')
                for tag_item in json[0]["tags"].split():
                    tag_items += '#'+tag_item + ' '
                await message.reply_photo(photo= json[0]["sample_url"], caption= tag_items)
            else: 
                arts = []
                await bot.send_chat_action(message.chat.id, 'upload_photo')
                for arts_item in json:
                    arts.append(InputMediaPhoto(arts_item["sample_url"]))
                await bot.send_media_group(message.chat.id, arts, reply_to_message_id=message.message_id)
                logging.info(str(message.from_user.username) + ' | ' + message.text)
        except Exception:
            await message.answer("Чет тг не понрав")
            logging.error(str(message.from_user.username) + ' | ' + message.text)
