import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', ])
def start(message: telebot.types.Message):
    text = "Привет! Хочешь Проверить курс валют?"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help', ])
def help(message: telebot.types.Message):
    text = 'Для получения курса валют введите данные \n \
в следующем формате:\n \
<имя конвертируемой валюты>,<имя итоговой валюты>,<количество>'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(',')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')
        
        answer = Convertor.get_price(*values)
    except APIException as er:
        bot.reply_to(message, f"Ошибка в команде:\n{er}" )
    except Exception as er:
        traceback.print_tb(er.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{er}" )
    else:
        bot.reply_to(message,answer)

bot.polling()
