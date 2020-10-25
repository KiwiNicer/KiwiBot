import telebot
import requests
import xml.etree.cElementTree as ET

bot = telebot.TeleBot('1012306043:AAG9Gr-QUXn4xX5iKIg5xAKl-M9kfTyNeKg')

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Привет, '+message.from_user.username+', ты написал мне /start')
	print(message)
@bot.message_handler(commands=['last'])
def photo_message(message):
	response = requests.get('https://yande.re/post.json?limit=1')
	Json = response.json()
	print(Json[0]["sample_url"])
	try:
		bot.send_photo(message.chat.id, Json[0]["sample_url"])    
	except:		
		bot.send_message(message.chat.id, "Чет тг не понрав")
bot.polling()

