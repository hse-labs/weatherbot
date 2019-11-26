import telebot as tb
import pyowm
import os


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


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, 'Привет! Чтобы узнать, какая сейчас погода в твоем городе, отправь мне его название.')


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.reply_to(message, 'Этот бот показывает, какая сейчас погода в городе.')


@bot.message_handler(func=lambda msg: msg.text is not None)
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
    except Exception as e:
        print(e)


bot.polling()


