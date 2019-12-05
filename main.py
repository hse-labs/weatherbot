import os
import re
import telebot as tb
import pyowm

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = tb.TeleBot(token=TELEGRAM_TOKEN)
OWM_API_KEY = os.getenv('OWM_API_KEY')
owm = pyowm.OWM(API_key=OWM_API_KEY, language='ru')


def get_weather(location):
    obs = owm.weather_at_place(location[0])
    w = obs.get_weather()
    status = w.get_detailed_status()
    temp = w.get_temperature(unit='celsius')
    wind = w.get_wind()
    humidity = w.get_humidity()
    pressure = w.get_pressure()
    return status, temp, wind, humidity, pressure


def set_up_daily():
    pass


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, 'Привет! Чтобы узнать, какая сейчас погода в твоем городе, отправь мне его название.')


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.reply_to(message, 'Этот бот показывает, какая сейчас погода в городе.')


@bot.message_handler(commands=['notify'])
def command_notify(message):
    bot.reply_to(message, '')


@bot.message_handler(func=lambda msg: msg.content_type == 'text')
def get_send_message(message):
    try:
        global status, temp, wind, humidity, pressure
        location = message.text.split()
        status, temp, wind, humidity, pressure = get_weather(location)
        to_send = f'{status.capitalize()}\nСредняя температура:{temp["temp"]}C\n' \
                  f'Максимальная температура:{temp["temp_max"]}C\nМинимальная температура:{temp["temp_min"]}C\n' \
                  f'Скорость ветра {wind["speed"]} м/c\nВлажность воздуха:{humidity}%\n' \
                  f'Атмосферное давление {round(pressure["press"] / 1.333)} мм рт.ст.'
        bot.reply_to(message, text='*Прогноз погоды на сегодня:\n*' + to_send, parse_mode='Markdown')
        msg = bot.reply_to(message, text='Установить ежедневные оповещения о погоде?')
        bot.register_next_step_handler(msg, notification_handler)
    except Exception as e:
        bot.reply_to(message, text='Кажется, что-то пошло не так, попробуй еще раз.')


def notification_handler(message):
    try:
        answer = message.text
        if answer.lower() == 'да':
            msg = bot.reply_to(message, text='Хорошо. В какое время присылать оповещения? \n'
                                             'Время должно быть описано в таком формате: 00:00')
            bot.register_next_step_handler(msg, time_setter)
        else:
            bot.reply_to(message, text='Приходи еще.')
    except Exception as e:
        bot.reply_to(message, text='Кажется, что-то пошло не так, попробуй еще раз.')


def time_setter(message):
    m = message.text
    print(m)
    pattern = r'(?:[0-1]?[0-9]|2[1-4])\:[0-5][0-9]'
    t = re.search(pattern, m)
    print(t)



bot.polling()


