
import telebot as tb
import pyowm
import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = tb.TeleBot(token=f'{TELEGRAM_TOKEN}')
OWM_API_KEY = os.getenv('OWM_API_KEY')
owm = pyowm.OWM(API_key=f'{OWM_API_KEY}', language='ru')


@bot.message_handler(commands=['start'])
def command_start(message):
    bot.reply_to(message, 'Привет!')


@bot.message_handler(commands=['help'])
def command_help(message):
    bot.reply_to(message, 'Чтобы узнать прогноз погоды, просто отправь мне название города.')


@bot.message_handler(func=lambda msg: msg.text is not None)
def get_location(message):
    location = message.text.split()
    return get_weather(location)


def get_weather(location):
    obs = owm.weather_at_place(location)
    weather = obs.get_weather()
    print(weather)
    return send_weather(weather)


def send_weather(weather):
    pass


def main():
    pass


bot.polling()

if __name__ == '__main__':
    main()