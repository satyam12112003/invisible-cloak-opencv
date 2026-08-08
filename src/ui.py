import cv2


class UI:

    def __init__(self, window_name):

        self.window_name = window_name

        cv2.namedWindow(
            self.window_name,
            cv2.WINDOW_NORMAL
        )

        cv2.resizeWindow(
            self.window_name,
            1100,
            700
        )

    def draw_header(
        self,
        frame,
        color,
        fps,
        background_ready
    ):

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (0, 0),
            (frame.shape[1], 75),
            (20, 20, 20),
            -1
        )

        frame = cv2.addWeighted(
            overlay,
            0.85,
            frame,
            0.15,
            0
        )

        cv2.putText(
            frame,
            "INVISIBLE CLOAK",
            (25, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        cv2.putText(
            frame,
            f"Color: {color}",
            (25, 62),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (200, 200, 200),
            1,
            cv2.LINE_AA
        )

        status = (
            "BACKGROUND READY"
            if background_ready
            else "CAPTURE BACKGROUND"
        )

        cv2.putText(
            frame,
            status,
            (frame.shape[1] - 300, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (frame.shape[1] - 130, 62),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (180, 180, 180),
            1,
            cv2.LINE_AA
        )

        return frame

    def draw_controls(self, frame):

        h, w = frame.shape[:2]

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (0, h - 55),
            (w, h),
            (20, 20, 20),
            -1
        )

        frame = cv2.addWeighted(
            overlay,
            0.85,
            frame,
            0.15,
            0
        )

        controls = (
            "[B] Background   "
            "[R] Red   "
            "[G] Green   "
            "[U] Blue   "
            "[Q] Quit"
        )

        cv2.putText(
            frame,
            controls,
            (20, h - 20),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (230, 230, 230),
            1,
            cv2.LINE_AA
        )

        return frame