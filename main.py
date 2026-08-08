import cv2
import time

from src.camera import Camera
from src.config import (
    DEFAULT_COLOR,
    CAMERA_INDEX,
    WINDOW_NAME
)
from src.segmentation import CloakDetector
from src.ui import UI


def calculate_fps(previous_time):

    current_time = time.time()

    elapsed = current_time - previous_time

    if elapsed <= 0:
        return 0, current_time

    fps = 1 / elapsed

    return fps, current_time


def create_invisible_effect(
    frame,
    background,
    mask
):

    mask = cv2.GaussianBlur(
        mask,
        (9, 9),
        0
    )

    inverse_mask = cv2.bitwise_not(mask)

    visible_part = cv2.bitwise_and(
        frame,
        frame,
        mask=inverse_mask
    )

    invisible_part = cv2.bitwise_and(
        background,
        background,
        mask=mask
    )

    result = cv2.add(
        visible_part,
        invisible_part
    )

    return result


def capture_background(camera):

    print("\nCapturing background...")
    print("Please move out of the camera frame.")

    background = None

    for _ in range(30):

        frame = camera.read()

        if frame is not None:
            background = frame

        cv2.waitKey(30)

    if background is not None:
        print("Background captured successfully!")

    return background


def main():

    print("=" * 55)
    print("          INVISIBLE CLOAK - OPENCV")
    print("=" * 55)

    print("\nControls:")
    print("B = Capture background")
    print("R = Red cloak")
    print("G = Green cloak")
    print("U = Blue cloak")
    print("Q = Quit")

    try:

        camera = Camera(
            CAMERA_INDEX
        )

    except RuntimeError as error:

        print(f"\nERROR: {error}")

        return

    detector = CloakDetector(
        DEFAULT_COLOR
    )

    ui = UI(
        WINDOW_NAME
    )

    background = None

    previous_time = time.time()

    fps = 0

    while True:

        frame = camera.read()

        if frame is None:

            print("Unable to read frame.")

            break

        fps, previous_time = calculate_fps(
            previous_time
        )

        if background is None:

            display = frame.copy()

            display = ui.draw_header(
                display,
                detector.color,
                fps,
                False
            )

            cv2.putText(
                display,
                "Press B to capture background",
                (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

        else:

            mask = detector.detect(
                frame
            )

            result = create_invisible_effect(
                frame,
                background,
                mask
            )

            display = result

            display = ui.draw_header(
                display,
                detector.color,
                fps,
                True
            )

        display = ui.draw_controls(
            display
        )

        cv2.imshow(
            WINDOW_NAME,
            display
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):

            break

        elif key == ord("b"):

            background = capture_background(
                camera
            )

        elif key == ord("r"):

            detector.set_color(
                "RED"
            )

            print("Cloak color: RED")

        elif key == ord("g"):

            detector.set_color(
                "GREEN"
            )

            print("Cloak color: GREEN")

        elif key == ord("u"):

            detector.set_color(
                "BLUE"
            )

            print("Cloak color: BLUE")

    camera.release()

    cv2.destroyAllWindows()

    print("\nInvisible Cloak closed.")


if __name__ == "__main__":

    main()