import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import telebot

# --- 1. السيرفر الوهمي لخدعة موقع Render ---
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# تشغيل السيرفر في الخلفية
threading.Thread(target=run_dummy_server, daemon=True).start()

# --- 2. إعدادات البوت والتوكن ---
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("ERROR: BOT_TOKEN is missing!")

bot = telebot.TeleBot(BOT_TOKEN)

# --- 3. بيانات المنتجات (الأسعار الجديدة) ---
PRODUCTS = {
    "شدات ببجي": [
        {"name": "60 شدة", "price": "4.5 ر.س"},
        {"name": "325 شدة", "price": "21 ر.س"},
        {"name": "660 شدة", "price": "40 ر.س"},
        {"name": "1800 شدة", "price": "95 ر.س"}
    ],
    "حسابات ببجي": [
        {"name": "حساب عشوائي - ليفل 50+", "price": "35 ر.س"},
        {"name": "حساب مشحون كونكر", "price": "120 ر.س"}
    ],
    "تطبيقات بلس": [
        {"name": "اشتراك بلس سنة (آيفون)", "price": "45 ر.س"}
    ]
}

# --- 4. أوامر البوت وقوائم التشغيل ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🛒 استعراض الأقسام", "📞 الدعم الفني")
    bot.send_message(
        message.chat.id,
        "👋 أهلاً بك في متجر N7L STORE!\n\nيسعدنا خدمتك، اختر من القائمة بالأسفل للبدء:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "🛒 استعراض الأقسام":
        markup = telebot.types.InlineKeyboardMarkup()
        for category in PRODUCTS.keys():
            markup.add(telebot.types.InlineKeyboardButton(text=category, callback_data=f"cat_{category}"))
        bot.send_message(message.chat.id, "📁 اختر القسم الذي تريد تصفحه:", reply_markup=markup)
        
    elif message.text == "📞 الدعم الفني":
        bot.send_message(message.chat.id, "👨‍💻 للتواصل مع الدعم الفني أو الشراء المباشر:\n@khldwf94")

@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def show_products(call):
    category_name = call.data.replace("cat_", "")
    products_list = PRODUCTS.get(category_name, [])
    
    response_text = f"📦 **قسم: {category_name}**\n\n"
    for prod in products_list:
        response_text += f"🔹 {prod['name']} ➔ {prod['price']}\n"
        
    response_text += "\n💳 للشراء، تواصل مع الدعم الفني مباشرة واذكر الطلب."
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text="🔙 العودة للأقسام", callback_data="back_to_cats"))
    
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=response_text, reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "back_to_cats")
def back_to_categories(call):
    markup = telebot.types.InlineKeyboardMarkup()
    for category in PRODUCTS.keys():
        markup.add(telebot.types.InlineKeyboardButton(text=category, callback_data=f"cat_{category}"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="📁 اختر القسم الذي تريد تصفحه:", reply_markup=markup)

# --- 5. تشغيل البوت المستمر ---
print("البوت يعمل الآن بنجاح على السيرفر المجاني...")
bot.infinity_polling()
