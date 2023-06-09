import telebot
from config import currency,cur_city, TOKEN
from extensions import APIException, CurrencyConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help_command(message: telebot.types.Message):
    text = '*Чтобы начать работу введите команду в следующем формате:*\n"Доллар Рубль 100"\n<имя валюты, цену которой хотите узнать> \
<имя валюты, в которой надо узнать цену первой валюты> \
<количество первой валюты> (одной цифрой без пробела)\n \n *Чтобы увидеть список валют:* /values'
    bot.reply_to(message, text, parse_mode= 'Markdown')


@bot.message_handler(commands=['values'])
def values_command(message: telebot.types.Message):
    text = '*Доступные валюты:*'
    for cur,city in cur_city.items():
        text = '\n'.join((text, cur + ' ' + city))
    bot.reply_to(message, text, parse_mode= 'Markdown')


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) < 3:
            raise APIException('Слишком мало аргументов. Команда должна быть в формате: *Валюта* *Валюта* *Количество*\n \
Посмотреть правила: /help')
        if len(values) > 3:
            raise APIException('Слишком много аргументов. Команда должна быть в формате: *Валюта* *Валюта* *Количество*\n \
Посмотреть правила: /help')

        for v in range(len(values)):
            values[v] = values[v].capitalize()

        base, quote, amount = values
        convert_result = CurrencyConverter.get_pice(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'{amount} {currency[base]} = {convert_result} {currency[quote]}'
        bot.reply_to(message, text)


bot.polling()
