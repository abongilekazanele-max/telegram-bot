import requests
import time
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

# 🔥 Get real market data
def get_price(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
        data = requests.get(url).json()
        return float(data["price"])
    except:
        return None

def generate_signal():
    pairs = {
        "EUR/USD": "EURUSDT",
        "GBP/USD": "GBPUSDT",
        "USD/JPY": "JPYUSDT",
        "AUD/USD": "AUDUSDT"
    }

    pair_name, symbol = list(pairs.items())[0]

    price1 = get_price(symbol)
    time.sleep(1)
    price2 = get_price(symbol)

    if price1 and price2:
        if price2 > price1:
            direction = "BUY ⬆️"
        else:
            direction = "SELL ⬇️"
    else:
        direction = "WAIT ⚠️"

    # SAT time
    now = datetime.utcnow() + timedelta(hours=2)
    entry_time = now + timedelta(seconds=30)

    message = f"""📊 {pair_name}
Signal: {direction}
Prep time: 30 seconds ⏳
Entry time (SAT): {entry_time.strftime('%H:%M:%S')}
Expiry: 2 minutes ⏱️"""

    return message

def main():
    global CHAT_ID
    offset = None
    last_signal_time = 0

    while True:
        updates = get_updates(offset)

        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1

                if "message" in update:
                    CHAT_ID = update["message"]["chat"]["id"]

        if CHAT_ID:
            current_time = time.time()
            if current_time - last_signal_time >= 60:
                signal = generate_signal()
                send_message(CHAT_ID, signal)
                last_signal_time = current_time

        time.sleep(2)

if __name__ == "__main__":
    main()

