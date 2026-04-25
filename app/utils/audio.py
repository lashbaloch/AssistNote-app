import html

import streamlit.components.v1 as components


def speak(message: str, enabled: bool = True) -> None:
    """Speak feedback in the browser using the Web Speech API."""
    if not enabled or not message:
        return

    safe_message = html.escape(message, quote=True)
    components.html(
        f"""
        <script>
          const text = "{safe_message}";
          if ("speechSynthesis" in window && text) {{
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.92;
            utterance.pitch = 1.0;
            utterance.volume = 1.0;
            window.speechSynthesis.speak(utterance);
          }}
        </script>
        """,
        height=0,
    )
