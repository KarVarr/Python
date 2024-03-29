import telebot
from telebot import types
import randfacts
from googletrans import Translator
from PIL import Image
from main import text_recognition

bot = telebot.TeleBot("6137716265:AAFK0DHeAqnD-LKtwnbAYSgsAFPbOMuITvQ")
translator = Translator()

birdhday = {"Андрей": "16.06", "Карина": "10.07", "Дима": "17.06", "Богдан": "14.06", "Аршам": "29.02", "Илья": "25.11", "Карина 2": "02.08","Карен": "03.12","Анаит": "15.07"}

def bd():
    message = "Дни рождения:\n"
    for name, day in birdhday.items():
        message += f"{name}: {day}\n"
    return message

@bot.message_handler(commands=['bd'])
def send_birthday(message):
    bot.reply_to(message, bd())

@bot.message_handler(commands=['facts'])
def facts(message):
    fact = randfacts.get_fact(False)
    translation = translator.translate(fact, dest='ru')
    bot.reply_to(message, translation.text)
    
@bot.message_handler(commands=['start'])
def send_help(message):
    bot.reply_to(message, "Привет, я бот ебалот для управления чем-то там... Напиши /help или иди работай дальше")

@bot.message_handler(commands=['help'])
def send_photo_with_button(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_photo = types.KeyboardButton('Скан штрихкода')
    button_bd = types.KeyboardButton('Дни рождения')
    button_facts = types.KeyboardButton('Случайный факт')
    button_start = types.KeyboardButton('Как пользоваться')
    markup.add(button_photo, button_bd, button_facts, button_start)
    bot.send_message(message.chat.id, "Выберите команду:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Скан штрихкода')
def handle_scan(message):
    bot.reply_to(message, "Вы выбрали скан штрихкода.")

@bot.message_handler(func=lambda message: message.text == 'Дни рождения')
def handle_bd(message):
    send_birthday(message)

@bot.message_handler(func=lambda message: message.text == 'Случайный факт')
def handle_facts(message):
    facts(message)

@bot.message_handler(func=lambda message: message.text == 'Как пользоваться')
def handle_help(message):
    send_help(message)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.reply_to(message, "Фотография получена. Обработка началась...")
        bot.send_chat_action(message.chat.id, 'typing')
    
        photo = message.photo[-1]  
        file_id = photo.file_id  
        file_info = bot.get_file(file_id) 
        file = bot.download_file(file_info.file_path) 

        with open("photo.jpg", "wb") as photo_file:
            photo_file.write(file)

        recognized_text = text_recognition('photo.jpg')
        # bot.reply_to(message, f"[Link H&M: ](https://www2.hm.com/pl_pl/productpage.{recognized_text}.html)")
        if recognized_text != "Штрихкод не распознан!":
            bot.reply_to(message, f"[Link H&M: ](https://www2.hm.com/pl_pl/productpage.{recognized_text}.html)")
        else:
            bot.reply_to(message, recognized_text)
    except Exception as e:
        print(f"Ошибка при обработке фото: {e}")
        bot.reply_to(message, "Плохое качество фотографии, попробоуйте снова!")
    
bot.polling(non_stop=True)

