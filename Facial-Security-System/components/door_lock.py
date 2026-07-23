import time

class DoorLock:
    def __init__(self):
        self.locked = True

    def unlock(self):
        if self.locked:
            print("[DOOR] ✅ WELLCOME DOOR UNLOCKED")
            self.locked = False
            time.sleep(2)
        else:
            print("[DOOR] Already unlocked.")

    def lock(self):
        if not self.locked:
            print("[DOOR] 🔒 Door locked again.")
            self.locked = True
        else:
            print("[DOOR] Already locked.")
