from api import my_api
import telebot
import os
import randfacts
from googletrans import Translator
from PIL import Image
import pytesseract

bot = telebot.TeleBot(my_api.telegram_bot)
translator = Translator()

birdhday = {"Андрей": "16.06",
             "Карина": "10.07", 
             "Дима": "17.06",
             "Богдан": "14.06", 
             "Аршам": "29.02", 
             "Илья": "25.11", 
             "Карина 2": "02.08",
             "Карен": "03.12",
             "Анаит": "15.07"}

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
#     TOKEN = my_api.telegram_bot
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

path = os.getcwd()
print(path)
image_path = "/usr/local/bin/python3 /Users/karenvardanian/Desktop/Python/Work/111.jpg"
# image1 = Image.open("../Work/111.jpg")
# image = Image.open("./111.jpg")
# image2 = Image.open("123.jpg")
image3 = Image.open(image_path)

text = pytesseract.image_to_string(image3)

print(text)
# pipeline = keras_ocr.pipeline.Pipeline()
# prediction_groups = pipeline.recognize(image)

# for ax, image, predictions in zip(axs, image, prediction_groups):
#     keras_ocr.tools.drawAnnotations(image=image, predictions=predictions, ax=ax)

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