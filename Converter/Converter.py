import telebot
from Config import TOKEN, key
from Utils import APIException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help(message):
    text = 'Чтобы начать работу введите команды в следующем формате:\n \
<наименование переводимой валюты> \
<валюта, в которую перводим>\
<количество>\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for i in key.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Неверное количество параметров')

        quote, base, amount = values

        text2 = CryptoConverter.get_price(quote, base, amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать комманду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {text2}'
        bot.send_message(message.chat.id, text)


bot.polling()

