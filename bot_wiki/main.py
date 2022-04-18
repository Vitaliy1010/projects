from config import TOKEN
import telebot
from telebot import types
import wikipedia as wiki
from loguru import logger

logger.add("debug.log")
try:
    bot = telebot.TeleBot(TOKEN)
except:
    logger.critical("Error TOKEN!!!")

logger.info("Start Bot")
def main():
    wiki.set_lang("RU")

    @bot.message_handler(content_types=["text"])
    def start(message):
        if message.text.lower() == "/start":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            key_start = types.KeyboardButton("/start")
            key_help = types.KeyboardButton("/help")
            markup.add(key_start, key_help)
            bot.send_message(message.chat.id, "Привет я бот wikipedia спроси у меня что либо)", reply_markup=markup)
        elif message.text.lower() == "/help":
            bot.send_message(message.chat.id, "Просто введите свой запрос)\nБез слов 'Что такое', 'Кто такой'")
        else:
            try:
                text = message.text.lower()
                otvet = wiki.summary(text)
                logger.info(f"{text} Poisk...")
                bot.send_message(message.chat.id, f"Ответ на вопрос: {otvet}")
            except:
                logger.error(f"Ответ не найден!!! {text}")
                bot.send_message(message.chat.id, f"Я не знаю что такое {text}")

if __name__ == "__main__":
    main()
    bot.polling(none_stop=True)
    logger.info("Stopped Bot")