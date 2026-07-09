import telebot
from telebot import types

# توكن البوت
TOKEN = "8866438689:AAGAE2JvglNmRwarNegJ6Xu8zyQysXB1ZPk"
ADMIN_ID = 5432340735  # الآيدي حقك

bot = telebot.TeleBot(TOKEN)

# دالة الترحيب
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🛒 قائمة المنتجات", callback_data="products")
    markup.add(btn)
    bot.reply_to(message, "👋 نورت متجر نحل N7L\nالاسم: " + message.from_user.first_name + "\nالايدي: " + str(message.from_user.id), reply_markup=markup)

# عرض المنتجات
@bot.callback_query_handler(func=lambda call: call.data == "products")
def show_products(call):
    text = "📦 قائمة المنتجات المتوفرة:\n\n١- محاكي الحوادث.. ٢٠ ⃁\n٢- شرح تركيب المودات.. ١٠ ⃁\n٣- بكج مودات مدفوعه.. ٤٥ ⃁\n٤- لعبه سونرنر.. ١٥ ⃁\n٥- بكج محاكي حوادث (كامل).. ٣٥ ⃁\n٦- بكج لعبتين محاكي.. ٤٠ ⃁"
    markup = types.InlineKeyboardMarkup()
    for i in range(1, 7):
        markup.add(types.InlineKeyboardButton(f"اختيار غرض {i}", callback_data=f"buy_{i}"))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

# اختيار البنك
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def choose_bank(call):
    product_id = call.data.split("_")[1]
    text = "🏦 اختر البنك للتحويل:"
    markup = types.InlineKeyboardMarkup()
    banks = ["الراجحي", "الاهلي", "STC", "برق", "يو باي"]
    for bank in banks:
        markup.add(types.InlineKeyboardButton(bank, callback_data=f"bank_{bank}_{product_id}"))
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

# تفاصيل الدفع
@bot.callback_query_handler(func=lambda call: call.data.startswith("bank_"))
def show_payment(call):
    data = call.data.split("_")
    bank_name = data[1]
    bot.send_message(call.message.chat.id, f"📋 تفاصيل الدفع لـ {bank_name}\n\n📌 بعد إتمام التحويل أرسل لقطة الشاشة هنا للتفعيل.")
    # تنبيه للأدمن
    bot.send_message(ADMIN_ID, f"🔔 طلب جديد!\nالمستخدم: {call.from_user.username}\nالايدي: {call.from_user.id}\nالغرض: {data[2]}\nالبنك: {bank_name}")

bot.infinity_polling()
