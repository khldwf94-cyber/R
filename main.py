import os
import telebot
from telebot import types

# جلب التوكن من إعدادات Render (آمن جداً)
TOKEN = os.environ.get("TOKEN")
ADMIN_ID = 5432340735
bot = telebot.TeleBot(TOKEN)

# الترحيب
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🛒 قائمة المنتجات", callback_data="products")
    markup.add(btn)
    bot.reply_to(message, f"👋 نورت متجر نحل N7L\nالاسم: {message.from_user.first_name}\nالايدي: {message.from_user.id}", reply_markup=markup)

# قائمة المنتجات
@bot.callback_query_handler(func=lambda call: call.data == "products")
def show_products(call):
    text = "📦 قائمة المنتجات المتوفرة:\n\n١- محاكي الحوادث.. ٢٠ ⃁\n٢- شرح تركيب المودات.. ١٠ ⃁\n٣- بكج مودات مدفوعه.. 45 ⃁\n٤- لعبه سونرنر.. 15 ⃁\n٥- بكج محاكي حوادث (كامل).. 35 ⃁\n٦- بكج لعبتين محاكي.. 40 ⃁"
    markup = types.InlineKeyboardMarkup()
    for i in range(1, 7):
        markup.add(types.InlineKeyboardButton(f"شراء غرض {i}", callback_data=f"buy_{i}"))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

# اختيار البنك
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def choose_bank(call):
    product_id = call.data.split("_")[1]
    markup = types.InlineKeyboardMarkup()
    banks = ["الراجحي", "الاهلي", "STC", "برق", "يو باي"]
    for bank in banks:
        markup.add(types.InlineKeyboardButton(bank, callback_data=f"bank_{bank}_{product_id}"))
    bot.edit_message_text("🏦 اختر البنك للتحويل:", call.message.chat.id, call.message.message_id, reply_markup=markup)

# إتمام الطلب وتنبيه الأدمن
@bot.callback_query_handler(func=lambda call: call.data.startswith("bank_"))
def finish_order(call):
    data = call.data.split("_")
    bank_name = data[1]
    bot.edit_message_text(f"📋 تفاصيل الدفع لـ {bank_name}\n📌 أرسل لقطة الشاشة هنا للتفعيل.", call.message.chat.id, call.message.message_id)
    bot.send_message(ADMIN_ID, f"🔔 طلب جديد!\nالمستخدم: @{call.from_user.username}\nالايدي: {call.from_user.id}\nالغرض: {data[2]}\nالبنك: {bank_name}")

print("🤖 البوت يعمل الآن وبأمان!")
bot.infinity_polling()
