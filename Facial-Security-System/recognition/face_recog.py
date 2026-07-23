import os
import cv2
import face_recognition
import numpy as np

TOLERANCE = 0.45
MODEL = "hog"  

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWN_FACES_DIR = os.path.join(BASE_DIR, "..", "dataset", "known_faces")

print("[SYSTEM] Loading known faces...")

known_encodings = []
known_names = []

if not os.path.exists(KNOWN_FACES_DIR):
    print(f"[ERROR] Known faces directory not found: {KNOWN_FACES_DIR}")
else:
    for filename in os.listdir(KNOWN_FACES_DIR):
        filepath = os.path.join(KNOWN_FACES_DIR, filename)
        if not os.path.isfile(filepath):
            continue
        try:
            image = face_recognition.load_image_file(filepath)
            encodings = face_recognition.face_encodings(image)
            if len(encodings) == 0:
                print(f"[WARNING] No face found in {filename}, skipping.")
                continue
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(filename)[0])
        except Exception as e:
            print(f"[ERROR] Could not process {filename}: {e}")

print(f"[SYSTEM] Loaded {len(known_encodings)} known faces.")


def recognize_faces(frame):
    """
    Recognize all faces in the frame.
    Returns:
        face_names: list of names (or "Unknown")
        face_locations: list of tuples (top, right, bottom, left)
    """
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]

    face_locations_small = face_recognition.face_locations(rgb_small_frame, model=MODEL)
    face_locations = [(top*4, right*4, bottom*4, left*4) for (top, right, bottom, left) in face_locations_small]

    face_encodings = face_recognition.face_encodings(frame, face_locations)
    face_names = []

    for encoding in face_encodings:
        matches = face_recognition.compare_faces(known_encodings, encoding, TOLERANCE)
        distances = face_recognition.face_distance(known_encodings, encoding)
        name = "Unknown"
        if len(distances) > 0:
            best_idx = np.argmin(distances)
            if matches[best_idx]:
                name = known_names[best_idx]
        face_names.append(name)

    return face_names, face_locations
