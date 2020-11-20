import logging

import requests
from aiogram import executor, types
from aiogram.types import InputMediaPhoto

import Token as Tg
from init import bot, dp
from init import engine, db, main
from init import moebooru, booru, rating


@dp.message_handler(commands=["last"])
@dp.message_handler(lambda c: c.text == 'Последний арт')
async def last_art(message: types.Message):
    for item in engine.connect().execute(main.select().where(main.c.Id==message.from_user.id)):
        if item.Source in moebooru:
            response = requests.get('https://' + item.Source + '/post.json?limit='+ str(item.Count) +'&tags=rating:'+item.Rating)
        elif item.Source in booru:
            response = requests.get('https://' + item.Source + '/index.php?page=dapi&s=post&q=index&limit=' + str(item.Count) + '&json=1' + '&tags=' + rating[item.Rating])
        json = response.json()
        try:
            if len(json) == 1:
                tag_items = ""
                await bot.send_chat_action(message.chat.id, 'upload_photo')
                for tag_item in json[0]["tags"].split():
                    tag_items += '#'+tag_item + ' '
                if item.Source in moebooru:
                    await message.reply_photo(photo= json[0]["sample_url"], caption= tag_items)
                elif item.Source in booru:
                    await message.reply_photo(photo= 'https://' + item.Source + '/images/' + json[0]["directory"] + '/'+json[0]["image"], caption= tag_items)
            else: 
                arts = []
                await bot.send_chat_action(message.chat.id, 'upload_photo')
                for arts_item in json:
                    if item.Source in moebooru:
                        arts.append(InputMediaPhoto(arts_item["sample_url"]))
                    elif item.Source in booru:
                        arts.append(InputMediaPhoto('https://' + item.Source + '/images/' + arts_item["directory"] + '/'+arts_item["image"]))
                await bot.send_media_group(message.chat.id, arts, reply_to_message_id=message.message_id)
                logging.info(str(message.from_user.username) + ' | ' + message.text)
        except Exception as err:
            await message.answer("Чет тг не понрав")
            logging.error(str(message.from_user.username) + ' | ' + message.text + ' | ' + str(err))
