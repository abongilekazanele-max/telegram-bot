import requests
import time
import random
import os
from datetime import datetime, timedelta

TOKEN = os.getenv("TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/"

CHAT_ID = None

def send_message(chat_id, text):
    url = URL + "sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

def get_updates(offset=None):
    url = URL + "getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()

def generate_signal():
    pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]
    directions = ["BUY ⬆️", "SELL ⬇️"]

    pair = random.choice(pairs)
    direction = random.choice(directions)

    now = datetime.utcnow() + timedelta(hours=2)  # SAT time
    entry_time = now + timedelta(seconds=30)  # prep time

    time_str = entry_time.strftime("%H:%M:%S")

    message = f"""📊 {pair}
Signal: {direction}
Prep time: 30 seconds ⏳
Entry time (SAT): {time_str}
Expiry: 2 candles"""

    return message

def main():
    global CHAT_ID
    offset = None
    last_signal_time = 0

    while True:
        # Capture user chat ID
        updates = get_updates(offset)

        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1

                if "message" in update:
                    CHAT_ID = update["message"]["chat"]["id"]

        # Send signal every 60 seconds
        if CHAT_ID:
            current_time = time.time()
            if current_time - last_signal_time >= 60:
                signal = generate_signal()
                send_message(CHAT_ID, signal)
                last_signal_time = current_time

        time.sleep(2)

if __name__ == "__main__":
    main()


