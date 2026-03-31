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

    now = datetime.now()
    prep_time = now + timedelta(seconds=30)
    entry_time = now + timedelta(seconds=60)

    message = f"""📊 {pair}
Signal: {direction}
Prep time: {prep_time.strftime('%H:%M:%S')}
Entry time: {entry_time.strftime('%H:%M:%S')}
Expiry: 2 candles"""

    return message

def main():
    global CHAT_ID
    offset = None

    while True:
        updates = get_updates(offset)

        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1

                if "message" in update:
                    CHAT_ID = update["message"]["chat"]["id"]

        if CHAT_ID:
            signal = generate_signal()
            send_message(CHAT_ID, signal)
            time.sleep(60)

        time.sleep(2)

if __name__ == "__main__":
    main()
