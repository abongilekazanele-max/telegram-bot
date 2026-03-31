import requests
import time
import random
import os

TOKEN = os.getenv("TOKEN")
URL = f"https://api.telegram.org/bot{TOKEN}/"

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

    message = f"""📊 {pair}
Signal: {direction}
Expiry: 2 candles
Entry time: NOW"""

    return message

def main():
    offset = None

    while True:
        updates = get_updates(offset)

        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1

                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"].get("text", "")

                    if text.lower() == "signal":
                        signal = generate_signal()
                        send_message(chat_id, signal)

        time.sleep(2)

if __name__ == "__main__":
    main()
