import os
import telebot
from telebot import types
import sqlite3

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

PRODUCTS = {
    '1': 'محاكي الحوادث مع المودات (20 ⃁)', '2': 'شرح تركيب المودات (10 ⃁)',
    '3': 'بكج مودات مدفوعة (45 ⃁)', '4': 'لعبة سونرنر (15 ⃁)',
    '5': 'بكج المحاكي الكامل (35 ⃁)', '6': 'بكج لعبتين (40 ⃁)'
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    for key, value in PRODUCTS.items():
        markup.add(types.InlineKeyboardButton(value, callback_data=f"product_{key}"))
    
    text = (f"🐝 نورت متجر N7L STORE\n\nالاسم: {message.from_user.first_name}\n"
            f"اليوزر: @{message.from_user.username}\nالايدي: {message.from_user.id}\n\n"
            "الرجاء اختيار الغرض المطلوب:")
    bot.reply_to(message, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('product_'))
def product_selected(call):
    product_id = call.data.split('_')[1]
    product_name = PRODUCTS[product_id]
    
    # هنا سنضيف لاحقاً منطق اختيار البنوك
    bot.answer_callback_query(call.id, f"تم اختيار: {product_name}")
    bot.send_message(call.message.chat.id, f"لقد اخترت {product_name}. جاري تجهيز بيانات البنوك...")

bot.infinity_polling()
