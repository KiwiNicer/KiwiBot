from aiogram.types import KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, \
        ReplyKeyboardMarkup

Source_Keyboard=InlineKeyboardMarkup()
Source_Keyboard.row( 
    InlineKeyboardButton('yande.re', callback_data='yande.re'),  
    InlineKeyboardButton('konachan.net', callback_data='konachan.net'),  
    InlineKeyboardButton('safebooru.org', callback_data='safebooru.org') 
) 


GeneralMenu=InlineKeyboardMarkup()
GeneralMenu.row(  
    InlineKeyboardButton('Источник', callback_data='Source'),  
    InlineKeyboardButton('Содержание арта', callback_data='Sex'),
).add(InlineKeyboardButton('Количество артов за раз', callback_data='Counts')    
).add(InlineKeyboardButton('Закрыть', callback_data='Close')) 


Sex_Keyboard=InlineKeyboardMarkup()
Sex_Keyboard.row(  
    InlineKeyboardButton('Без хентая', callback_data='s'),  
    InlineKeyboardButton('Хентай', callback_data='e'),
    InlineKeyboardButton('Эччи', callback_data='q')   
 )
Sex_Keyboard.add(InlineKeyboardButton('Без фильтрации', callback_data='n'))

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
).add(KeyboardButton('Случайный арт'))