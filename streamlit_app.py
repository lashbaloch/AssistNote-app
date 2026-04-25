import streamlit as st

from app.config.settings import (
    APP_TITLE,
    CLASSES_PATH,
    DEFAULT_CONFIDENCE,
    MODEL_PATH,
)
from app.inference.detector import BanknoteDetector
from app.ui.components import (
    render_app_frame_start,
    render_empty_scan_state,
    render_home,
    render_result,
    render_scan_input,
    render_settings,
)
from app.ui.styles import apply_styles
from app.utils.audio import speak
from app.utils.labels import load_class_labels


st.set_page_config(
    page_title=f"{APP_TITLE} Demo",
    page_icon="A",
    layout="centered",
    initial_sidebar_state="collapsed",
)


@st.cache_resource(show_spinner="Loading AssistNote detector...")
def get_detector() -> BanknoteDetector:
    labels = load_class_labels(CLASSES_PATH)
    return BanknoteDetector(MODEL_PATH, labels)


def initialise_state() -> None:
    st.session_state.setdefault("screen", "home")
    st.session_state.setdefault("last_feedback", "")
    st.session_state.setdefault("scan_input_version", 0)


def main() -> None:
    initialise_state()
    apply_styles()

    threshold, voice_enabled = render_settings(DEFAULT_CONFIDENCE)

    render_app_frame_start(voice_enabled)
    if st.session_state.screen == "home":
        if render_home():
            st.session_state.screen = "scan"
            st.rerun()
    else:
        st.markdown(
            f"""
            <section class="hero">
              <h1>Scan a note</h1>
              <p class="hero-copy">Use the camera to check an Australian banknote and hear the result.</p>
            </section>
            """,
            unsafe_allow_html=True,
        )

        image = render_scan_input(st.session_state.scan_input_version)
        if image is None:
            render_empty_scan_state()
        else:
            detector = get_detector()
            with st.spinner("Scanning note..."):
                result = detector.predict_image(image, threshold)
            feedback = render_result(result, threshold)
            if st.button("Speak Result", type="primary"):
                speak(feedback, True)
            if feedback != st.session_state.last_feedback:
                speak(feedback, voice_enabled)
                st.session_state.last_feedback = feedback

            if st.button("Try Again"):
                st.session_state.last_feedback = ""
                st.session_state.scan_input_version += 1
                st.rerun()


if __name__ == "__main__":
    main()
