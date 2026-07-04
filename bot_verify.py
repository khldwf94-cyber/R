import os
import telebot

# هنا نستخدم متغير آمن، لن يسبب أي تنبيه تسريب
TOKEN = os.environ.get('VERIFY_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# ضع الآيدي الخاص بك هنا (تستطيع الحصول عليه من بوت @userinfobot)
ADMIN_ID = "ضع_الآيدي_الخاص_بك_هنا"

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    # إرسال الصورة للإدارة للتحقق منها
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"إيصال جديد من المستخدم: {message.chat.id}")
    bot.reply_to(message, "تم إرسال الإيصال للإدارة، سيتم التحقق منه قريباً. ✅")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أرسل صورة الإيصال هنا للتحقق من طلبك.")

bot.infinity_polling()
