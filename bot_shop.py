import telebot

TOKEN = "8346972966:AAGJpcm8XOroKT4VE-o38Ky4JEHXILsb1-k"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "نورت متجر نحل! 🐝\nالرجاء إرسال اسمك، الآيدي، واليوزر لكي نبدأ.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text
    if "1" in text:
        bot.reply_to(message, "اخترت محاكي الحوادث. تفاصيل البنوك:\n[هنا سأضع لك تفاصيل البنوك لاحقاً]\nبعد التحويل أرسل الإيصال.")
    else:
        bot.reply_to(message, "أهلاً بك في N7L STORE. اختر غرضاً من 1 إلى 6.")

bot.infinity_polling()
