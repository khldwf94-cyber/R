import os
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
import telebot
from telebot import types
from datetime import datetime, timedelta

# --- 1. السيرفر الوهمي لتشغيل البوت مجاناً على Render ---
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# --- 2. إعدادات البوت والمالك ---
TOKEN = os.environ.get('BOT_TOKEN')
ADMIN_ID = 5432340735  # الأيدي الخاص بك يا خالد
OWNER_USER = "@III888IIIII"

if not TOKEN:
    raise ValueError("ERROR: BOT_TOKEN is missing!")

bot = telebot.TeleBot(TOKEN)

# تخزين مؤقت لبيانات العملاء
user_store = {}

# ملف تخزين Mبيعات لإحصائيات دقيقة
STATS_FILE = "sales_log.txt"

# الحسابات البنكية التفصيلية
BANK_DETAILS = {
    'الراجحي': {"رقم": "378000010006080187221", "آيبان": "SA14 8000 0378 6080 1018 7221"},
    'الاهلي': {"رقم": "74300000606900", "آيبان": "SA36 1000 0074 3000 0060 6900"},
    'STC': {"رقم": "1023327364", "آيبان": "SA5278000000001023327364"},
    'برق': {"رقم": "991103822484251", "آيبان": "SA0530100991103822484251"},
    'يو باي': {"رقم": "لا يوجد رقم حساب", "آيبان": "SA9480200841178222121011"}
}

# قائمة المنتجات الرسمية والأسعار الرقمية للحسابات
PRODUCTS = {
    '1': {"name": "محاكي الحوادث مع طريقه تركيب مودات و مودات محدوده", "price": "20 ⃁", "num_price": 20},
    '2': {"name": "شرح تركيب المودات مع مودات محدوده", "price": "10 ⃁", "num_price": 10},
    '3': {"name": "بكج مودات مدفوعه ( تجميعه )", "price": "45 ⃁", "num_price": 45},
    '4': {"name": "لعبه سونرنر مع طريقه المودات", "price": "15 ⃁", "num_price": 15},
    '5': {"name": "بكج لعبه محاكي حوادث ( كامل )", "price": "35 ⃁", "num_price": 35},
    '6': {"name": "بكج لعبتين محاكي حوادث ( كامل )", "price": "40 ⃁", "num_price": 40}
}

# روابط التسليم الفردية لكل غرض عند القبول
DELIVERY = {
    '1': "1- https://t.me/+tPBT1R66qx43NGQ0\n2- https://t.me/+Ha82GPmaPJ05Yzg0\n3- https://t.me/+3wCL0hf-hbw0YTlk",
    '2': "1- https://t.me/+Ha82GPmaPJ05Yzg0\n2- https://t.me/+3wCL0hf-hbw0YTlk",
    '3': "1- https://t.me/+YjIKDxJjhsw1MDY8\n2- بوت الحماية والتفعيل: @N7L_STORE_bot",
    '4': "1- https://t.me/+PLLXva6AXRs0YTRk",
    '5': "1- https://t.me/+eRAj2HFhWTwzZDZk\n2- بوت الحماية والتفعيل: @N7L_STORE_bot",
    '6': "1- بوت الحماية والتفعيل: @N7L_STORE_bot\n2- https://t.me/+ZQQxOF8TELtiMTQ0"
}

# دالة لتسجيل المبيعات في ملف نصي
def log_sale(price):
    today_str = datetime.now().strftime("%Y-%m-%d")
    with open(STATS_FILE, "a") as f:
        f.write(f"{today_str},{price}\n")

# --- 3. أمر الإحصائيات السري الجديد للمالك فقط ---
@bot.message_handler(commands=['ارباحي'])
def show_statistics(message):
    if message.chat.id != ADMIN_ID:
        return  # يتجاهل أي شخص آخر لحماية خصوصيتك
        
    if not os.path.exists(STATS_FILE):
        with open(STATS_FILE, "w") as f:
            pass
        
    today = datetime.now().date()
    one_week_ago = today - timedelta(days=7)
    
    today_revenue = 0
    week_revenue = 0
    total_revenue = 0
    total_orders = 0
    
    with open(STATS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line or ',' not in line:
                continue
            date_str, price_str = line.split(',')
            try:
                sale_date = datetime.strptime(date_str, "%Y-%m-%d").date()
                price = int(price_str)
                
                total_revenue += price
                total_orders += 1
                
                if sale_date == today:
                    today_revenue += price
                if sale_date >= one_week_ago:
                    week_revenue += price
            except:
                continue
                
    stats_msg = (
        f"📊 **إحصائيات وأرباح متجر N7L STORE**\n\n"
        f"💰 أرباح اليوم: {today_revenue} ر.س\n"
        f"📅 أرباح آخر 7 أيام: {week_revenue} ر.س\n"
        f"💎 إجمالي الأرباح الكلي: {total_revenue} ر.س\n"
        f"📦 عدد الطلبات الناجحة: {total_orders} طلب\n\n"
        f"📈 استمر يا بطل، الله يرزقك ويبارك لك!"
    )
    bot.reply_to(message, stats_msg, parse_mode="Markdown")

# --- 4. أمر البداية والترحيب واستخراج البيانات للزبائن ---
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    uname = message.chat.first_name
    username = f"@{message.chat.username}" if message.chat.username else "لا يوجد يوزر"
    
    welcome_msg = (
        f"👋 نورت متجر نحل\n\n"
        f"👤 الاسم: {uname}\n"
        f"🆔 الأيدي: {uid}\n"
        f"🔗 اليوزر: {username}\n\n"
        f"اضغط على زر الشراء بالأسفل لمشاهدة المنتجات وبدء الطلب:"
    )
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("💳 للشراء")
    bot.send_message(uid, welcome_msg, reply_markup=markup)

# --- 5. التعامل مع زر للشراء ---
@bot.message_handler(func=lambda message: True)
def handle_text_buttons(message):
    if message.text == "💳 للشراء":
        markup = types.InlineKeyboardMarkup()
        for key, item in PRODUCTS.items():
            markup.add(types.InlineKeyboardButton(f"{key}- {item['name']} | {item['price']}", callback_data=f"prod_{key}"))
        bot.send_message(message.chat.id, "📁 قائمة المنتجات المتوفرة، اختر طلبك لبدء التحويل والدفع:", reply_markup=markup)

# --- 6. اختيار الغرض وعرض البنوك ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('prod_'))
def choose_bank(call):
    prod_id = call.data.split('_')[1]
    user_store[call.message.chat.id] = {"prod_id": prod_id}
    
    markup = types.InlineKeyboardMarkup()
    banks = ['الراجحي', 'الاهلي', 'STC', 'برق', 'يو باي']
    for b in banks:
        markup.add(types.InlineKeyboardButton(b, callback_data=f"bank_{b}"))
        
    bot.edit_message_text("🏦 البنوك المتوفرة لدفع:\nاختر البنك الذي تريد التحويل إليه:", call.message.chat.id, call.message.message_id, reply_markup=markup)

# --- 7. عرض تفاصيل البنك والمبلغ التلقائي ---
@bot.callback_query_handler(func=lambda call: call.data.startswith('bank_'))
def show_bank_details(call):
    bank_name = call.data.split('_')[1]
    uid = call.message.chat.id
    
    if uid not in user_store:
        bot.send_message(uid, "❌ انتهت الجلسة، يرجى البدء من جديد عبر الضغط على 💳 للشراء")
        return
        
    user_store[uid]["bank"] = bank_name
    prod_id = user_store[uid]["prod_id"]
    price = PRODUCTS[prod_id]["price"]
    
    bank_info = BANK_DETAILS[bank_name]
    
    msg = (
        f"📋 تفاصيل الدفع:\n\n"
        f"🏦 البنك: بنك {bank_name}\n"
        f"🔢 رقم الحساب: {bank_info['رقم']}\n"
        f"💳 الآيبان: {bank_info['آيبان']}\n"
        f"👤 اسم صاحب الحساب: محمد حسن عبدالله عتين\n"
        f"💰 المبلغ المطلوب: {price}\n\n"
        f"📌 بعد إتمام التحويل أرسل لقطة شاشة الحوالة او رساله الايصال او ملف الايصال هنا في المحادثة مباشرة.\n"
        f"⏳ سيتم التفعيل بعد تحقق لطلبك ."
    )
    bot.send_message(uid, msg)

# --- 8. استقبال الإثباتات وتوجيهها للمالك ---
@bot.message_handler(content_types=['photo', 'text', 'document'])
def handle_receipt(message):
    uid = message.chat.id
    if uid not in user_store or "bank" not in user_store[uid]:
        bot.reply_to(message, "⚠️ يرجى الضغط أولاً على زر 💳 للشراء واختيار غرضك قبل إرسال الإثبات.")
        return
        
    prod_id = user_store[uid]["prod_id"]
    bank_name = user_store[uid]["bank"]
    prod_name = PRODUCTS[prod_id]["name"]
    
    uname = message.chat.first_name
    username = f"@{message.chat.username}" if message.chat.username else "لا يوجد"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ قبول وتفعيل", callback_data=f"accept_{uid}_{prod_id}"),
        types.InlineKeyboardButton("❌ رفض الطلب", callback_data=f"reject_{uid}")
    )
    
    info_caption = f"🔔 إيصال جديد للمراجعة:\n👤 العميل: {uname}\n🔗 اليوزر: {username}\n🆔 الأيدي: {uid}\n📦 الغرض المطلوب: {prod_name}\n🏦 البنك المختار: {bank_name}"
    
    if message.content_type == 'photo':
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=info_caption, reply_markup=markup)
    elif message.content_type == 'document':
        bot.send_document(ADMIN_ID, message.document.file_id, caption=info_caption, reply_markup=markup)
    elif message.content_type == 'text':
        bot.send_message(ADMIN_ID, f"{info_caption}\n\n📝 الإثبات النصي المستلم:\n{message.text}", reply_markup=markup)
        
    bot.reply_to(message, "✅ تم استلام إيصالك بنجاح وجاري مراجعته والتحقق من قبل الإدارة.")

# --- 9. نظام معالجة القبول أو الرفض الذكي (يدعم النص والملف والصور بكفاءة) ---
@bot.callback_query_handler(func=lambda call: call.data.startswith(('accept_', 'reject_')))
def handle_approval(call):
    data_split = call.data.split('_')
    action = data_split[0]
    user_id = int(data_split[1])
    
    if action == 'accept':
        prod_id = data_split[2]
        prod_name = PRODUCTS[prod_id]["name"]
        num_price = PRODUCTS[prod_id]["num_price"]
        links = DELIVERY.get(prod_id, "لم يتم العثور على روابط، تواصل مع الإدارة.")
        
        # تسجيل العملية في نظام الأرباح
        log_sale(num_price)
        
        # رسالة الشكر والتسليم التلقائي للعميل
        success_client_msg = (
            f"شكرا على ثقتك فينا ❤️\n\n"
            f"📦 الغرض الذي طلبته:\n{prod_name}\n\n"
            f"🔗 روابط وأدوات غرضك المتاحة:\n{links}"
        )
        bot.send_message(user_id, success_client_msg)
        
        # تحديث رسالة الإداري بأمان سواء كانت نصية أو ملف/صورة
        try:
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="تم قبول الطلب وتسليم الروابط وتحديث الإحصائيات بنجاح ✅")
        except:
            bot.edit_message_text("تم قبول الطلب وتسليم الروابط وتحديث الإحصائيات بنجاح ✅", chat_id=call.message.chat.id, message_id=call.message.message_id)
        
        # تنبيه فوري للمالك
        try:
            client_chat = bot.get_chat(user_id)
            c_username = f"@{client_chat.username}" if client_chat.username else "لا يوجد يوزر"
            c_name = client_chat.first_name
        except:
            c_username = "غير معروف"
            c_name = "عميل"
            
        owner_alert = (
            f"🎉 **تنبيه: اكتمل طلب جديد بنجاح وتم تسجيل الأرباح!**\n\n"
            f"👤 الاسم: {c_name}\n"
            f"🔗 اليوزر: {c_username}\n"
            f"🆔 الأيدي: {user_id}\n"
            f"📦 الغرض: {prod_name}\n"
            f"💰 القيمة المضافة للإحصائيات: {num_price} ر.س"
        )
        bot.send_message(ADMIN_ID, owner_alert, parse_mode="Markdown")
        
    else:
        bot.send_message(user_id, "❌ نعتذر منك، تم رفض إيصال التحويل المرفق لعدم وضوحه أو عدم وصول المبلغ. يرجى مراجعة الحوالة والمحاولة مجدداً.")
        
        # تحديث رسالة الإداري عند الرفض بأمان
        try:
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="تم رفض طلب العميل ❌")
        except:
            bot.edit_message_text("تم رفض طلب العميل ❌", chat_id=call.message.chat.id, message_id=call.message.message_id)

print("تم تأمين استقبال النصوص والملفات بنجاح...")
bot.infinity_polling()
