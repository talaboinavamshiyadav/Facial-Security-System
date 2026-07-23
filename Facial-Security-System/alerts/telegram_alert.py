import io
import requests
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = "8481597794:AAGfJCRaVVDQvjU0yKKb7jkDrdNotj1afHo"
CHAT_ID = "1990226507"

owner_response = None  
def send_telegram_alert(message, image_bytes=None):
    try:
        url_msg = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url_msg, data={"chat_id": CHAT_ID, "text": message})

        if image_bytes:
            url_photo = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
            image_file = io.BytesIO(image_bytes)
            image_file.name = "intruder.jpg"  
            requests.post(url_photo, data={"chat_id": CHAT_ID}, files={"photo": image_file})

        print("[TELEGRAM] 📲 Alert sent.")
    except Exception as e:
        print(f"[TELEGRAM ERROR] {e}")

def unlock(update, context):
    global owner_response
    owner_response = "unlock"
    context.bot.send_message(chat_id=CHAT_ID, text="✅ Door will be unlocked.")

def start_bot_listener():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("unlock", unlock))
    updater.start_polling()
    return updater

def get_owner_response():
    global owner_response
    return owner_response

def reset_owner_response():
    global owner_response
    owner_response = None
