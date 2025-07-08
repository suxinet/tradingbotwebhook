import os
import sys
from flask import Flask, request
import requests
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus .env-Datei
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = int(os.getenv("CHAT_ID"))
SECRET_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    requests.post(url, json=payload)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        send_telegram_message("⚠️ Kein JSON empfangen.")
        return "No JSON", 400

    secret = data.get("secret")
    sys.stderr.write(f"[DEBUG] Secret im JSON: {secret}\n")
    sys.stderr.write(f"[DEBUG] SECRET_KEY aus ENV: {SECRET_KEY}\n")

    if secret != SECRET_KEY:
        return "Forbidden", 403

    required_fields = ["symbol", "direction", "rr", "entry", "sl", "tp", "sma_fast", "sma_slow", "kapitalEmpfehlung"]
    if not all(field in data for field in required_fields):
        send_telegram_message("⚠️ Fehlende Felder im JSON.")
        return "Fehlende Felder", 400

    msg = f"📈 <b>Trading-Signal</b>\n" \
          f"<b>Symbol:</b> {data['symbol']}\n" \
          f"<b>Richtung:</b> {data['direction']}\n" \
          f"<b>Entry:</b> {data['entry']}\n" \
          f"<b>Stop Loss:</b> {data['sl']}\n" \
          f"<b>Take Profit:</b> {data['tp']}\n" \
          f"<b>CRV:</b> {data['rr']}\n" \
          f"<b>SMA Fast:</b> {data['sma_fast']}\n" \
          f"<b>SMA Slow:</b> {data['sma_slow']}\n" \
          f"<b>Kapitalempfehlung:</b> {data['kapitalEmpfehlung']}"

    send_telegram_message(msg)
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=False, port=5000, host="0.0.0.0")
