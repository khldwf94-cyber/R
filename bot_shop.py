import os
import telebot

# هنا لن نضع التوكن مباشرة
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
# إكمال الكود لبوت الشراء
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً بك في متجر N7L STORE 🐝\nاختر رقماً للبدء:\n1- محاكي الحوادث\n2- شرح المودات\n3- بكج مودات\n4- سونرنر\n5- بكج محاكي\n6- بكج لعبتين")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text in ['1','2','3','4','5','6']:
        bot.reply_to(message, "تم اختيار الغرض! تفضل بيانات البنوك للتحويل:\n[الراجحي: XXXX]\n[الأهلي: XXXX]\nأرسل صورة الإيصال لإتمام طلبك.")
    else:
        bot.reply_to(message, "يرجى اختيار رقم صحيح من القائمة أعلاه.")

bot.infinity_polling()
