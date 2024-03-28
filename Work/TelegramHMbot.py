import requests
import time
from datetime import datetime
import telebot
import randfacts
from googletrans import Translator


bot = telebot.TeleBot("6137716265:AAFK0DHeAqnD-LKtwnbAYSgsAFPbOMuITvQ")
translator = Translator()

birdhday = {"Андрей": "16.06", "Карина": "10.07", "Дима": "17.06", "Богдан": "14.06", "Аршам": "29.02", "Илья": "25.11", "Карина 2": "02.08","Карен": "03.12","Анаит": "15.07"}
help = 'Для пользования ботом нужно ввести нужную команду:\n /help - подсказки\n /start - общие правила\n /bd - дни рождения\n /facts - случайный факт'

def bd():
    message = "Дни рождения:\n"
    for name, day in birdhday.items():
        message += f"{name}: {day}\n"
    return message

@bot.message_handler(commands=['bd'])
def send_birthday(message):
    bot.reply_to(message, bd())


# def send_msg(message):
#     TOKEN = "6137716265:AAFK0DHeAqnD-LKtwnbAYSgsAFPbOMuITvQ"
#     chat_id = "677863095"
#     url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
#     result = requests.get(url).json()
#     print(result)
    
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, help)

@bot.message_handler(commands=['facts'])
def facts(message):
    fact = randfacts.get_fact(False)
    translation = translator.translate(fact, dest='ru')
    bot.reply_to(message, translation)
    
@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Привет, я бот ебалот для управления чем-то там... Напиши /help или иди работай дальше")

bot.polling()






