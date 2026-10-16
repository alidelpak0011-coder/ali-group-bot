import telebot

# کدهای تنظیم شده با توکن ارسالی شما
BOT_TOKEN = "8827172526:AAHuPKfl_df5b_xY41AE0WrF01PRfVaQkf8"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "سلام صاحب من! ربات مدیریت گروه زنده و آماده کار است. 🚀")

@bot.message_handler(func=lambda message: True)
def check_links(message):
    if message.chat.type in ['group', 'supergroup']:
        text = message.text or message.caption
        if text and ("http" in text or "t.me" in text or "@" in text):
            chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
            if chat_member.status not in ['administrator', 'creator']:
                try:
                    bot.delete_message(message.chat.id, message.message_id)
                    bot.send_message(message.chat.id, f"🗣 کاربر {message.from_user.first_name}، ارسال لینک ممنوع است!")
                except Exception as e:
                    print(e)

print("ربات روشن شد...")
bot.infinity_polling()
