import requests
from bs4 import BeautifulSoup as BS
import telebot
from telebot import types
from loguru import logger

logger.add("debug.log", rotation="5 MB", compression="zip")

logger.info("Start Bot...")

URL_SARANSK = "https://yandex.ru/pogoda/?lat=54.18743515&lon=45.18393707"
URL_NIKOLAEVKA = "https://yandex.ru/pogoda/?lat=54.473539&lon=45.06033"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"}
TOKEN = "5156879953:AAEzZ1M-k-neP7jRaQORW7qC9ZuQUbtaQJI"

def parser_saransk():
    try:
        logger.info("Start Parser Saransk")
        response = requests.get(URL_SARANSK, headers=HEADERS)
        soup = BS(response.text, "html.parser")

        #Текущая погода (температура)
        weather_now = soup.find("div", class_="temp fact__temp fact__temp_size_s").find("span", class_="temp__value temp__value_with-unit")

        #Ветер
        wind = soup.find("span", class_="wind-speed")

        #Влажность
        humidity = soup.find("div", class_="term term_orient_v fact__humidity").find("div", class_="term__value")

        #Давление
        pressure = soup.find("div", class_="term term_orient_v fact__pressure").find("div", class_="term__value")

        #Погода
        clouds = soup.find("div", class_="link__feelings fact__feelings").find("div", class_="link__condition day-anchor i-bem")

        weather = soup.find("abbr", class_="icon-abbr")
    except:
        logger.error("Error getting data from Yandex")
        return parser_saransk()

    logger.info(f"Parser log: Температура: {weather_now.text} Ветер: {wind.text}{weather.text} Влажность{humidity.text} Давление: {pressure.text} Погода: {clouds.text}")
    logger.info("Stopped Parser Saransk")
    return weather_now.text, wind.text, humidity.text, pressure.text, clouds.text, weather.text

def parser_nikolaevka():
    try:
        logger.info("Start Parser Nikolaevka")
        response = requests.get(URL_NIKOLAEVKA, headers=HEADERS)
        soup = BS(response.text, "html.parser")

        #Текущая погода (температура)
        weather_now = soup.find("div", class_="temp fact__temp fact__temp_size_s").find("span", class_="temp__value temp__value_with-unit")

        #Ветер
        wind = soup.find("span", class_="wind-speed")

        #Влажность
        humidity = soup.find("div", class_="term term_orient_v fact__humidity").find("div", class_="term__value")

        #Давление
        pressure = soup.find("div", class_="term term_orient_v fact__pressure").find("div", class_="term__value")

        #Погода
        clouds = soup.find("div", class_="link__feelings fact__feelings").find("div", class_="link__condition day-anchor i-bem")

        #Ветер с какой стороны
        weather = soup.find("abbr", class_="icon-abbr")
    except:
        logger.error("Error getting data from Yandex")
        return parser_nikolaevka()

    logger.info(f"Parser log: Температура: {weather_now.text} Ветер: {wind.text}{weather.text} Влажность{humidity.text} Давление: {pressure.text} Погода: {clouds.text}")
    logger.info("Stopped Parser Nikolaevka")
    return weather_now.text, wind.text, humidity.text, pressure.text, clouds.text, weather.text

def parser_scherepovez():
    try:
        logger.info("Start Parser scherepovez")
        response = requests.get(URL_NIKOLAEVKA, headers=HEADERS)
        soup = BS(response.text, "html.parser")

        #Текущая погода (температура)
        weather_now = soup.find("div", class_="temp fact__temp fact__temp_size_s").find("span", class_="temp__value temp__value_with-unit")

        #Ветер
        wind = soup.find("span", class_="wind-speed")

        #Влажность
        humidity = soup.find("div", class_="term term_orient_v fact__humidity").find("div", class_="term__value")

        #Давление
        pressure = soup.find("div", class_="term term_orient_v fact__pressure").find("div", class_="term__value")

        #Погода
        clouds = soup.find("div", class_="link__feelings fact__feelings").find("div", class_="link__condition day-anchor i-bem")

        #Ветер с какой стороны
        weather = soup.find("abbr", class_="icon-abbr")
    except:
        logger.error("Error getting data from Yandex")
        return parser_nikolaevka()

    logger.info(f"Parser log: Температура: {weather_now.text} Ветер: {wind.text}{weather.text} Влажность{humidity.text} Давление: {pressure.text} Погода: {clouds.text}")
    logger.info("Stopped Parser scherepovez")
    return weather_now.text, wind.text, humidity.text, pressure.text, clouds.text, weather.text


bot = telebot.TeleBot(token=TOKEN)

@bot.message_handler(content_types=["text"])
def start(message):
    if message.text.lower() == "/start":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        saransk = types.KeyboardButton("Саранск")
        nikolaevka = types.KeyboardButton("Николаевка")
        scherepovez = types.KeyboardButton("Череповец")
        markup.add(saransk, nikolaevka)
        markup.add(scherepovez)
        bot.send_message(message.from_user.id, "Привет, могу тебе прислать погоду в разных городах) (нажми на кнопки с низу)", reply_markup=markup)
    elif message.text.lower() == "саранск":
        logger.info("User click Saransk")
        data = parser_saransk()
        bot.send_message(message.from_user.id, f"<b>Город</b>: Саранск\n<b>Температура</b>: {data[0]} °C\n<b>Ветер</b>: {data[1]} м/c {data[5]}\n<b>Влажность</b>: {data[2]}\n<b>Давление</b>: {data[3]}\n<b>Погода</b>: {data[4]}", parse_mode="html")
    elif message.text.lower() == "николаевка":
        logger.info("User click Nikolaevka")
        data = parser_nikolaevka()
        bot.send_message(message.from_user.id, f"<b>Деревня</b>: Николаевка\n<b>Температура</b>: {data[0]} °C\n<b>Ветер</b>: {data[1]} м/c {data[5]}\n<b>Влажность</b>: {data[2]}\n<b>Давление</b>: {data[3]}\n<b>Погода</b>: {data[4]}", parse_mode="html")
    elif message.text.lower() == "череповец":
        logger.info("User click Scherepovez")
        data = parser_scherepovez()
        bot.send_message(message.from_user.id, f"<b>Город</b>: Череповец\n<b>Температура</b>: {data[0]} °C\n<b>Ветер</b>: {data[1]} м/c {data[5]}\n<b>Влажность</b>: {data[2]}\n<b>Давление</b>: {data[3]}\n<b>Погода</b>: {data[4]}", parse_mode="html")
    else:
        bot.send_message(message.from_user.id, "Такого города я не знаю(")


if __name__ == "__main__":
    bot.polling(none_stop=True)
    logger.info("-----------------------------------Stopped Bot-----------------------------------")