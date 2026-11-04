import os
import threading
import telebot
from flask import Flask
from yt_dlp import YoutubeDL

# ضع توكن بوت التحميل الجديد هنا مباشرة
TOKEN = 9244470415:AAH-qkaq2d_n1zcOQu-0vge9_tE7UPJuEkA
bot = telebot.TeleBot(TOKEN)

# خادم ويب مصغر لترضية منصة Render وجعل الاستضافة مجانية 100%
app = Flask(__name__)

@app.route('/')
def home():
    return "Media Downloader Bot is active and running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# رسالة البدء /start
@bot.message_handler(commands=['start'])
def send_welcome(bot_msg):
    welcome_text = (
        "مرحباً بك في بوت تحميل الفيديوهات الشامل! 📥\n\n"
        "أرسل لي فقط رابط أي فيديو من:\n"
        "• تيك توك (TikTok)\n"
        "• إنستغرام (Instagram)\n"
        "• يوتيوب (YouTube)\n\n"
        "وسأقوم بتحميله وإرساله لك فوراً بجودة عالية!"
    )
    bot.reply_to(bot_msg, welcome_text)

# استقبال الروابط ومعالجتها
@bot.message_handler(func=lambda message: True)
def download_video(bot_msg):
    url = bot_msg.text.strip()
    
    if not url.startswith("http"):
        bot.reply_to(bot_msg, "⚠️ من فضلك أرسل رابطاً صحيحاً يبدأ بـ http أو https")
        return

    msg = bot.reply_to(bot_msg, "⏳ جاري معالجة وتحميل الفيديو، يرجى الانتظار ثواني...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'max_filesize': 50 * 1024 * 1024, # تحديد الحجم ليتوافق مع حدود تلغرام
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists("video.mp4"):
            with open("video.mp4", 'rb') as video:
                bot.send_video(
                    bot_msg.chat.id, 
                    video, 
                    caption="✅ تم التحميل بنجاح!\n\n🔗 روابط إضافية ممولة: [اضغط هنا](https://auctionr.org)"
                )
            os.remove("video.mp4")
            bot.delete_message(bot_msg.chat.id, msg.message_id)
        else:
            bot.edit_message_text("❌ عذراً، لم نتمكن من استخراج الملف. حاول مجدداً برابط آخر.", bot_msg.chat.id, msg.message_id)
            
    except Exception as e:
        try:
            bot.edit_message_text("❌ حدث خطأ أثناء التحميل: تأكد أن الرابط عام وليس خاصاً أو محميأ.", bot_msg.chat.id, msg.message_id)
        except:
            pass

if __name__ == "__main__":
    # تشغيل خادم الويب في الخلفية ليبقي البوت حياً ومستمراً
    t = threading.Thread(target=run_web)
    t.start()
    
    print("Media Downloader Bot is polling...")
    bot.infinity_polling()
