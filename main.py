
import os
import random
import telebot

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("Не найден BOT_TOKEN в GitHub Secrets")

bot = telebot.TeleBot(TOKEN)

JOKES = [
    "😂 Ты так долго отвечаешь, что я успел состариться.",
    "🐢 Черепаха уже ответила быстрее тебя.",
    "🤖 Мой процессор завис от твоего сообщения.",
    "👀 Я всё вижу. Даже как ты читаешь и молчишь.",
    "🏆 Ты чемпион по откладыванию дел!",
    "😈 Не переживай, я просто троллю.",
    "📡 Алло! Чувство юмора, ты здесь?",
]

enabled_chats = set()

@bot.message_handler(commands=["start", "help"])
def start(message):
    bot.reply_to(
        message,
        "😈 Привет! Я бот троллинга!\n\n"
        "/troll — случайная шутка\n"
        "/troll_on — включить троллинг в группе\n"
        "/troll_off — выключить троллинг"
    )

@bot.message_handler(commands=["troll"])
def troll(message):
    bot.reply_to(message, random.choice(JOKES))

def is_admin(message):
    try:
        member = bot.get_chat_member(
            message.chat.id,
            message.from_user.id
        )
        return member.status in ["administrator", "creator"]
    except Exception:
        return False

@bot.message_handler(commands=["troll_on"])
def troll_on(message):
    if message.chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, "Добавь меня в группу!")
        return

    if not is_admin(message):
        bot.reply_to(message, "Только администратор может включить троллинг.")
        return

    enabled_chats.add(message.chat.id)
    bot.reply_to(message, "😈 Троллинг включён!")

@bot.message_handler(commands=["troll_off"])
def troll_off(message):
    if message.chat.type not in ["group", "supergroup"]:
        bot.reply_to(message, "Эта команда работает только в группе.")
        return

    if not is_admin(message):
        bot.reply_to(message, "Только администратор может выключить троллинг.")
        return

    enabled_chats.discard(message.chat.id)
    bot.reply_to(message, "👌 Троллинг выключен!")

@bot.message_handler(func=lambda m: (
    m.chat.type in ["group", "supergroup"]
    and m.chat.id in enabled_chats
    and bool(m.text)
    and not m.text.startswith("/")
))
def auto_troll(message):
    if random.random() < 0.15:
        bot.reply_to(message, random.choice(JOKES))

if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)

