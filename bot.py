import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8827172526:AAHuPKfl_df5b_xY41AE0WrF01PRfVaQkf8"
bot = telebot.TeleBot(BOT_TOKEN)

group_settings = {}
BAD_WORDS = ["احمق", "بیشعور", "خر", "اسپم"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == 'private':
        bot.reply_to(message, "سلام صاحب من! ربات مدیریت گروه پیشرفته آماده کار است. 🚀\nمن را به گروه خود اضافه کنید و ادمین کنید.")

@bot.message_handler(commands=['setting'])
def show_settings(message):
    if message.chat.type in ['group', 'supergroup']:
        chat_member = bot.get_chat_member(message.chat.id, message.from_user.id)
        if chat_member.status in ['administrator', 'creator', 'owner']:
            chat_id = message.chat.id
            if chat_id not in group_settings:
                group_settings[chat_id] = {"link": True, "word": True, "welcome": True}
            
            markup = InlineKeyboardMarkup()
            status_link = "✅ قفل" if group_settings[chat_id]["link"] else "❌ باز"
            status_word = "✅ قفل" if group_settings[chat_id]["word"] else "❌ باز"
            status_welcome = "✅ روشن" if group_settings[chat_id]["welcome"] else "❌ خاموش"
            
            markup.row(InlineKeyboardButton(f"ضد لینک: {status_link}", callback_data=f"toggle_link_{chat_id}"))
            markup.row(InlineKeyboardButton(f"فیلتر کلمات زشت: {status_word}", callback_data=f"toggle_word_{chat_id}"))
            markup.row(InlineKeyboardButton(f"خوش‌آمدگویی اعضا: {status_welcome}", callback_data=f"toggle_welcome_{chat_id}"))
            
            bot.send_message(chat_id, "⚙️ **پنل تنظیمات ربات مدیریت گروه**\nبرای مدیریت قفل‌ها روی دکمه‌های زیر کلیک کنید:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("toggle_"))
def callback_inline(call):
    chat_id = int(call.data.split("_")[-1])
    chat_member = bot.get_chat_member(chat_id, call.from_user.id)
    if chat_member.status not in ['administrator', 'creator', 'owner']:
        bot.answer_callback_query(call.id, "❌ این پنل فقط مخصوص مدیران گروه است!", show_alert=True)
        return

    action = call.data.split("_")[1]
    if action == "link":
        group_settings[chat_id]["link"] = not group_settings[chat_id]["link"]
    elif action == "word":
        group_settings[chat_id]["word"] = not group_settings[chat_id]["word"]
    elif action == "welcome":
        group_settings[chat_id]["welcome"] = not group_settings[chat_id]["welcome"]
        
    markup = InlineKeyboardMarkup()
    status_link = "✅ قفل" if group_settings[chat_id]["link"] else "❌ باز"
    status_word = "✅ قفل" if group_settings[chat_id]["word"] else "❌ باز"
    status_welcome = "✅ روشن" if group_settings[chat_id]["welcome"] else "❌ خاموش"
    
    markup.row(InlineKeyboardButton(f"ضد لینک: {status_link}", callback_data=f"toggle_link_{chat_id}"))
    markup.row(InlineKeyboardButton(f"فیلتر کلمات زشت: {status_word}", callback_data=f"toggle_word_{chat_id}"))
    markup.row(InlineKeyboardButton(f"خوش‌آمدگویی اعضا: {status_welcome}", callback_data=f"toggle_welcome_{chat_id}"))
    
    bot.edit_message_reply_markup(chat_id, call.message.message_id, reply_markup=markup)
    bot.answer_callback_query(call.id, "تنظیمات با موفقیت بروزرسانی شد.")

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_member(message):
    chat_id = message.chat.id
    if chat_id not in group_settings:
        group_settings[chat_id] = {"link": True, "word": True, "welcome": True}
        
    if group_settings[chat_id]["welcome"]:
        for new_user in message.new_chat_members:
            bot.send_message(chat_id, f"🌟 سلام {new_user.first_name} عزیز!\nبه گروه ما خوش آمدید. لطفا قوانین را رعایت کنید. 🙏")

@bot.message_handler(func=lambda message: True)
def control_group_messages(message):
    if message.chat.type in ['group', 'supergroup']:
        chat_id = message.chat.id
        if chat_id not in group_settings:
            group_settings[chat_id] = {"link": True, "word": True, "welcome": True}
            
        text = message.text or message.caption
        if text:
            chat_member = bot.get_chat_member(chat_id, message.from_user.id)
            if chat_member.status not in ['administrator', 'creator', 'owner']:
                if group_settings[chat_id]["link"] and ("http" in text or "t.me" in text or "@" in text):
                    try:
                        bot.delete_message(chat_id, message.message_id)
                        bot.send_message(chat_id, f"🗣 کاربر {message.from_user.first_name}، ارسال لینک در این گروه ممنوع است!")
                        return
                    except: pass
                
                if group_settings[chat_id]["word"]:
                    for word in BAD_WORDS:
                        if word in text:
                            try:
                                bot.delete_message(chat_id, message.message_id)
                                bot.send_message(chat_id, f"⚠️ کاربر {message.from_user.first_name}، احترام خود را نگه دارید! ارسال کلمات ممنوعه مجاز نیست.")
                                return
                            except: pass

print("ربات پیشرفته و کامل روشن شد...")
bot.infinity_polling()

