import cv2
import time
from recognition.face_recog import recognize_faces
from alerts.email_alert import send_email_alert
from alerts.telegram_alert import send_telegram_alert, start_bot_listener, get_owner_response, reset_owner_response
from alerts.whatsapp_alert import send_whatsapp_alert
from components.door_lock import DoorLock

def main():
    print("Starting Facial Recognition Security System...")
    video = cv2.VideoCapture(0)
    lock = DoorLock()

    stable_start_time = {}  
    updater = start_bot_listener()  

    while True:
        ret, frame = video.read()
        if not ret:
            continue


        face_names, face_locations = recognize_faces(frame)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255) 
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow("Facial Recognition", frame)
        current_time = time.time()

        if face_names:
            name = face_names[0]

            if name not in stable_start_time:
                stable_start_time.clear()  
                stable_start_time[name] = current_time
            else:
                if current_time - stable_start_time[name] >= 10:
                    if name != "Unknown":
                        print(f"[ACCESS GRANTED] ✅ Welcome {name}")
                        lock.unlock()
                        break  
                    else:
                        print("[ALERT] 🚨 Intruder detected!")
                        _, jpeg_img = cv2.imencode(".jpg", frame)
                        intruder_bytes = jpeg_img.tobytes()

                        send_email_alert("Intruder Alert!", "Unknown person detected!", intruder_bytes)
                        send_telegram_alert("🚨 Intruder detected! Reply with /unlock to open door.", intruder_bytes)
                        send_whatsapp_alert("🚨 Intruder detected at home!", intruder_bytes)

                        start_time = time.time()
                        while time.time() - start_time < 60:
                            time.sleep(1)
                            if get_owner_response() == "unlock":
                                print("[ACCESS GRANTED] ✅ Door unlocked via Telegram command.")
                                lock.unlock()
                                reset_owner_response()
                                break
                        break  
        else:
            stable_start_time.clear()  

        
        if cv2.waitKey(1) & 0xFF == 27:
            break

    updater.stop()
    video.release()
    cv2.destroyAllWindows()
    print(" Program stopped")

if __name__ == "__main__":
    main()
