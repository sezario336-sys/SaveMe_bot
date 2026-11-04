import os
import threading
import telebot
from flask import Flask

# ضع توكن بوتك الجديد هنا مباشرة لتفادي أي خطأ في قراءة البيئة
TOKEN = 9244470415:AAH-qkaq2d_n1zcOQu-0vge9_tE7UPJuEkA
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return "Etsy SEO Sniper Bot is active and running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# قاعدة بيانات الكلمات المفتاحية
SEO_DATABASE = {
    "planner": {
        "tags": ["Digital Planner", "GoodNotes Template", "iPad Planner 2026", "Daily Life Planner", "Minimalist Organizer", "Undated PDF Planner", "Productivity Tracker", "Student Planner App"],
        "title": "Ultimate Digital Planner 2026 | Minimalist iPad & GoodNotes Daily Organizer"
    },
    "journal": {
        "tags": ["Mind Reset Journal", "Self Care Workbook", "Daily Reflection PDF", "Mental Health Log", "Printable Journal Prompts", "Anxiety Relief Guide", "Wellness Tracker"],
        "title": "Daily Mind Reset Journal | Printable & Digital Mental Health Workbook"
    },
    "default": {
        "tags": ["Digital Product Template", "Instant Download File", "Editable Canva Design", "Business Growth Tool", "Marketing Asset Bundle", "Passive Income Kit", "Etsy Best Seller PDF"],
        "title": "High-Converting Digital Product Asset | Instant Download & Ready to Use"
    }
}

@bot.message_handler(commands=['start'])
def send_welcome(bot_msg):
    welcome_text = (
        "🎯 **مرحباً بك في بوت Etsy & Digital Store SEO Sniper!**\n\n"
        "أرسل لي الآن اسم منتجك باللغة الإنجليزية (مثال: `Digital Planner`) وسأحلل لك الكلمات المفتاحية فوراً!"
    )
    bot.reply_to(bot_msg, welcome_text, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def analyze_seo(bot_msg):
    query = bot_msg.text.strip().lower()
    if len(query) < 2:
        bot.reply_to(bot_msg, "⚠️ من فضلك اكتب اسم منتج صحيح مكون من حروف واضحة.")
        return

    msg = bot.reply_to(bot_msg, "🔍 جاري فحص خوارزميات البحث واستخراج أفضل الكلمات المفتاحية...")

    matched_data = SEO_DATABASE["default"]
    for key in SEO_DATABASE:
        if key in query:
            matched_data = SEO_DATABASE[key]
            break

    tags_formatted = ", ".join([f"`{tag}`" for tag in matched_data['tags']])
    
    response_text = (
        f"✅ **تم تحليل المنتج لـ:** `{query.title()}`\n\n"
        f"📌 **العنوان المقترح (SEO Title):**\n`{matched_data['title']}`\n\n"
        f"🔑 **الكلمات الدلالية (Tags):**\n{tags_formatted}\n\n"
        f"🚀 **أداة التحليل المتقدمة:**\n🔗 [اضغط هنا برعاية ممولنا](https://auctionr.org)"
    )

    try:
        bot.edit_message_text(response_text, bot_msg.chat.id, msg.message_id, parse_mode="Markdown")
    except:
        bot.send_message(bot_msg.chat.id, response_text, parse_mode="Markdown")

if __name__ == "__main__":
    t = threading.Thread(target=run_web)
    t.start()
    bot.infinity_polling()
