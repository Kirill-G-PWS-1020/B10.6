import telebot
from extensions import Convert, APIException
from config import exchanges, TOKEN
import traceback

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = f"Здравствуй, чтобы начать работу,  введите команду в формате" \
           "\n<имя исходной валюты><в какую перевести><количество валюты" \
           "\nУвидеть список всех доступных валют: /value"

    bot.reply_to(message, text)

@bot.message_handler(commands=['value'])
def value(message: telebot.types.Message):
    text = 'Доступны валюты: '
    for key in exchanges.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(commands=['text'])
def conv(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров!')

        answer = Convert.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)

bot.polling(non_stop=True)
