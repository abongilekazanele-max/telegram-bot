import requests
import time
import random

TOKEN = "8581975485:AAGWI-4lmpgSbZ0TOkHbRWyMqUSmpe5thtY"
URL = f"https://api.telegram.org/bot{TOKEN}/"

def get_updates(offset=None):
    url = URL + "getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(chat_id, text):
    url = URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]
actions = ["BUY", "SELL"]

print("🤖 Bot started...")

last_update_id = None
last_signal_time = time.time()

while True:
    updates = get_updates(last_update_id)

    if "result" in updates:
        for update in updates["result"]:
            last_update_id = update["update_id"] + 1

            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "").lower()

                print("Received:", text)

                if "start" in text:
                    send_message(chat_id, "Welcome Pinky 💖🔥\nType 'signal' or wait for auto signals 📊")

                if "signal" in text:
                    pair = random.choice(pairs)
                    action = random.choice(actions)

                    message = f"📊 {action} {pair} 🔥\n⏱ Expiry: 2 min\n🎯 Confidence: 85%"
                    send_message(chat_id, message)

    # AUTO SIGNAL EVERY 60 SECONDS
    if time.time() - last_signal_time > 60:
        last_signal_time = time.time()

        pair = random.choice(pairs)
        action = random.choice(actions)

        message = f"📊 {action} {pair} 🔥\n⏱ Expiry: 2 min\n🎯 Confidence: 85%"
        
        # ⚠️ replace with your chat_id after first message
        try:
            send_message(chat_id, message)
        except:
            pass

    time.sleep(2)
