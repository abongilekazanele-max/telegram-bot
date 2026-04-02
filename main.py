import os
import time
import requests

BOT_TOKEN = os.getenv("8581975485:AAGWI-4lmpgSbZ0TOkHbRWyMqUSmpe5thtY")
CHAT_ID = os.getenv("6674923900")

def send_signal(signal):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = f"📊 EUR/USD\n\n🔥 Signal: {signal}\n⏱ Expiry: 2 minutes"
    
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

def get_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=EURUSDT"
    data = requests.get(url).json()
    return float(data["price"])

print("Bot started...")

while True:
    try:
        price1 = get_price()
        time.sleep(60)
        price2 = get_price()

        if price2 > price1:
            send_signal("BUY 📈")
        else:
            send_signal("SELL 📉")

        print("Signal sent")
        time.sleep(60)

    except Exception as e:
        print("Error:", e)
        time.sleep(30)
