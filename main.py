import os
import time
import requests
import random

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_signal(signal):
    url=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    message = f"📊 EUR/USD\n\n🔥 Signal: {signal}\n⏰ Expiry: 2 minutes"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

def get_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT"
    data = requests.get(url).json()
    return float(data["price"])

print("Bot started...")

# ✅ TEST MESSAGE (you can remove later)
send_signal("TEST 🚀")

while True:
    try:
        price1 = get_price()
        time.sleep(60)
        price2 = get_price()

        if price2 > price1:
            send_signal("BUY 📈")
        else:
            send_signal("SELL 📉")

        time.sleep(120)

    except Exception as e:
        print("Error:", e)
        time.sleep(60)
send_signal("TEST 🚀")
