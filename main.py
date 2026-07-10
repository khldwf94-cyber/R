import os
import threading
import telebot
from telebot import types
from flask import Flask

# التوكن والبيانات الأساسية
TOKEN = "8866438689:AAGAE2JvglNmRwarNegJ6Xu8zyQysXB1ZPk"
ADMIN_ID = 5432340735  # آيدي المالك
bot = telebot.TeleBot(TOKEN)

# إعداد سيرفر الويب لتخطي فحص ريندر (Render) وتثبيت التشغيل
app = Flask(__name__)

@app.route('/')
def home():
    return "N7L Store Bot is running 24/7!"

# 1. بداية تشغيل البوت والترحيب (الاسم، الآيدي، اليوزر)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    username = f"@{message.from_user.username}" if message.from_user.username else "لا يوجد يوزر"
    
    markup = types.InlineKeyboardMarkup()
    btn_buy = types.InlineKeyboardButton("للشراء 💳", callback_data="show_products")
    markup.add(btn_buy)
    
    welcome_text = (
        f"👋 نورت متجر نحل N7L\n\n"
        f"👤 الاسم: {first_name}\n"
        f"🆔 الآيدي: {user_id}\n"
        f"🏷️ اليوزر: {username}"
    )
    bot.reply_to(message, welcome_text, reply_markup=markup)

# 2. عرض المنتجات الستة والأسعار بعد ضغط "للشراء"
@bot.callback_query_handler(func=lambda call: call.data == "show_products")
def show_products(call):
    text = (
        "تحديد نوع الغرض 👇:\n\n"
        "١- محاكي الحوادث مع طريقه تركيب مودات و مودات محدوده ٢٠ ⃁\n"
        "٢- شرح تركيب المودات مع مودات محدوده ب ١٠ ⃁\n"
        "٣- بكج مودات مدفوعه ( تجميعه ) ٤٥ ⃁\n"
        "٤- لعبه سونرنر مع طريقه المودات ١٥ ⃁\n"
        "٥- بكج لعبه محاكي حوادث ( كامل ) ب ٣٥ ⃁\n"
        "٦- بكج لعبتين محاكي حوادث ( كامل ) ٤٠ ⃁"
    )
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("١", callback_data="prod_1_20"), types.InlineKeyboardButton("٢", callback_data="prod_2_10"))
    markup.add(types.InlineKeyboardButton("٣", callback_data="prod_3_45"), types.InlineKeyboardButton("٤", callback_data="prod_4_15"))
    markup.add(types.InlineKeyboardButton("٥", callback_data="prod_5_35"), types.InlineKeyboardButton("٦", callback_data="prod_6_40"))
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

# 3. اختيار البنك بعد تحديد الغرض
@bot.callback_query_handler(func=lambda call: call.data.startswith("prod_"))
def choose_bank(call):
    _, prod_num, price = call.data.split("_")
    
    text = "البنوك المتوفرة لتسديد المبلغ عبرها:\nانواع البنوك 👇:"
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("١- بنك الراجحي", callback_data=f"bank_rajhi_{prod_num}_{price}"))
    markup.add(types.InlineKeyboardButton("٢- بنك الاهلي", callback_data=f"bank_ahli_{prod_num}_{price}"))
    markup.add(types.InlineKeyboardButton("٣- بنك STC", callback_data=f"bank_stc_{prod_num}_{price}"))
    markup.add(types.InlineKeyboardButton("٤- برق", callback_data=f"bank_barq_{prod_num}_{price}"))
    markup.add(types.InlineKeyboardButton("٥- يو باي", callback_data=f"bank_upay_{prod_num}_{price}"))
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)

# 4. تفاصيل الدفع حسب البنك المختار مع إدخال السعر تلقائياً
@bot.callback_query_handler(func=lambda call: call.data.startswith("bank_"))
def payment_details(call):
    _, bank, prod_num, price = call.data.split("_")
    
    # تفاصيل البنوك والبيانات
    details = ""
    if bank == "rajhi":
        details = (
            f"البنك: بنك الراجحي 🏦\n"
            f"رقم: 378000010006080187221\n"
            f"الايبان: SA14 8000 0378 6080 1018 7221\n"
            f"اسم صاحب الحساب: محمد حسن عبدالله عتين\n"
            f"المبلغ: {price} ريال"
        )
    elif bank == "stc":
        details = (
            f"البنك: بنك STC 📱\n"
            f"رقم حساب: 1023327364\n"
            f"الايبان: SA5278000000001023327364\n"
            f"المبلغ: {price} ريال"
        )
    elif bank == "ahli":
        details = (
            f"البنك: بنك الاهلي 🏦\n"
            f"رقم حساب: 74300000606900\n"
            f"رقم حساب الدولي: SA36 1000 0074 3000 0060 6900\n"
            f"المبلغ: {price} ريال"
        )
    elif bank == "upay":
        details = (
            f"البنك: يو باي 💳\n"
            f"الايبان: SA9480200841178222121011\n"
            f"المبلغ: {price} ريال"
        )
    elif bank == "barq":
        details = (
            f"البنك: برق ⚡\n"
            f"رقم حساب: 991103822484251\n"
            f"الايبان: SA0530100991103822484251\n"
            f"المبلغ: {price} ريال"
        )

    text = (
        f"📋 تفاصيل الدفع:\n\n{details}\n\n"
        f"📌 بعد إتمام التحويل أرسل لقطة شاشة الحوالة او رساله الايصال او ملف الايصال هنا.\n"
        f"⏳ سيتم التفعيل بعد تحقق لطلبك ."
    )
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id)
    
    # تحويل حالة المستخدم لانتظار الإثبات وتخزين الغرض المطلوب
    bot.register_next_step_handler(call.message, receive_proof, prod_num, price, bank)

# 5. استقبال الإثبات (صورة، نص، ملف) وإرسال التنبيه الفوري للمالك
def receive_proof(message, prod_num, price, bank):
    user_id = message.from_user.id
    username = f"@{message.from_user.username}" if message.from_user.username else "لا يوجد يوزر"
    first_name = message.from_user.first_name
    
    # إرسال التنبيه للمالك أولاً
    admin_alert = (
        f"🔔 وصلك إثبات دفع جديد لطلب!\n\n"
        f"👤 العميل: {first_name}\n"
        f"🆔 الآيدي: {user_id}\n"
        f"🏷️ اليوزر: {username}\n"
        f"📦 الغرض المطلوب: غرض رقم {prod_num}\n"
        f"💰 السعر: {price} ريال\n"
        f"🏦 البنك المستخدم: {bank}"
    )
    bot.send_message(ADMIN_ID, admin_alert)
    
    # إعادة توجيه الإثبات (سواء صورة، ملف، أو نص) للمالك مباشرة للتحقق منه
    if message.content_type == 'photo':
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"📸 إثبات صورة من العميل {user_id}")
    elif message.content_type == 'document':
        bot.send_document(ADMIN_ID, message.document.file_id, caption=f"📄 إثبات ملف من العميل {user_id}")
    elif message.content_type == 'text':
        bot.send_message(ADMIN_ID, f"✍️ إثبات نصي أو رسالة من العميل {user_id}:\n{message.text}")
        
    # خيارات التحكم للمالك (قبول أو رفض) الحوالة بضغطة زر
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ قبول", callback_data=f"approve_{user_id}_{prod_num}"),
        types.InlineKeyboardButton("❌ رفض", callback_data=f"reject_{user_id}")
    )
    bot.send_message(ADMIN_ID, "⚙️ التحكم في الطلب:", reply_markup=markup)
    
    # تأكيد الاستلام للزبون والانتظار
    bot.reply_to(message, "⏳ تم استلام إثبات الدفع وجاري التحقق من طلبك من قبل الإدارة...")

# 6. معالجة قبول أو رفض الأدمن للطلب وإرسال الروابط وشكر الزبون تلقائياً
@bot.callback_query_handler(func=lambda call: call.data.startswith(("approve_", "reject_")))
def handle_admin_decision(call):
    if call.message.chat.id != ADMIN_ID:
        return
        
    data = call.data.split("_")
    action = data[0]
    target_user_id = int(data[1])
    
    if action == "approve":
        prod_num = data[2]
        thanks_msg = f"شكرا على ثقتك فينا ❤️\n🎁 الغرض الذي طلبته:"
        
        # تسليم الروابط بناءً على رقم الغرض المشتري
        if prod_num == "1":
            links = "‏١- https://t.me/+tPBT1R66qx43NGQ0\n‏٢- https://t.me/+Ha82GPmaPJ05Yzg0\n‏٣- https://t.me/+3wCL0hf-hbw0YTlk"
            bot.send_message(target_user_id, f"{thanks_msg}\n{links}")
        elif prod_num == "2":
            links = "‏١- https://t.me/+Ha82GPmaPJ05Yzg0\n‏٢- https://t.me/+3wCL0hf-hbw0YTlk"
            bot.send_message(target_user_id, f"{thanks_msg}\n{links}")
        elif prod_num == "3":
            links = "‏١- https://t.me/+YjIKDxJjhsw1MDY8\n٢- يوزر بوت الحماية: @N7L_STORE_bot"
            bot.send_message(target_user_id, f"{thanks_msg}\n{links}")
        elif prod_num == "4":
            links = "‏١- https://t.me/+PLLXva6AXRs0YTRk"
            bot.send_message(target_user_id, f"{thanks_msg}\n{links}")
        elif prod_num == "5":
            links = "‏١- https://t.me/+eRAj2HFhWTwzZDZk\n٢- يوزر بوت الحماية: @N7L_STORE_bot"
            bot.send_message(target_user_id, f"{thanks_msg}\n{links}")
        elif prod_num == "6":
            links = "١- يوزر بوت الحماية: @N7L_STORE_bot\n٢- https://t.me/+ZQQxOF8TELtiMTQ0"
            bot.send_message(target_user_id, f"{thanks_msg}\n{links}")
            
        bot.edit_message_text(f"✅ تم قبول طلب العميل {target_user_id} وتسليمه الروابط بنجاح.", call.message.chat.id, call.message.message_id)
        # إشعار مالك لإتمام الطلب
        bot.send_message(ADMIN_ID, f"📢 تنبيه: اكتمل طلب العميل {target_user_id} بنجاح.")
        
    elif action == "reject":
        bot.send_message(target_user_id, "❌ المعذرة، تم رفض إثبات الدفع الخاص بك. يرجى التأكد من الحوالة والمحاولة مجدداً أو مراسلة المالك.")
        bot.edit_message_text(f"❌ تم رفض طلب العميل {target_user_id}.", call.message.chat.id, call.message.message_id)

# تشغيل خادم الويب والبوت معاً في خيوط منفصلة لثبات الاتصال
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    print("🤖 N7L Store Bot starts polling now...")
    bot.infinity_polling(timeout=15, long_polling_timeout=5)
