import os
import telebot
import sqlite3

# إعداد البوت
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# دالة حفظ الطلب في قاعدة البيانات
def add_order(user_id, product_name):
    conn = sqlite3.connect('n7l_store.db')
    cursor = conn.cursor()
    # تأكد أن جدول الطلبات موجود في database.py
    cursor.execute("INSERT INTO orders (user_id, product_name) VALUES (?, ?)", (user_id, product_name))
    conn.commit()
    conn.close()

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "مرحباً بك في متجر N7L STORE 🐝\nاختر رقماً للبدء:\n1- محاكي الحوادث\n2- شرح المودات\n3- بكج مودات\n4- سونرنر\n5- بكج محاكي\n6- بكج لعبتين")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    products = {'1': 'محاكي الحوادث', '2': 'شرح المودات', '3': 'بكج مودات', '4': 'سونرنر', '5': 'بكج محاكي', '6': 'بكج لعبتين'}
    
    if message.text in products:
        product_name = products[message.text]
        add_order(message.chat.id, product_name)
        bot.reply_to(message, f"تم تسجيل طلبك لـ {product_name} بنجاح! ✅\n\nتفضل بيانات البنوك للتحويل:\n[الراجحي: XXXX]\n[الأهلي: XXXX]\nأرسل صورة الإيصال ليتم التحقق منه.")
    else:
        bot.reply_to(message, "الرجاء اختيار رقم صحيح من القائمة أعلاه.")

bot.infinity_polling()
