import cv2

class HeadControl:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.direction = "center"

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        h, w, _ = frame.shape
        center_x = w // 2

        # fake tracking simple (tu amélioreras après)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # exemple simplifié
        if center_x < w * 0.4:
            self.direction = "left"
        elif center_x > w * 0.6:
            self.direction = "right"
        else:
            self.direction = "center"