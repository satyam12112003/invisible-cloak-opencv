import cv2
import numpy as np

from .config import (
    COLORS,
    MIN_CONTOUR_AREA,
    MORPH_KERNEL_SIZE
)


class CloakDetector:

    def __init__(self, color="RED"):

        self.color = color

        self.kernel = np.ones(
            (
                MORPH_KERNEL_SIZE,
                MORPH_KERNEL_SIZE
            ),
            np.uint8
        )

    def set_color(self, color):

        if color in COLORS:
            self.color = color

    def create_mask(self, frame):

        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV
        )

        mask = np.zeros(
            hsv.shape[:2],
            dtype=np.uint8
        )

        ranges = COLORS[self.color]

        for lower, upper in ranges:

            lower = np.array(lower)
            upper = np.array(upper)

            current_mask = cv2.inRange(
                hsv,
                lower,
                upper
            )

            mask = cv2.bitwise_or(
                mask,
                current_mask
            )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            self.kernel,
            iterations=2
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            self.kernel,
            iterations=2
        )

        mask = cv2.dilate(
            mask,
            self.kernel,
            iterations=1
        )

        mask = cv2.GaussianBlur(
            mask,
            (7, 7),
            0
        )

        return mask

    def get_largest_region(self, mask):

        binary = cv2.threshold(
            mask,
            100,
            255,
            cv2.THRESH_BINARY
        )[1]

        contours, _ = cv2.findContours(
            binary,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if not contours:
            return mask

        largest = max(
            contours,
            key=cv2.contourArea
        )

        if cv2.contourArea(largest) < MIN_CONTOUR_AREA:
            return np.zeros_like(mask)

        clean_mask = np.zeros_like(mask)

        cv2.drawContours(
            clean_mask,
            [largest],
            -1,
            255,
            thickness=cv2.FILLED
        )

        clean_mask = cv2.GaussianBlur(
            clean_mask,
            (9, 9),
            0
        )

        return clean_mask

    def detect(self, frame):

        mask = self.create_mask(frame)

        mask = self.get_largest_region(mask)

        return mask