# AssistNote

AssistNote is a polished Streamlit GUI prototype for the university project **Real-Time Banknote Detection and Denomination Recognition with Audio Feedback for Visually Impaired Users**.

The app uses the included YOLO model to detect Australian banknotes from a phone-friendly camera capture, displays annotated results, and speaks clear feedback through the browser text-to-speech API.

## Features

- Mobile-first Streamlit interface with large touch targets and high-contrast styling
- Home screen with one clear primary action
- Camera capture workflow using `st.camera_input()`
- Image upload kept as a secondary backup option
- YOLO inference using `app/models/best.pt`
- Class labels loaded from `app/config/classes.json`
- Annotated image view with bounding boxes
- Simple result cards for detected note, confidence level, and total notes found
- Manual **Speak Result** button plus optional automatic voice feedback
- Browser-based audio feedback
- Low-confidence retry messaging
- Simple settings for confidence threshold and voice feedback

## Project Structure

```text
assistnote_codex_gui/
├── streamlit_app.py
├── requirements.txt
├── README.md
└── app/
    ├── AGENTS.md
    ├── config/
    │   ├── classes.json
    │   └── settings.py
    ├── docs/
    │   ├── gui_requirements.txt
    │   └── project_summary.txt
    ├── inference/
    │   ├── detector.py
    │   └── yolo_test_snippet.py
    ├── models/
    │   └── best.pt
    ├── sample_images/
    │   ├── sample1.jpg
    │   ├── sample2.jpg
    │   └── sample3.jpg
    ├── ui/
    │   ├── components.py
    │   └── styles.py
    └── utils/
        ├── audio.py
        └── labels.py
```

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Start the Streamlit app from the project root:

```bash
streamlit run streamlit_app.py
```

Open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## Demo Flow

1. Click **Start Scanning**.
2. Use **Scan with Camera** to capture a banknote photo.
3. Review the annotated image and the simple result cards.
4. Use **Speak Result** to replay the spoken result.
5. Use **Upload an Image Instead** only when a camera is not available.

## Notes

- The app currently prioritises camera capture for a phone-browser demo.
- Uploaded images are still supported as a backup path.
- If no detection passes the selected threshold, the app shows and speaks a retry message.
