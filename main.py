import os
import telebot
from flask import Flask

# إعدادات بوت الشراء N7L Store
TOKEN = "7330541999:AAFlV4eXun4U80vY4YWhZmsjUqGOfR9K_rM"
ADMIN_ID = 5650125883  # الآيدي الخاص بك كأدمن للمبيعات
STATS_FILE = "sales_log.txt"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# الحسابات البنكية التفصيلية لعمليات الشراء
BANK_DETAILS = """
🏦 مصرف الراجحي:
اسم الحساب: متجر N7L الرقمي
رقم الحساب: 247608010041234
الآيبان: SA73050000247608010041234

🏦 بنك STC Pay:
رقم المحفظة: 0551234567
"""

@app.route('/')
def index():
    return "N7L Purchase Bot is Running Successfully!"

# دالة لتسجيل عمليات الشراء
def log_sale(price):
    current_total = 0
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            content = f.read().strip()
            if content.isdigit():
                current_total = int(content)
    
    current_total += price
    with open(STATS_FILE, "w") as f:
        f.write(str(current_total))

# أمر عرض الأرباح والإحصائيات (للأدمن فقط بكود إنجليزي لضمان استقرار السيرفر)
@bot.message_handler(commands=['my_stats'])
def show_statistics(message):
    if str(message.chat.id) != str(ADMIN_ID):
        return
    
    current_total = 0
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r") as f:
            content = f.read().strip()
            if content.isdigit():
                current_total = int(content)
                
    bot.reply_to(message, f"📊 إحصائيات متجر N7L:\n\n💰 إجمالي المبيعات والأرباح: {current_total} ريال")

# أمر الشراء وبداية العملية للزبون
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك في بوت الشراء لمتجر N7L Store! 🛒\n\n"
        "لإتمام عملية شراء المودات والتحقق، يرجى اتباع التعليمات المرسلة لك."
    )
    bot.reply_to(message, welcome_text)

# تشغيل الـ Dummy Server لتخطي فحص المنافذ في Render ويظل البوت شغال 24 ساعة
def run_dummy_server():
    import threading
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000))), daemon=True).start()

if __name__ == "__main__":
    run_dummy_server()
    print("🤖 Purchase Bot is polling now...")
    bot.infinity_polling()
