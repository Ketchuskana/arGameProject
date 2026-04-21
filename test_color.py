import cv2
import numpy as np

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    h, w, _ = frame.shape
    pixel_center = hsv[h//2, w//2]
    
    cv2.circle(frame, (w//2, h//2), 5, (255, 0, 0), 2)
    cv2.putText(frame, f"HSV: {pixel_center}", (20, 50), 1, 2, (0, 255, 0), 2)
    cv2.imshow("Calibration", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()