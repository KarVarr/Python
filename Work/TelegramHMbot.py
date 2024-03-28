import requests
import time
from datetime import datetime
import telebot
import randfacts
from googletrans import Translator
from pyzbar.pyzbar import decode
from PIL import Image
import pyzbar.pyzbar as pyzbar
# from paddleocr import PaddleOCR
import pytesseract

import matplotlib.pyplot as plt

import keras_ocr

bot = telebot.TeleBot("6137716265:AAFK0DHeAqnD-LKtwnbAYSgsAFPbOMuITvQ")
translator = Translator()

birdhday = {"Андрей": "16.06", "Карина": "10.07", "Дима": "17.06", "Богдан": "14.06", "Аршам": "29.02", "Илья": "25.11", "Карина 2": "02.08","Карен": "03.12","Анаит": "15.07"}
help = 'Для пользования ботом нужно ввести нужную команду:\n /help - подсказки\n /start - общие правила\n /bd - дни рождения\n /facts - случайный факт\n /photo - скан штрихкода'

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
    bot.reply_to(message, translation.text)
    
@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Привет, я бот ебалот для управления чем-то там... Напиши /help или иди работай дальше")

# bot.polling()
#pip install python-barcode 
#pip install "python-barcode[images]"
#pip install paddlepaddle


image = Image.open("111.jpg")

pipeline = keras_ocr.pipeline.Pipeline()
prediction_groups = pipeline.recognize(image)

for ax, image, predictions in zip(axs, image, prediction_groups):
    keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)

# decoded = decode(image_barcode)
# print(decoded[0].data.decode("utf-8"))


# barcodes = pyzbar._decode_symbols(image)

# for barcode in barcodes:
#     text = barcode.data.decode("utf-8")
#     print(text)

# ocr = "OB 0722169 001 C15"

# def convert_to_link(text):
#     result = text.replace(' ', '')[2:][:-3]
#     print(result)
#     return f"https://www2.hm.com/sv_se/productpage.{result}.html"

# convert_to_link(ocr)