import os
import telebot
from telebot import types

TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 5432340735  # <--- ضع رقم الأيدي الخاص بك هنا (بدون علامات تنصيص)
bot = telebot.TeleBot(TOKEN)

# بيانات البنوك
BANK_DETAILS = {
    'الراجحي': "رقم: 378000010006080187221\nآيبان: SA14 8000 0378 6080 1018 7221\nصاحب الحساب: محمد حسن عبدالله عتين",
    'الأهلي': "رقم: 74300000606900\nآيبان: SA36 1000 0074 3000 0060 6900",
    'STC Pay': "رقم حساب: 1023327364\nآيبان: SA5278000000001023327364",
    'برق': "آيبان: SA0530100991103822484251",
    'يو باي': "آيبان: SA9480200841178222121011"
}

PRODUCTS = {
    '1': 'محاكي الحوادث مع (20 ⃁)', '2': 'شرح تركيب المودات (10 ⃁)',
    '3': 'بكج مودات مدفوعة (45 ⃁)', '4': 'لعبة سونرنر (15 ⃁)',
    '5': 'بكج المحاكي الكامل (35 ⃁)', '6': 'بكج لعبتين (40 ⃁)'
}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    for key, value in PRODUCTS.items():
        markup.add(types.InlineKeyboardButton(value, callback_data=f"prod_{key}"))
    bot.reply_to(message, " نورت متجر N7L STORE، اختر الغرض:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('prod_'))
def choose_bank(call):
    markup = types.InlineKeyboardMarkup()
    for bank in BANK_DETAILS.keys():
        markup.add(types.InlineKeyboardButton(bank, callback_data=f"bank_{bank}"))
    bot.edit_message_text("ممتاز! اختر البنك للتحويل:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('bank_'))
def show_bank_details(call):
    bank_name = call.data.split('_')[1]
    details = BANK_DETAILS[bank_name]
    msg = f"📋 تفاصيل الدفع:\n\nالبنك: {bank_name} 🏦\n{details}\n\n📌 بعد التحويل أرسل الإيصال (صورة) لهذا البوت."
    bot.send_message(call.message.chat.id, msg)

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ قبول", callback_data=f"accept_{message.chat.id}"),
        types.InlineKeyboardButton("❌ رفض", callback_data=f"reject_{message.chat.id}")
    )
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, 
                   caption=f"🔔 إيصال جديد من: {message.chat.first_name}\nID: {message.chat.id}", 
                   reply_markup=markup)
    bot.reply_to(message, "✅ تم استلام إيصالك، جاري التحقق من قبل الإدارة.")

@bot.callback_query_handler(func=lambda call: call.data.startswith(('accept_', 'reject_')))
def handle_approval(call):
    action, user_id = call.data.split('_')
    if action == 'accept':
        bot.send_message(user_id, "تم قبول طلبك! شكراً لك.")
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="تم قبول الطلب ✅")
    else:
        bot.send_message(user_id, "عذراً، تم رفض طلبك.")
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="تم رفض الطلب ❌")

bot.infinity_polling()
