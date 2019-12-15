import os
from re import fullmatch
from collections import namedtuple
import schedule
import telebot as tb
import pyowm


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = tb.TeleBot(token=TELEGRAM_TOKEN)
OWM_API_KEY = os.getenv('OWM_API_KEY')
owm = pyowm.OWM(API_key=OWM_API_KEY, language='ru')
WEATHER_TUPLE = namedtuple('weather', ['status', 'temp', 'wind', 'humidity', 'pressure'])
user_dict = {}


def owm_weather(location):
    obs = owm.weather_at_place(location[0])
    w = obs.get_weather()
    weather = WEATHER_TUPLE(status=w.get_detailed_status(), temp=w.get_temperature(), wind=w.get_wind(),
                            humidity=w.get_humidity(), pressure=w.get_pressure())
    return weather


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, 'Привет! Чтобы узнать, какая сейчас погода в твоем городе, отправь мне его название.')


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.reply_to(message, 'Этот бот показывает, какая сейчас погода в городе.')


@bot.message_handler(func=lambda msg: msg.content_type == 'text')
def weather_sender(message):
    global chat_id
    try:
        chat_id = message.chat.id
        print(chat_id)
        location = message.text.split()
        user_dict[chat_id] = {'location': location[0]}
        weather = owm_weather(location)
        message_to_send = f'{weather.status.capitalize()}\nСредняя температура:{weather.temp["temp"]}C\n' \
                          f'Максимальная температура:{weather.temp["temp_max"]}C\n' \
                          f'Минимальная температура:{weather.temp["temp_min"]}C/n' \
                          f'Скорость ветра {weather.wind["speed"]} м/c\n' \
                          f'Влажность воздуха:{weather.humidity}%\n' \
                          f'Атмосферное давление {round(weather.pressure["press"] / 1.333)} мм рт.ст.'
        bot.reply_to(message, text='*Прогноз погоды на сегодня:\n*' + message_to_send, parse_mode='Markdown')
        msg = bot.reply_to(message, text='Установить ежедневные оповещения о погоде?')
        bot.register_next_step_handler(msg, notification_setter)
    except Exception as e:
        print(e)
        bot.reply_to(message, text='Кажется, что-то пошло не так, попробуй еще раз.')


def notification_setter(message):
    answer = message.text
    if answer.lower() == 'да':
        msg = bot.reply_to(message, text='Хорошо. В какое время присылать оповещения?')
        bot.register_next_step_handler(msg, time_setter)
    else:
        bot.reply_to(message, text='Приходи еще!')


def time_setter(message):
    t = message.text
    pattern = r'[0-2][0-9]\:[0-5][0-9]'
    check_valid_time = fullmatch(pattern, t)
    if check_valid_time:
        user_dict[chat_id].update({'time': t})
        print(user_dict)
        set_up_daily(t)
        bot.reply_to(message, text='Установлены ежедневные оповещения в {}'.format(t))
        bot.register_next_step_handler(message, automatic_weather_sender, t)
    else:
        bot.reply_to(message, text='Кажется, что-то пошло не так, попробуй еще раз.')


def automatic_weather_sender(t):
    location = user_dict[chat_id]['location']
    weather = owm_weather(location)
    message_to_send = f'{weather.status.capitalize()}\nСредняя температура:{weather.temp["temp"]}C\n' \
                      f'Максимальная температура:{weather.temp["temp_max"]}C\n' \
                      f'Минимальная температура:{weather.temp["temp_min"]}C/n' \
                      f'Скорость ветра {weather.wind["speed"]} м/c\n' \
                      f'Влажность воздуха:{weather.humidity}%\n' \
                      f'Атмосферное давление {round(weather.pressure["press"] / 1.333)} мм рт.ст.'
    bot.send_message(chat_id, text='*Прогноз погоды на сегодня:\n*' + message_to_send, parse_mode='Markdown')


def set_up_daily(t):
    schedule.every().day.at(t).do(automatic_weather_sender)


bot.polling()
