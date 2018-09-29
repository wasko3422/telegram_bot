import telebot
import config
import web
from telebot import apihelper

apihelper.proxy = {'https': '145.249.106.107:8118'}

bot = telebot.TeleBot(config.TOKEN)


def log(message, answer):
    print(" \n  =======")
    print("Name {}, Surname {}, id = {} \n Text - {}".format(message.from_user.first_name,
                                                             message.from_user.last_name,
                                                             message.from_user.id,
                                                             message.text))
    print("answer - {}".format(answer))


@bot.message_handler(func = lambda message: "/add" in message.text)
def add(message):
    bot.send_message(message.chat.id, "kek")


@bot.message_handler(func = lambda message: "/show" in message.text)
def text(message):
    answer = web.get_info(message.text.split[1:])
    log(message, answer)
    bot.send_message(message.chat.id, answer, parse_mode = "HTML")


def main():
    try:
        bot.polling()
    except:
        main()


main()
