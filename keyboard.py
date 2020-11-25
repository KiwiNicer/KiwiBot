from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)

Source_Keyboard=InlineKeyboardMarkup()
Source_Keyboard.row( 
    InlineKeyboardButton('yande.re', callback_data='yandere'),  
    InlineKeyboardButton('konachan.net', callback_data='konachan'), 
    InlineKeyboardButton('danbooru.donmai.us', callback_data='danbooru') 
).add(InlineKeyboardButton('lolibooru.moe', callback_data='lolibooru')) 


GeneralMenu=InlineKeyboardMarkup()
GeneralMenu.row(  
    InlineKeyboardButton('Источник', callback_data='Source'),  
).add(InlineKeyboardButton('Количество артов за раз', callback_data='Counts')    
).add(InlineKeyboardButton('Закрыть', callback_data='Close')) 


Help_tags=InlineKeyboardMarkup()
Help_tags.row(  
    InlineKeyboardButton('konachan.net', url='https://konachan.net/help/tags'),   
    InlineKeyboardButton('yande.re', url='https://yande.re/help/tags'), 
 ) 


Count_ReplyKeyboard = ReplyKeyboardMarkup().row(
    KeyboardButton('1'), KeyboardButton('2'), KeyboardButton('3')
).add(KeyboardButton('4'),KeyboardButton('5'),KeyboardButton('6')
).add(KeyboardButton('7'),KeyboardButton('8'),KeyboardButton('9'), KeyboardButton('10'))


Start_ReplyKeyboard = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton('Последний арт')
).add(KeyboardButton('Случайный арт')
).add(KeyboardButton('Закрыть'))
