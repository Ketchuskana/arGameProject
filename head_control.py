import cv2
import mediapipe as mp

class HeadControl:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.mp_face = mp.solutions.face_mesh
        self.face_mesh = self.mp_face.FaceMesh()
        self.direction = "center"

    def update(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(rgb)

        if result.multi_face_landmarks:
            face = result.multi_face_landmarks[0]

            # nez (point 1)
            nose = face.landmark[1]
            x = nose.x

            if x < 0.4:
                self.direction = "left"
            elif x > 0.6:
                self.direction = "right"
            else:
                self.direction = "center"