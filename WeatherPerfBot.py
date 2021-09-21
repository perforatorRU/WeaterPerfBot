#Version 0.0.1

from pyowm import OWM
#from pyowm.utils import config
#from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
from pyowm.commons.exceptions import NotFoundError

import telebot
#from telebot import types
 
TOKEN = "1858287065:AAGBDzIEOhD7PA0fAY-0i-R7iwBzyP4qHqk"
bot = telebot.TeleBot(TOKEN)

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM('2d38c59f25faa75d0ccbd7d7ac97d013', config_dict)
mgr = owm.weather_manager()

@bot.message_handler(commands=['start'])
def welcome(message):
    city = bot.send_message(message.chat.id, "Введите название города:")

@bot.message_handler(content_types=['text'])
def Weather(message):
    city = message.text
    
    try:
        observation = mgr.weather_at_place(city)
        w = observation.weather

        deg = w.wind()['deg']
        def wind_deg_to_str(deg):
            arr = ("Север","Северо-восток","Восток", "Юго-восток","Юг","Юго-запад","Запад","Северо-запад")
            return arr[int(deg / 45)]

        atmospheric_pressure = w.pressure['press'] * 0.75 - 10

        bot.send_message(message.chat.id, f"Погода в городе {city}:")
        bot.send_message(message.chat.id, f"Температура: *{w.temperature('celsius')['temp']}*°C, ощущается как *{w.temperature('celsius')['feels_like']}*°C", parse_mode= "Markdown")
        bot.send_message(message.chat.id, f"Скорость ветра: *{w.wind()['speed']}*м/с, направление: *{wind_deg_to_str(deg)}*", parse_mode= "Markdown")
        bot.send_message(message.chat.id, f"Состояние неба: *{w.detailed_status}*, облачность *{w.clouds}*%", parse_mode= "Markdown")
        bot.send_message(message.chat.id, f"Давление: *{round(atmospheric_pressure)}* мм рт. ст.", parse_mode= "Markdown")
        bot.send_message(message.chat.id, f"Влажность: *{w.humidity}*%", parse_mode= "Markdown")
    except NotFoundError:
        bot.send_message(message.chat.id, "Ты что-то попутал...")
# RUN
bot.polling(none_stop=True)