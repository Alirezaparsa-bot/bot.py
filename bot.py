import telebot
import random
import os

TOKEN = os.environ.get("8440200479:AAG9ZI3AAGLi6zWQGHb0nlIvxGMsAcVgzzo")
bot = telebot.TeleBot(TOKEN)

user_codes = {}
code_users = {}
active_chats = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))
    user_codes[message.chat.id] = code
    code_users[code] = message.chat.id
    bot.reply_to(message, f"سلام! کد اختصاصی تو: {code}\nاین کد رو به کسی بده تا بتونه باهات ناشناس چت کنه.\nبرای اتصال به یک نفر کدش رو بفرست.")

@bot.message_handler(func=lambda msg: msg.text.upper() in code_users)
def connect_users(message):
    code = message.text.upper()
    partner_id = code_users[code]
    if partner_id == message.chat.id:
        bot.reply_to(message, "نمیتونی با خودت چت کنی!")
        return
    active_chats[message.chat.id] = partner_id
    active_chats[partner_id] = message.chat.id
    bot.send_message(partner_id, "یک نفر با کد تو وصل شد! حالا میتونید چت کنید.")
    bot.reply_to(message, "وصل شدی! حالا میتونی پیام بفرستی.")

@bot.message_handler(commands=['stop'])
def stop_chat(message):
    if message.chat.id in active_chats:
        partner_id = active_chats.pop(message.chat.id)
        active_chats.pop(partner_id, None)
        bot.send_message(partner_id, "طرف مقابل چت رو قطع کرد.")
        bot.reply_to(message, "چت قطع شد.")
    else:
        bot.reply_to(message, "تو هیچ چتی نیستی.")

@bot.message_handler(func=lambda msg: True)
def relay_message(message):
    if message.chat.id in active_chats:
        bot.send_message(active_chats[message.chat.id], message.text)

bot.infinity_polling()
