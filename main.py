import os
import telebot
from telebot import types

TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 5432340735  # <--- ضع رقم الأيدي الخاص بك هنا
bot = telebot.TeleBot(TOKEN)

user_data = {}

BANK_DETAILS = {
    'الراجحي': "رقم الحساب: 378000010006080187221\nآيبان: SA14 8000 0378 6080 1018 7221",
    'الأهلي': "رقم الحساب: 74300000606900\nآيبان: SA36 1000 0074 3000 0060 6900",
    'STC Pay': "رقم الحساب: 1023327364\nآيبان: SA5278000000001023327364",
    'برق': "رقم الحساب: 30100991103822484251\nآيبان: SA0530100991103822484251",
    'يو باي': "رقم الحساب: 80200841178222121011\nآيبان: SA9480200841178222121011"
}

# قائمة المنتجات مع الأسعار
PRODUCTS = {
    '1': 'محاكي الحوادث (20 ⃁)', '2': 'شرح تركيب المودات (10 ⃁)',
    '3': 'بكج مودات مدفوعة (45 ⃁)', '4': 'لعبة سونرنر (15 ⃁)',
    '5': 'بكج المحاكي الكامل (35 ⃁)', '6': 'بكج لعبتين (40 ⃁)'
}

DELIVERY = {
    '1': "✅ شكراً لثقتك بمتجرنا!\nروابط غرضك:\n1. https://t.me/+tPBT1R66qx43NGQ0\n2. https://t.me/+Ha82GPmaPJ05Yzg0\n3. https://t.me/+3wCL0hf-hbw0YTlk",
    '2': "✅ شكراً لثقتك بمتجرنا!\nروابط غرضك:\n1. https://t.me/+Ha82GPmaPJ05Yzg0\n2. https://t.me/+3wCL0hf-hbw0YTlk",
    '3': "✅ شكراً لثقتك بمتجرنا!\n1. https://t.me/+YjIKDxJjhsw1MDY8\n2. بوت الحماية: @N7L_STORE_bot",
    '4': "✅ شكراً لثقتك بمتجرنا!\nرابط غرضك:\nhttps://t.me/+PLLXva6AXRs0YTRk",
    '5': "✅ شكراً لثقتك بمتجرنا!\n1. https://t.me/+eRAj2HFhWTwzZDZk\n2. بوت الحماية: @N7L_STORE_bot",
    '6': "✅ شكراً لثقتك بمتجرنا!\n1. بوت الحماية: @N7L_STORE_bot\n2. https://t.me/+ZQQxOF8TELtiMTQ0"
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    for key, value in PRODUCTS.items():
        markup.add(types.InlineKeyboardButton(value, callback_data=f"prod_{key}"))
    bot.reply_to(message, "🐝 نورت متجر N7L STORE، اختر الغرض:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('prod_'))
def choose_bank(call):
    user_data[call.message.chat.id] = call.data.split('_')[1]
    markup = types.InlineKeyboardMarkup()
    for bank in BANK_DETAILS.keys():
        markup.add(types.InlineKeyboardButton(bank, callback_data=f"bank_{bank}"))
    bot.edit_message_text("ممتاز! اختر البنك للتحويل:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('bank_'))
def show_bank_details(call):
    bank_name = call.data.split('_')[1]
    msg = f"📋 تفاصيل الدفع:\n\nالبنك: {bank_name} 🏦\n{BANK_DETAILS[bank_name]}\n\n📌 أرسل صورة الإيصال بعد التحويل."
    bot.send_message(call.message.chat.id, msg)

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    if message.chat.id not in user_data:
        bot.reply_to(message, "يرجى اختيار منتج أولاً عبر /start")
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ قبول", callback_data=f"accept_{message.chat.id}"),
        types.InlineKeyboardButton("❌ رفض", callback_data=f"reject_{message.chat.id}")
    )
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, 
                   caption=f"🔔 إيصال من {message.chat.first_name}\nالطلب: {PRODUCTS[user_data[message.chat.id]]}", 
                   reply_markup=markup)
    bot.reply_to(message, "✅ تم استلام إيصالك، جاري التحقق.")

@bot.callback_query_handler(func=lambda call: call.data.startswith(('accept_', 'reject_')))
def handle_approval(call):
    action, user_id = call.data.split('_')
    product_id = user_data.get(int(user_id))
    if action == 'accept':
        bot.send_message(user_id, DELIVERY.get(product_id, "تم قبول طلبك!"))
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="تم تسليم الطلب ✅")
    else:
        bot.send_message(user_id, "عذراً، تم رفض طلبك.")
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="تم رفض الطلب ❌")

bot.infinity_polling()
