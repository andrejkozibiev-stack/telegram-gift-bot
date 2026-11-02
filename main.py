import os
import telebot

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(
        message,
        "🎁 Привет! Добро пожаловать!\n\nЯ бот подарков. Напиши мне, что ты хочешь узнать."
    )

@bot.message_handler(func=lambda message: True)
def answer(message):
    bot.reply_to(message, "🎁 Спасибо за сообщение!")

bot.infinity_polling()
