from aiogram.types import KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

Source_Keyboard=InlineKeyboardMarkup()
Source_Keyboard.row( 
    InlineKeyboardButton('yande.re', callback_data='yande.re'),  
    InlineKeyboardButton('konachan.net', callback_data='konachan.net')  
) 


GeneralMenu=InlineKeyboardMarkup()
GeneralMenu.row(  
    InlineKeyboardButton('Источник', callback_data='Source'),  
    InlineKeyboardButton('Содержание арта', callback_data='Sex'),   
 ).add(InlineKeyboardButton('Закрыть', callback_data='Close')) 


Sex_Keyboard=InlineKeyboardMarkup()
Sex_Keyboard.row(  
    InlineKeyboardButton('Без хентая', callback_data='s'),  
    InlineKeyboardButton('Хентай', callback_data='e'),
    InlineKeyboardButton('Эччи', callback_data='q')   
 )


Help_tags=InlineKeyboardMarkup()
Help_tags.row(  
    InlineKeyboardButton('konachan.net', url='https://konachan.net/help/tags'),   
    InlineKeyboardButton('yande.re', url='https://yande.re/help/tags'),  
 ) 