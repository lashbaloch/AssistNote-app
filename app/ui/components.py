import streamlit as st
from PIL import Image

from app.inference.detector import Detection, DetectionResult
from app.utils.labels import format_denominations


def render_app_frame_start(voice_enabled: bool) -> None:
    voice_state = "Voice on" if voice_enabled else "Voice off"
    st.markdown(
        f"""
        <div class="assist-topbar">
          <div class="app-logo">A</div>
          <div class="assist-pill">{voice_state}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home() -> bool:
    st.markdown(
        """
        <section class="hero">
          <h1>AssistNote</h1>
          <p class="hero-copy">
            AssistNote helps users recognise Australian banknotes using the camera and spoken feedback.
          </p>
          <div class="signal-strip">
            <div class="signal"><strong>Camera first</strong>Point and capture</div>
            <div class="signal"><strong>Spoken help</strong>Hear the result</div>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    return st.button("Start Scanning", type="primary")


def render_settings(default_confidence: float) -> tuple[float, bool]:
    with st.sidebar:
        st.header("Settings")
        threshold = st.slider(
            "Confidence threshold",
            min_value=0.10,
            max_value=0.90,
            value=default_confidence,
            step=0.05,
            help="Raise this if you want the app to be more careful before reading a result.",
        )
        voice_enabled = st.toggle("Voice feedback", value=True)
        st.caption("Simple demo settings for scanning and spoken feedback.")
    return threshold, voice_enabled


def render_scan_input(input_version: int) -> Image.Image | None:
    st.markdown(
        """
        <section class="assist-section">
          <div class="section-heading">
            <h2>Scan with Camera</h2>
            <p>Place the note in good light, then take a clear photo.</p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )

    camera_file = st.camera_input(
        "Take a photo of the banknote",
        label_visibility="collapsed",
        key=f"camera_{input_version}",
    )

    if camera_file is not None:
        return Image.open(camera_file)

    st.markdown('<section class="assist-section backup-section">', unsafe_allow_html=True)
    with st.expander("Upload an Image Instead"):
        uploaded_file = st.file_uploader(
            "Choose a banknote image",
            type=["jpg", "jpeg", "png"],
            key=f"upload_{input_version}",
        )
    st.markdown("</section>", unsafe_allow_html=True)

    if uploaded_file is not None:
        return Image.open(uploaded_file)

    return None


def render_empty_scan_state() -> None:
    st.markdown(
        """
        <section class="assist-section">
          <div class="quiet-card">
            <p>
              The camera is ready. For best results, keep the whole note inside the frame.
            </p>
          </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_result(result: DetectionResult, threshold: float) -> str:
    feedback = build_feedback_message(result, threshold)
    summary = summarise_result(result)
    st.markdown('<section class="assist-section">', unsafe_allow_html=True)
    st.subheader("Result")

    st.image(result.annotated_image, width="stretch")

    metric_confidence = f"{result.best_confidence:.0%}" if result.best_confidence else "0%"
    st.markdown(
        f"""
        <div class="result-grid">
          <div class="metric">
            <div class="metric-label">Detected Note</div>
            <div class="metric-value metric-note">{summary}</div>
          </div>
          <div class="metric">
            <div class="metric-label">Confidence Level</div>
            <div class="metric-value">{metric_confidence}</div>
          </div>
          <div class="metric">
            <div class="metric-label">Total Notes Found</div>
            <div class="metric-value">{result.note_count}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if result.detections:
        render_detection_list(result.detections)
    else:
        st.markdown(
            """
            <div class="retry">
              We couldn't recognise the note clearly. Please try again in better lighting or move the camera closer.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</section>", unsafe_allow_html=True)
    return feedback


def render_detection_list(detections: list[Detection]) -> None:
    if len(detections) <= 1:
        return

    st.markdown('<div class="mini-list">', unsafe_allow_html=True)
    for index, detection in enumerate(detections, start=1):
        st.markdown(
            f"""
            <div class="mini-row">
              <span>Note {index}: {detection.label}</span>
              <strong>{detection.confidence:.0%}</strong>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)


def summarise_result(result: DetectionResult) -> str:
    if not result.detections:
        return "No clear note"

    labels = [detection.label for detection in result.detections]
    unique_labels = list(dict.fromkeys(labels))
    if len(labels) > 1 and len(unique_labels) == 1:
        return f"{len(labels)} x {unique_labels[0]}"
    if len(labels) > 1:
        return "Multiple notes"
    return labels[0]


def build_feedback_message(result: DetectionResult, threshold: float) -> str:
    if not result.detections:
        return "No clear note detected. Please try again."

    labels = [detection.label for detection in result.detections]
    if len(labels) > 1:
        return f"Multiple notes detected. {format_denominations(labels)} detected."

    readable = labels[0].replace("AUD", " dollars")
    confidence = result.detections[0].confidence
    if confidence < threshold:
        return "Unable to recognise clearly, please try again"
    return f"{readable} detected"
