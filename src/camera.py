import cv2


class Camera:

    def __init__(self, camera_index=0):

        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            raise RuntimeError("Unable to open camera.")

        self.cap.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            1280
        )

        self.cap.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            720
        )

    def read(self):

        success, frame = self.cap.read()

        if not success:
            return None

        return cv2.flip(frame, 1)

    def release(self):

        self.cap.release()