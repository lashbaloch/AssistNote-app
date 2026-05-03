from pathlib import Path
from ultralytics import YOLO

MODEL_PATH = Path("app/models/best.pt")
SAMPLE_DIR = Path("app/sample_images")

if not MODEL_PATH.exists():
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")

model = YOLO(str(MODEL_PATH))
images = []
for ext in ("*.jpg", "*.jpeg", "*.png", "*.webp"):
    images.extend(SAMPLE_DIR.glob(ext))

if not images:
    raise FileNotFoundError(f"No sample images found in {SAMPLE_DIR}")

print(f"Model: {MODEL_PATH}")
print(f"Testing {len(images)} sample images")

results = model.predict(
    source=[str(p) for p in images],
    conf=0.25,
    imgsz=640,
    save=True,
    project="runs_app_test",
    name="predictions",
    exist_ok=True,
)

print("Done. Prediction images saved to: runs_app_test/predictions")
