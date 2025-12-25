import feedparser
import asyncio
import json
import os
from telegram import Bot

# تنظیمات
BOT_TOKEN = '8352605258:AAH8665umPVw_KYWkD8CyntomRPyebOX8BU' \
''
CHANNEL_ID = '@economic_on'
DELAY = 300  # هر ۵ دقیقه

# فقط نام رسانه‌ها (بدون سرویس)
RSS_FEEDS = {
    "ایسنا": "https://www.isna.ir/rss/tp/14",
    "ایسنا": "https://www.isna.ir/rss/tp/34",
    "ایسنا": "https://www.isna.ir/rss/tp/17",
    "مهر": "https://www.mehrnews.com/rss/tp/25",
    "مهر": "https://www.mehrnews.com/rss/tp/653",
    "مهر": "https://www.mehrnews.com/rss/tp/7",
    "مهر": "https://www.mehrnews.com/rss/tp/8",
    "میزان": "https://www.mizanonline.ir/fa/rss/11",
    "میزان": "https://www.mizanonline.ir/fa/rss/17",
    "YJC": "https://www.yjc.ir/fa/rss/3",
    "YJC": "https://www.yjc.ir/fa/rss/9",
    "YJC": "https://www.yjc.ir/fa/rss/6",
    "ایرنا": "https://www.irna.ir/rss/tp/20",
    "ایرنا": "https://www.irna.ir/rss/tp/1003421",
    "ایرنا": "https://www.irna.ir/rss/tp/33",
    "تسنیم": "https://www.tasnimnews.com/fa/rss/feeds/7/0/0/0",
    "تسنیم": "https://www.tasnimnews.com/fa/rss/feeds/1407/0/0/0",
    "تسنیم": "https://www.tasnimnews.com/fa/rss/feeds/1/0/0/0",
    "خانه ملت": "https://www.icana.ir/rss",
    "ریاست‌جمهوری": "https://president.ir/rss/all",
    "پایگاه دولت": "https://dolat.ir/view/rss.php"
}

SENT_LINKS_FILE = 'sent_links.json'

# بارگذاری لینک‌های قبلاً ارسال‌شده
def load_sent_links():
    if os.path.exists(SENT_LINKS_FILE):
        with open(SENT_LINKS_FILE, 'r', encoding='utf-8') as f:
            return set(json.load(f))
    return set()

# ذخیره لینک‌های جدید
def save_sent_links(sent_links):
    with open(SENT_LINKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(list(sent_links), f, ensure_ascii=False, indent=2)

# خواندن و ارسال خبرها
async def fetch_and_send_news(bot):
    sent_links = load_sent_links()

    for source, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)

        for entry in feed.entries:
            link = entry.link.strip()
            title = entry.title.strip()
            description = entry.get("description", "").strip()

            if link in sent_links:
                continue  # قبلاً ارسال شده

            # ساخت پیام
            if description:
                message = f"<b>{source}</b>\n\n<a href=\"{link}\">{title}</a>\n\n{description}"
            else:
                message = f"<b>{source}</b>\n\n<a href=\"{link}\">{title}</a>"

            try:
                await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=message,
                    parse_mode="HTML",
                    disable_web_page_preview=True
                )
                print(f"✅ ارسال شد: {title}")
                sent_links.add(link)
                save_sent_links(sent_links)
                await asyncio.sleep(2)
            except Exception as e:
                print(f"❌ خطا در ارسال پیام: {e}")
                continue

# حلقه اصلی
async def main():
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHANNEL_ID, text="✅ ربات آماده است!", disable_web_page_preview=True)

    while True:
        await fetch_and_send_news(bot)
        await asyncio.sleep(DELAY)

# اجرا
if __name__ == "__main__":
    asyncio.run(main())
