import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL

# ضع هنا التوكن الخاص ببوتك الذي أرسلته لي
TOKEN = "9244470415:AAFMRHsP6LL9mjsgOVN07rAetcG9_V5snFg"
bot = telebot.TeleBot(TOKEN)

# روابط إعلانات Adsterra الخاصة بك
AD_LINK_1 = "https://auctionr.org/4/ccfde0e6595e3e53ade83017c720ce7d"
AD_LINK_2 = "https://asiafilm.org/4/3c30e7e1aaae3c7a53addedef397debd"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك في بوت تحميل الفيديوهات الاحترافي! 🎬\n\n"
        "أرسل لي أي رابط فيديو من (تيك توك، إنستغرام، يوتيوب، فيسبوك) وسأقوم بتحميله لك فوراً بدون علامة مائية."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(message, "الرجاء إرسال رابط صحيح يبدأ بـ http أو https.")
        return

    sent_msg = bot.reply_to(message, "⏳ جاري معالجة وتحميل الفيديو، يرجى الانتظار قليلاً...")

    output_filename = "downloaded_video.mp4"
    
    ydl_opts = {
        'outtmpl': output_filename,
        'format': 'best',
        'noplaylist': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # إنشاء أزرار تفاعلية تتضمن روابط الإعلانات للربح
        markup = InlineKeyboardMarkup()
        btn_ad1 = InlineKeyboardButton("🔥 عرض مميز ودعم البوت", url=AD_LINK_1)
        btn_ad2 = InlineKeyboardButton("⭐ روابط ومواقع أخرى مفيدة", url=AD_LINK_2)
        markup.add(btn_ad1)
        markup.add(btn_ad2)

        with open(output_filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="تم تحميل الفيديو بنجاح بواسطة MOLCCI DG 📥\n\nsupport us by checking sponsors below 👇", reply_markup=markup)
        
        bot.delete_message(message.chat.id, sent_msg.message_id)

    except Exception as e:
        bot.edit_message_text("❌ حدث عطل أثناء تحميل الفيديو. تأكد أن الرابط عام وصحيح.", message.chat.id, sent_msg.message_id)
    
    finally:
        if os.path.exists(output_filename):
            os.remove(output_filename)

if __name__ == '__main__':
    print("البوت يعمل الآن بنجاح...")
    bot.infinity_polling()
