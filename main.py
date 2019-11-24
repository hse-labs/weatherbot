from TOKEN import TOKEN
import telebot as tb
import pyowm


bot = tb.TeleBot(token=f'{TOKEN}')
URL = f'https://api.telegram.org/bot{TOKEN}/'
owm = pyowm.OWM(API_key='7cb6354ecb987867617b2f060da2293c', language='ru')


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
    obs = owm.weather_at_place('Москва')
    weather = obs.get_weather()
    print(weather)
    return weather


def send_weather(weather):
    pass


def main():
    get_weather()


bot.polling()

if __name__ == '__main__':
    main()