import os
import time
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_signal(signal):
url=
f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    message = f"📊 EUR/USD\n\n🔥 Signal: {signal}\n⏰ Expiry: 2 minutes"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })

def get_prices():
 url = "https://api.binance.com/api/v3/klines?symbol=EURUSDT&interval=1m&limit=20"
    data = requests.get(url).json()
    closes = [float(candle[4]) for candle in data]
    return closes

def calculate_rsi(prices):
    gains = []
    losses = []

    for i in range(1, len(prices)):
        diff = prices[i] - prices[i-1]
        if diff > 0:
            gains.append(diff)
        else:
            losses.append(abs(diff))

    avg_gain = sum(gains) / len(gains) if gains else 0.0001
    avg_loss = sum(losses) / len(losses) if losses else 0.0001

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

print("Smart bot running... 🚀")

last_signal = None

while True:
    try:
        prices = get_prices()
        rsi = calculate_rsi(prices)

        current = prices[-1]
        previous = prices[-2]

        # TREND + RSI LOGIC
        if rsi < 30 and current > previous:
            signal = "BUY 🟢 (Oversold reversal)"

        elif rsi > 70 and current < previous:
            signal = "SELL 🔴 (Overbought reversal)"

        else:
            signal = None

        if signal and signal != last_signal:
            send_signal(signal)
            last_signal = signal

        time.sleep(60)  # 1 minute

    except Exception as e:
        print("Error:", e)
        time.sleep(30)