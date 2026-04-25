from pathlib import Path


APP_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = APP_ROOT.parent

MODEL_PATH = APP_ROOT / "models" / "best.pt"
CLASSES_PATH = APP_ROOT / "config" / "classes.json"
SAMPLE_IMAGES_DIR = APP_ROOT / "sample_images"

DEFAULT_CONFIDENCE = 0.35
LOW_CONFIDENCE_FLOOR = 0.05
IMAGE_SIZE = 640

APP_TITLE = "AssistNote"
APP_SUBTITLE = "Real-time Australian banknote detection with audio feedback."
