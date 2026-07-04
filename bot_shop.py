import os
import telebot
from telebot import types

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# بيانات البنوك المحدثة
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
    bot.reply_to(message, "🐝 نورت متجر N7L STORE، اختر الغرض:", reply_markup=markup)

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
    msg = f"📋 تفاصيل الدفع:\n\nالبنك: {bank_name} 🏦\n{details}\n\n📌 بعد التحويل أرسل الإيصال لبوت التحقق."
    bot.send_message(call.message.chat.id, msg)

bot.infinity_polling()
