import smtplib
import ssl
from email.message import EmailMessage
import cv2
import os

EMAIL_ADDRESS = "bunnyvignesh771@gmail.com"
EMAIL_PASSWORD = "qftv gmyu xqas jedm"  
TO_EMAIL = "vigneshpoloji@gmail.com"

def send_email_alert(subject, body, image_bytes=None):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL
        msg.set_content(body)

        if image_bytes:
            tmp_file = "intruder.jpg"
            with open(tmp_file, "wb") as f:
                f.write(image_bytes)
            with open(tmp_file, "rb") as f:
                msg.add_attachment(f.read(),
                                   maintype="image",
                                   subtype="jpeg",
                                   filename="intruder.jpg")
            os.remove(tmp_file)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("[EMAIL] 📩 Intruder alert sent.")
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")




