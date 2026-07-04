import os
import telebot

TOKEN = os.environ.get('VERIFY_BOT_TOKEN') # توكن بوت التحقق
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = os.environ.get('ADMIN_ID') # آيديك الشخصي

@bot.message_handler(content_types=['photo', 'document', 'text'])
def handle_verify(message):
    # إعادة توجيه الإيصال لك
    if message.content_type == 'photo':
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"إيصال من: {message.chat.id}")
    elif message.content_type == 'document':
        bot.send_document(ADMIN_ID, message.document.file_id, caption=f"إيصال من: {message.chat.id}")
    else:
        bot.send_message(ADMIN_ID, f"رسالة من {message.chat.id}: {message.text}")
    
    bot.reply_to(message, "تم استلام طلبك، جاري التحقق من التحويل. ✅")

bot.infinity_polling()
