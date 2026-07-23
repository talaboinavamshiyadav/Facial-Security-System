from twilio.rest import Client
import os

ACCOUNT_SID = "ACb2cda2396f6be7d2bf4a1cb02a87458"
AUTH_TOKEN = "99c2672d444h8932294"
FROM_WHATSAPP = "whatsapp:+14155238886"
TO_WHATSAPP = "whatsapp:+91**********"

client = Client(ACCOUNT_SID, AUTH_TOKEN)


def send_whatsapp_alert(message, image_bytes=None):
    try:
        if image_bytes:
            tmp_file = "intruder.jpg"
            with open(tmp_file, "wb") as f:
                f.write(image_bytes)

            client.messages.create(
                from_=FROM_WHATSAPP,
                body=message,
                to=TO_WHATSAPP,
                media_url=[f"https://demo.twilio.com/owl.png"],
            )
        else:
            client.messages.create(from_=FROM_WHATSAPP, body=message, to=TO_WHATSAPP)
        print("[WHATSAPP] ✅ Alert sent.")
    except Exception as e:
        print(f"[WHATSAPP ERROR] {e}")
