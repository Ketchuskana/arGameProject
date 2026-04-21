import cv2
import numpy as np
import threading

class HeadControl:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.offset = 0.0
        self.running = True
        self.debug_frame = None
        self.prev_gray = None 

        self.thread = threading.Thread(target=self.update_loop, daemon=True)
        self.thread.start()

    def update_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if self.prev_gray is None:
                self.prev_gray = gray
                continue

            frame_delta = cv2.absdiff(self.prev_gray, gray)
            thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)

            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                c = max(contours, key=cv2.contourArea)
                if cv2.contourArea(c) > 800: 
                    (x, y, w, h) = cv2.boundingRect(c)
                    cX = x + (w // 2)
                    
                    target_offset = (cX / frame.shape[1]) - 0.5
                    

                    self.offset = self.offset * 0.8 + target_offset * 0.2
                    
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                else:
                    self.offset *= 0.9

            self.prev_gray = gray
            self.debug_frame = frame

    def stop(self):
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()