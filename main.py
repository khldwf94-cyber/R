import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import telebot
from telebot import types

# --- 1. السيرفر الوهمي لخدعة موقع Render لتشغيله مجاناً 100% ---
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# تشغيل السيرفر في الخلفية
threading.Thread(target=run_dummy_server, daemon=True).start()

# --- 2. إعدادات البوت والتوكن ---
TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 5432340735  # <--- ⚠️ ضع رقم الأيدي الخاص بك هنا لتوثيق الإيصالات

if not TOKEN:
    raise ValueError("ERROR: BOT_TOKEN is missing!")

bot = telebot.TeleBot(TOKEN)
user_data = {}

# الحسابات البنكية الخاصة بك
BANK_DETAILS = {
    'الراجحي': "رقم الحساب: 378000010006080187221\nآيبان: SA14 8000 0378 6080 1018 7221",
    'الأهلي': "رقم الحساب: 74300000606900\nآيبان: SA36 1000 0074 3000 0060 6900",
    'STC Pay': "رقم الحساب: 1023327364\nآيبان: SA5278000000001023327364",
    'برق': "رقم الحساب: 30100991103822484251\nآيبان: SA0530100991103822484251",
    'يو باي': "رقم الحساب: 80200841178222121011\nآيبان: SA9480200841178222121011"
}

# قائمة منتجات متجرك الفعلية
PRODUCTS = {
    '1': 'محاكي الحوادث (20 ⃁)', '2': 'شرح تركيب المودات (10 ⃁)',
    '3': 'بكج مودات مدفوعة (45 ⃁)', '4': 'لعبة سونرنر (15 ⃁)',
    '5': 'بكج المحاكي الكامل (35 ⃁)', '6': 'بكج لعبتين (40 ⃁)'
}

# روابط التسليم التلقائي الخاصة بك
DELIVERY = {
    '1': "✅ شكراً لثقتك بمتجرنا!\nروابط غرضك:\n1. https://t.me/+tPBT1R66qx43NGQ0\n2. https://t.me/+Ha82GPmaPJ05Yzg0\n3. https://t.me/+3wCL0hf-hbw0YTlk",
    '2': "✅ شكراً لثقتك بمتجرنا!\nروابط غرضك:\n1. https://t.me/+Ha82GPmaPJ05Yzg0\n2. https://t.me/+3wCL0hf-hbw0YTlk",
    '3': "✅ شكراً لثقتك بمتجرنا!\n1. https://t.me/+YjIKDxJjhsw1MDY8\n2. بوت الحماية: @N7L_STORE_bot",
    '4': "✅ شكراً لثقتك بمتجرنا!\nرابط غرضك:\nhttps://t.me/+PLLXva6AXRs0YTRk",
    '5': "✅ شكراً لثقتك بمتجرنا!\n1. https://t.me/+eRAj2HFhWTwzZDZk\n2. بوت الحماية: @N7L_STORE_bot",
    '6': "✅ شكراً لثقتك بمتجرنا!\n1. بوت الحماية: @N7L_STORE_bot\n2. https://t.me/+ZQQxOF8TELtiMTQ0"
}

# --- 3. أمر تشغيل البوت والترحيب بزر الشراء فقط ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💳 للشراء")  # زر واحد كبير ومباشر بالأسفل
    bot.send_message(message.chat.id, "نورت متجر N7L STORE\n\nاضغط على زر الشراء بالأسفل لمشاهدة المنتجات وبدء الطلب:", reply_markup=markup)

# --- 4. التعامل مع زر للشراء ---
@bot.message_handler(func=lambda message: True)
def handle_text_buttons(message):
    if message.text == "💳 للشراء":
        markup = types.InlineKeyboardMarkup()
        for key, value in PRODUCTS.items():
            markup.add(types.InlineKeyboardButton(value, callback_data=f"prod_{key}"))
        bot.send_message(message.chat.id, "📁 قائمة المنتجات المتوفرة، اختر طلبك لبدء التحويل والدفع:", reply_markup=markup)

# --- 5. خطوات اختيار المنتج والبنك والإيصال ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('prod_'))
def choose_bank(call):
    user_data[call.message.chat.id] = call.data.split('_')[1]
    markup = types.InlineKeyboardMarkup()
    for bank in BANK_DETAILS.keys():
        markup.add(types.InlineKeyboardButton(bank, callback_data=f"bank_{bank}"))
    bot.edit_message_text("ممتاز! اختر البنك المناسب لك للتحويل:", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('bank_'))
def show_bank_details(call):
    bank_name = call.data.split('_')[1]
    msg = f"📋 تفاصيل الدفع والتحويل:\n\nالبنك: {bank_name} 🏦\n{BANK_DETAILS[bank_name]}\n\n📌 بعد التحويل، يرجى إرسال (صورة الإيصال) مباشرة هنا في المحادثة."
    bot.send_message(call.message.chat.id, msg)

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    if message.chat.id not in user_data:
        bot.reply_to(message, "يرجى الضغط أولاً على زر 💳 للشراء واختيار غرضك")
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ قبول وتوصيل", callback_data=f"accept_{message.chat.id}"),
        types.InlineKeyboardButton("❌ رفض الطلب", callback_data=f"reject_{message.chat.id}")
    )
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, 
                   caption=f"🔔 إيصال جديد من {message.chat.first_name}\nالطلب: {PRODUCTS[user_data[message.chat.id]]}", 
                   reply_markup=markup)
    bot.reply_to(message, "✅ تم استلام إيصالك بنجاح. جاري مراجعته من قبل الإدارة، ستصلك الروابط فوراً عند القبول.")

@bot.callback_query_handler(func=lambda call: call.data.startswith(('accept_', 'reject_')))
def handle_approval(call):
    action, user_id = call.data.split('_')
    product_id = user_data.get(int(user_id))
    if action == 'accept':
        bot.send_message(user_id, DELIVERY.get(product_id, "تم قبول طلبك بنجاح!"))
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="تم تسليم الروابط للعميل بنجاح ✅")
    else:
        bot.send_message(user_id, "عذراً، تم رفض طلبك بسبب عدم وضوح الإيصال أو عدم اكتمال عملية التحويل.")
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="تم رفض إيصال العميل ❌")

print("البوت شغال مجاناً وبزر شراء مباشر بدون إضافات...")
bot.infinity_polling()
