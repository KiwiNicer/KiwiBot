import telebot
import requests

bot = telebot.TeleBot('Токен сюда')

tags = ["no_bra", "tits", "boobs", "anus", "pussy", "uncensored", "censored", "open_shirt", "trap", "yaoi", "cum",
        "penis", "milk", "pantsu", "sex"]


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, ' + message.from_user.username + ', ты написал мне /start')
    print(message)


@bot.message_handler(commands=['last'])
def photo_message(message):
    response = requests.get('https://yande.re/post.json?limit=1')
    json = response.json()

    is_18 = False
    for tag in tags:
        if tag in json[0]["tags"].split():
            is_18 = True
            break

    if is_18:
        bot.send_message(message.chat.id, "Ага, 18+")
    else:
        try:
            bot.send_photo(message.chat.id, json[0]["sample_url"])
        except Exception:
            bot.send_message(message.chat.id, "Чет тг не понрав")


bot.polling()
