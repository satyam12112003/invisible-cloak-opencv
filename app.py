import cv2
import av
import time
import numpy as np
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Invisible Cloak | OpenCV",
    page_icon="🧥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    .hero {
        padding: 28px;
        border-radius: 22px;
        background: linear-gradient(
            135deg,
            rgba(70, 70, 70, 0.12),
            rgba(120, 120, 120, 0.04)
        );
        border: 1px solid rgba(128, 128, 128, 0.22);
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin: 0;
    }

    .hero-subtitle {
        font-size: 17px;
        opacity: 0.72;
        margin-top: 6px;
    }

    .footer {
        text-align: center;
        opacity: 0.6;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-title">🧥 Invisible Cloak</div>
        <div class="hero-subtitle">
            Real-time computer vision illusion powered by OpenCV + WebRTC
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SIDEBAR SETTINGS
# =========================================================

st.sidebar.header("🎨 Cloak Settings")

cloak_color = st.sidebar.selectbox(
    "Cloak Color",
    [
        "Red",
        "Green",
        "Blue",
        "Yellow",
        "Purple",
        "Orange",
        "Black",
        "White",
        "Custom",
    ],
)


sensitivity = st.sidebar.slider(
    "🎚️ Detection Sensitivity",
    min_value=1,
    max_value=100,
    value=55,
    step=1,
)


min_area = st.sidebar.slider(
    "🔎 Minimum Object Area",
    min_value=200,
    max_value=5000,
    value=700,
    step=100,
)


edge_softness = st.sidebar.slider(
    "✨ Edge Softness",
    min_value=1,
    max_value=15,
    value=7,
    step=2,
)


show_mask = st.sidebar.checkbox(
    "🧪 Show Detection Mask",
    value=False,
)


st.sidebar.divider()

st.sidebar.subheader("📖 How to use")

st.sidebar.markdown(
    """
    **1.** Keep the camera fixed.

    **2.** Stand away while calibration runs.

    **3.** Let the background reach 100%.

    **4.** Wear a solid-colored cloak.

    **5.** Come back in front of the camera.

    **6.** Adjust sensitivity if needed.
    """
)

st.sidebar.divider()

st.sidebar.warning(
    "Best results: fixed camera, stable lighting and a solid-colored cloth."
)


# =========================================================
# CUSTOM COLOR
# =========================================================

custom_hue = 60

if cloak_color == "Custom":

    custom_hue = st.sidebar.slider(
        "🌈 Custom Hue",
        min_value=0,
        max_value=179,
        value=60,
        step=1,
    )


# =========================================================
# COLOR RANGES
# HSV HUE = 0–179
# =========================================================

COLOR_RANGES = {

    "Red": [
        ((0, 70, 45), (12, 255, 255)),
        ((168, 70, 45), (179, 255, 255)),
    ],

    "Green": [
        ((30, 45, 35), (90, 255, 255)),
    ],

    "Blue": [
        ((88, 45, 35), (140, 255, 255)),
    ],

    "Yellow": [
        ((15, 55, 40), (40, 255, 255)),
    ],

    "Purple": [
        ((125, 40, 35), (170, 255, 255)),
    ],

    "Orange": [
        ((5, 55, 40), (25, 255, 255)),
    ],
}


# =========================================================
# CREATE COLOR MASK
# =========================================================

def create_color_mask(
    frame,
    selected_color,
    sensitivity,
    custom_hue_value,
):

    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV,
    )


    # =====================================================
    # BLACK
    # =====================================================

    if selected_color == "Black":

        # Higher sensitivity allows slightly brighter dark
        # objects to be detected.

        max_value = int(
            np.interp(
                sensitivity,
                [1, 100],
                [35, 85],
            )
        )

        lower = np.array(
            [0, 0, 0],
            dtype=np.uint8,
        )

        upper = np.array(
            [179, 255, max_value],
            dtype=np.uint8,
        )

        return cv2.inRange(
            hsv,
            lower,
            upper,
        )


    # =====================================================
    # WHITE
    # =====================================================

    if selected_color == "White":

        min_value = int(
            np.interp(
                sensitivity,
                [1, 100],
                [210, 145],
            )
        )

        max_saturation = int(
            np.interp(
                sensitivity,
                [1, 100],
                [45, 90],
            )
        )

        lower = np.array(
            [0, 0, min_value],
            dtype=np.uint8,
        )

        upper = np.array(
            [179, max_saturation, 255],
            dtype=np.uint8,
        )

        return cv2.inRange(
            hsv,
            lower,
            upper,
        )


    # =====================================================
    # COMMON SENSITIVITY
    # =====================================================

    sat_min = int(
        np.interp(
            sensitivity,
            [1, 100],
            [100, 25],
        )
    )

    val_min = int(
        np.interp(
            sensitivity,
            [1, 100],
            [100, 20],
        )
    )


    # =====================================================
    # CUSTOM COLOR
    # =====================================================

    if selected_color == "Custom":

        hue_width = int(
            np.interp(
                sensitivity,
                [1, 100],
                [5, 25],
            )
        )

        lower_h = max(
            0,
            custom_hue_value - hue_width,
        )

        upper_h = min(
            179,
            custom_hue_value + hue_width,
        )

        lower = np.array(
            [lower_h, sat_min, val_min],
            dtype=np.uint8,
        )

        upper = np.array(
            [upper_h, 255, 255],
            dtype=np.uint8,
        )

        return cv2.inRange(
            hsv,
            lower,
            upper,
        )


    # =====================================================
    # NORMAL COLORS
    # =====================================================

    mask = np.zeros(
        hsv.shape[:2],
        dtype=np.uint8,
    )


    for lower, upper in COLOR_RANGES[selected_color]:

        lower = list(lower)
        upper = list(upper)

        # Adjust minimum saturation
        lower[1] = min(
            lower[1],
            sat_min,
        )

        # Adjust minimum brightness
        lower[2] = min(
            lower[2],
            val_min,
        )

        current_mask = cv2.inRange(
            hsv,
            np.array(
                lower,
                dtype=np.uint8,
            ),
            np.array(
                upper,
                dtype=np.uint8,
            ),
        )

        mask = cv2.bitwise_or(
            mask,
            current_mask,
        )


    return mask


# =========================================================
# CLEAN MASK
# =========================================================

def clean_mask(
    mask,
    minimum_area,
):

    kernel_open = np.ones(
        (3, 3),
        np.uint8,
    )

    kernel_close = np.ones(
        (7, 7),
        np.uint8,
    )


    # Remove small noise
    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel_open,
        iterations=1,
    )


    # Fill small holes
    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel_close,
        iterations=2,
    )


    # Find connected regions
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )


    cleaned = np.zeros_like(
        mask
    )


    for contour in contours:

        area = cv2.contourArea(
            contour
        )

        if area >= minimum_area:

            cv2.drawContours(
                cleaned,
                [contour],
                -1,
                255,
                cv2.FILLED,
            )


    return cleaned


# =========================================================
# VIDEO PROCESSOR
# =========================================================

class InvisibleCloakProcessor:

    def __init__(self):

        self.background = None

        self.calibration_frames = []

        self.calibration_count = 0

        self.total_calibration_frames = 30

        self.last_time = time.time()

        self.fps = 0.0


    # =====================================================
    # BACKGROUND CALIBRATION
    # =====================================================

    def calibrate_background(
        self,
        frame,
    ):

        self.calibration_frames.append(
            frame.astype(np.float32)
        )

        self.calibration_count += 1


        if (
            self.calibration_count
            >= self.total_calibration_frames
        ):

            stack = np.stack(
                self.calibration_frames,
                axis=0,
            )


            # Median creates a stable background
            self.background = np.median(
                stack,
                axis=0,
            ).astype(
                np.uint8
            )


            self.calibration_frames.clear()


    # =====================================================
    # RESET BACKGROUND
    # =====================================================

    def reset_background(self):

        self.background = None

        self.calibration_frames.clear()

        self.calibration_count = 0


    # =====================================================
    # PROCESS FRAME
    # =====================================================

    def process(
        self,
        frame,
    ):

        image = frame.to_ndarray(
            format="bgr24",
        )


        # -------------------------------------------------
        # Resize
        # -------------------------------------------------

        image = cv2.resize(
            image,
            (640, 480),
            interpolation=cv2.INTER_AREA,
        )


        # -------------------------------------------------
        # Mirror camera
        # -------------------------------------------------

        image = cv2.flip(
            image,
            1,
        )


        # -------------------------------------------------
        # FPS
        # -------------------------------------------------

        current_time = time.time()

        elapsed = (
            current_time
            - self.last_time
        )


        if elapsed > 0:

            instant_fps = (
                1.0 / elapsed
            )

            self.fps = (
                self.fps * 0.9
                +
                instant_fps * 0.1
            )


        self.last_time = current_time


        # =================================================
        # BACKGROUND CALIBRATION
        # =================================================

        if self.background is None:

            self.calibrate_background(
                image,
            )

            output = image.copy()


            progress = int(
                (
                    self.calibration_count
                    /
                    self.total_calibration_frames
                )
                * 100
            )


            progress = min(
                progress,
                100,
            )


            # Calibration box
            cv2.rectangle(
                output,
                (15, 15),
                (625, 95),
                (0, 0, 0),
                -1,
            )


            cv2.putText(
                output,
                "CALIBRATING BACKGROUND",
                (30, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )


            cv2.putText(
                output,
                f"Progress: {progress}%",
                (30, 78),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )


            return av.VideoFrame.from_ndarray(
                output,
                format="bgr24",
            )


        # =================================================
        # CREATE MASK
        # =================================================

        mask = create_color_mask(
            image,
            cloak_color,
            sensitivity,
            custom_hue,
        )


        # =================================================
        # CLEAN MASK
        # =================================================

        mask = clean_mask(
            mask,
            min_area,
        )


        # =================================================
        # EDGE SOFTENING
        # =================================================

        kernel_size = int(
            edge_softness
        )


        if kernel_size % 2 == 0:

            kernel_size += 1


        mask = cv2.GaussianBlur(
            mask,
            (
                kernel_size,
                kernel_size,
            ),
            0,
        )


        # =================================================
        # ALPHA MASK
        # =================================================

        alpha = (
            mask.astype(
                np.float32
            )
            / 255.0
        )


        alpha = alpha[
            :,
            :,
            np.newaxis
        ]


        # =================================================
        # BACKGROUND REPLACEMENT
        # =================================================

        foreground = image.astype(
            np.float32
        )

        background = self.background.astype(
            np.float32
        )


        result = (
            foreground * (1.0 - alpha)
            +
            background * alpha
        )


        result = np.clip(
            result,
            0,
            255,
        ).astype(
            np.uint8
        )


        # =================================================
        # DETECTION MASK PREVIEW
        # =================================================

        if show_mask:

            mask_preview = cv2.cvtColor(
                mask,
                cv2.COLOR_GRAY2BGR,
            )


            result = cv2.addWeighted(
                result,
                0.75,
                mask_preview,
                0.25,
                0,
            )


        # =================================================
        # STATUS OVERLAY
        # =================================================

        cv2.rectangle(
            result,
            (15, 15),
            (625, 75),
            (0, 0, 0),
            -1,
        )


        cv2.putText(
            result,
            f"CLOAK: {cloak_color}",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
            cv2.LINE_AA,
        )


        cv2.putText(
            result,
            f"FPS: {self.fps:.1f}",
            (470, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )


        return av.VideoFrame.from_ndarray(
            result,
            format="bgr24",
        )


# =========================================================
# CAMERA SECTION
# =========================================================

st.subheader("🎥 Live Camera")

st.caption(
    "Keep your camera fixed while using the invisible cloak."
)


# =========================================================
# PROCESSOR
# =========================================================

if "cloak_processor" not in st.session_state:

    st.session_state.cloak_processor = (
        InvisibleCloakProcessor()
    )


processor = (
    st.session_state.cloak_processor
)


# =========================================================
# WEBRTC
# =========================================================

webrtc_streamer(
    key="invisible-cloak-v3",

    mode=WebRtcMode.SENDRECV,

    video_frame_callback=processor.process,

    media_stream_constraints={
        "video": {
            "width": {
                "ideal": 640
            },
            "height": {
                "ideal": 480
            },
            "frameRate": {
                "ideal": 15
            },
        },
        "audio": False,
    },

    rtc_configuration={
        "iceServers": [
            {
                "urls": [
                    "stun:stun.l.google.com:19302"
                ]
            }
        ]
    },
)


# =========================================================
# CONTROL PANEL
# =========================================================

st.divider()

st.subheader("🎮 Control Panel")


col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "🔄 Recalibrate Background",
        use_container_width=True,
    ):

        processor.reset_background()

        st.success(
            "Background calibration restarted."
        )


with col2:

    st.metric(
        "🎨 Detection",
        cloak_color,
    )


with col3:

    status = (
        "Ready"
        if processor.background is not None
        else "Calibrating"
    )

    st.metric(
        "📡 Status",
        status,
    )


# =========================================================
# TIPS
# =========================================================

st.divider()

st.subheader("💡 Tips for Best Results")


tip1, tip2, tip3 = st.columns(3)


with tip1:

    st.markdown(
        """
        **📷 Fixed Camera**

        Don't move the camera after calibration.
        """
    )


with tip2:

    st.markdown(
        """
        **💡 Good Lighting**

        Use even lighting and avoid strong shadows.
        """
    )


with tip3:

    st.markdown(
        """
        **🧥 Solid Cloth**

        Use a solid-colored cloth for better detection.
        """
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🧥 Invisible Cloak V3 · OpenCV · Python · Streamlit WebRTC
    </div>
    """,
    unsafe_allow_html=True,
)