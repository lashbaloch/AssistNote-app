from dataclasses import dataclass
import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault("YOLO_CONFIG_DIR", "/tmp/Ultralytics")

from ultralytics import YOLO

from app.config.settings import IMAGE_SIZE, LOW_CONFIDENCE_FLOOR


@dataclass(frozen=True)
class Detection:
    label: str
    confidence: float
    box: tuple[float, float, float, float]


@dataclass(frozen=True)
class DetectionResult:
    original_image: Image.Image
    annotated_image: Image.Image
    detections: list[Detection]
    low_confidence_detections: list[Detection]

    @property
    def note_count(self) -> int:
        return len(self.detections)

    @property
    def best_confidence(self) -> float:
        all_detections = self.detections or self.low_confidence_detections
        if not all_detections:
            return 0.0
        return max(detection.confidence for detection in all_detections)


class BanknoteDetector:
    """Small wrapper around the trained YOLO model."""

    def __init__(self, model_path: Path, class_labels: dict[int, str]) -> None:
        self.model_path = model_path
        self.class_labels = class_labels
        self.model = YOLO(str(model_path))

    def predict_image(self, image: Image.Image, confidence_threshold: float) -> DetectionResult:
        """Run inference on a PIL image and return display-ready results."""
        original = image.convert("RGB")
        source = np.asarray(original)

        results = self.model.predict(
            source=source,
            conf=LOW_CONFIDENCE_FLOOR,
            imgsz=IMAGE_SIZE,
            save=False,
            verbose=False,
        )
        result = results[0]

        detections: list[Detection] = []
        low_confidence: list[Detection] = []

        for box in result.boxes:
            class_id = int(box.cls.item())
            confidence = float(box.conf.item())
            xyxy = tuple(float(value) for value in box.xyxy[0].tolist())

            detection = Detection(
                label=self.class_labels.get(class_id, f"Class {class_id}"),
                confidence=confidence,
                box=xyxy,
            )

            if confidence >= confidence_threshold:
                detections.append(detection)
            else:
                low_confidence.append(detection)

        annotated = self._draw_annotations(original, detections)

        return DetectionResult(
            original_image=original,
            annotated_image=annotated,
            detections=detections,
            low_confidence_detections=low_confidence,
        )

    def _draw_annotations(self, image: Image.Image, detections: list[Detection]) -> Image.Image:
        canvas = image.copy()
        draw = ImageDraw.Draw(canvas)

        for detection in detections:
            x1, y1, x2, y2 = detection.box
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            label = f"{detection.label} {detection.confidence:.0%}"
            color = (31, 226, 144)

            # Draw bounding box
            draw.rectangle([x1, y1, x2, y2], outline=color, width=4)

            # Draw label background + text
            self._draw_label(draw, label, x1, y1, color)

        return canvas

    @staticmethod
    def _get_font(size: int = 20):
        """Try to load a nicer font, otherwise fall back safely."""
        try:
            return ImageFont.truetype("arial.ttf", size)
        except Exception:
            try:
                return ImageFont.truetype("DejaVuSans.ttf", size)
            except Exception:
                return ImageFont.load_default()

    def _draw_label(
        self,
        draw: ImageDraw.ImageDraw,
        label: str,
        x: int,
        y: int,
        color: tuple[int, int, int],
    ) -> None:
        font = self._get_font(20)

        bbox = draw.textbbox((x, y), label, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        padding_x = 10
        padding_y = 6
        top = max(y - text_height - padding_y * 2 - 4, 0)

        # Background rectangle
        draw.rectangle(
            [
                x,
                top,
                x + text_width + padding_x * 2,
                top + text_height + padding_y * 2,
            ],
            fill=color,
        )

        # Text
        draw.text(
            (x + padding_x, top + padding_y - 1),
            label,
            fill=(9, 15, 28),
            font=font,
        )

    def predict_frame(self, frame: np.ndarray, confidence_threshold: float) -> DetectionResult:
        """Future camera path: accept an RGB frame and reuse the same inference flow."""
        return self.predict_image(Image.fromarray(frame), confidence_threshold)
