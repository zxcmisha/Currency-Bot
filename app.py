import telebot
from config import keys, TOKEN
from extensions import APIException, СurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = '''Чтобы начать работу введите команду боту в следующем формате:
<имя валюты><в какую валюту перевести><количество переводимой валюты>
Увидеть список всех доступных валют:/values'''
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = " ".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много или мало параметров')

        quote, base, amount = values
        total_base = СurrencyConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя: {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду: {e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()