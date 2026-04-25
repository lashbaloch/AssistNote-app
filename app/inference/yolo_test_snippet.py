from ultralytics import YOLO

MODEL_PATH = "app/models/best.pt"
CLASS_NAMES = ["5AUD", "10AUD", "50AUD", "20AUD", "100AUD"]

model = YOLO(MODEL_PATH)

def predict_image(image_path, conf=0.25, imgsz=640):
    """
    Run YOLO inference on one image and return Ultralytics results.
    """
    results = model.predict(
        source=image_path,
        conf=conf,
        imgsz=imgsz,
        save=False,
        verbose=False
    )
    return results
