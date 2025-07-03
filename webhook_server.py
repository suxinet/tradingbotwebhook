from flask import Flask, request
import requests

app = Flask(__name__)

# Telegram-Konfiguration
BOT_TOKEN = "8028126368:AAHPdzY5eM8C2eBleM135vnjmdqoEELBXpg"
CHAT_ID = 780956531  # Deine Telegram-Chat-ID

# Geheimer Schlüssel für Webhook-Zugriff
SECRET_KEY = "meinSuperGeheimerWebhookKey123"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    requests.post(url, data=data)

@app.route("/webhook", methods=["POST"])
def webhook():
    secret = request.headers.get("X-Secret-Key")
    if secret != SECRET_KEY:
        return "Forbidden", 403

    data = request.get_json()

    if not data:
        send_telegram_message("⚠️ Kein JSON empfangen.")
        return "No JSON", 400

    required_fields = ["symbol", "direction", "rr", "entry", "sl", "tp", "kapitalEmpfehlung", "sma_fast", "sma_slow"]
    if all(field in data for field in required_fields):
        message = (
            f"📡 *Trading Signal empfangen!*\n\n"
            f"🪙 Symbol: {data['symbol']}\n"
            f"📈 Richtung: {data['direction'].upper()}\n"
            f"🎯 Entry: {data['entry']}\n"
            f"🛑 Stop-Loss: {data['sl']}\n"
            f"✅ Take-Profit: {data['tp']}\n"
            f"📊 Risk/Reward: {data['rr']}\n"
            f"📎 SMA Fast: {data['sma_fast']}\n"
            f"📎 SMA Slow: {data['sma_slow']}\n"
            f"💰 Kapitalempfehlung: {data['kapitalEmpfehlung']}"
        )
        send_telegram_message(message)
        return "Signal verarbeitet", 200
    else:
        send_telegram_message("⚠️ Ungültiges Signalformat erhalten.")
        return "Fehlende Felder", 400

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)