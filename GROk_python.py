import requests
import time
from bs4 import BeautifulSoup
from telegram import Bot
import os
import asyncio
# Binance Announcements URL
BINANCE_ANNOUNCEMENT_URL = "https://www.binance.com/en/support/announcement"

# Telegram Bot Credentials
TELEGRAM_TOKEN = '7706675741:AAGusazMVZZpMPNC3oNCp58VDDdnmLGRADA'
CHAT_ID = '1086859780'

if not TELEGRAM_TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN environment variable!")

# Initialize Telegram bot
bot = Bot(token=TELEGRAM_TOKEN)
async def send_startup_message():
    await bot.send_message(chat_id=CHAT_ID, text="Bot is working!")

# Call the function using asyncio
asyncio.run(send_startup_message())

def get_latest_listing():
    """Fetch the latest announcement from Binance."""
    try:
        response = requests.get(BINANCE_ANNOUNCEMENT_URL)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Binance uses specific formatting, searching for relevant text
        articles = soup.find_all("a", string=lambda text: text and "Will List" in text)
        
        if articles:
            latest_announcement = articles[0]  # Get the most recent listing announcement
            title = latest_announcement.text
            link = "https://www.binance.com" + latest_announcement["href"]
            return title, link
        return None, None
    except Exception as e:
        print(f"Error fetching Binance announcements: {e}")
        return None, None

def notify_user(title, link):
    """Send a Telegram notification with the listing details."""
    message = f"🚀 Upcoming Binance Listing Alert! 🚀\n\n{title}\n🔗 {link}"
    bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    print("Starting Binance Pre-Listing Notifier...")
    last_seen = None

    while True:
        title, link = get_latest_listing()
        if title and title != last_seen:
            print(f"New pre-listing detected: {title}")
            notify_user(title, link)
            last_seen = title  # Avoid duplicate alerts
        
        time.sleep(60)  # Check every 1 minute

if __name__ == "__main__":
    main()
