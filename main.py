import telebot
import requests
import xml.etree.cElementTree as ET

bot = telebot.TeleBot('Токен сюда')

tags=["no_bra", "tits", "boobs", "anus", "pussy", "uncensored", "censored", "open shirt", "trap", "yaoi", "cum", "penis", "milk", "pantsu","sex"] 

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Привет, '+message.from_user.username+', ты написал мне /start')
	print(message)
@bot.message_handler(commands=['last'])
def photo_message(message):
	response = requests.get('https://yande.re/post.json?limit=1')
	Json = response.json()
	print(Json[0]["tags"])
	for tagsx in tags:
		if (tagsx in Json[0]["tags"].split()):
			bot.send_message(message.chat.id,"Ага, 18+")
			break
		else:
			#print(Json)
			try:
				#print(tags in Json[0]["tags".split()])
				bot.send_photo(message.chat.id, Json[0]["sample_url"])    
			except:
				bot.send_message(message.chat.id, "Чет тг не понрав")
		break
bot.polling()

