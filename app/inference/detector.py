from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from ultralytics import YOLO


@dataclass
class Detection:
    label: str
    confidence: float
    box: tuple[int, int, int, int]


@dataclass
class DetectionResult:
    detections: list[Detection]
    annotated_image: Image.Image
    best_label: str | None
    best_confidence: float
    note_count: int


class BanknoteDetector:
    def __init__(self, model_path: str | Path, class_names: dict[int, str] | dict[str, str] | None = None) -> None:
        self.model_path = Path(model_path)

        if not self.model_path.exists():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        self.model = YOLO(str(self.model_path))

        # Correct AssistNote class order from original obj.names:
        # 0 = 5AUD
        # 1 = 10AUD
        # 2 = 50AUD
        # 3 = 20AUD
        # 4 = 100AUD
        default_class_names = {
            0: "5_dollar",
            1: "10_dollar",
            2: "50_dollar",
            3: "20_dollar",
            4: "100_dollar",
        }

        if class_names:
            self.class_names = {int(k): v for k, v in class_names.items()}
        else:
            self.class_names = default_class_names

        # Do NOT use: self.model.names = self.class_names
        # Some Ultralytics/Torch versions do not allow assigning model.names directly.

    def predict_image(self, image: Image.Image, confidence_threshold: float = 0.50) -> DetectionResult:
        return self.predict(
            image=image,
            confidence_threshold=confidence_threshold,
            iou_threshold=0.45,
        )

    def predict(
        self,
        image: Image.Image,
        confidence_threshold: float = 0.50,
        iou_threshold: float = 0.45,
    ) -> DetectionResult:
        image = image.convert("RGB")

        results = self.model.predict(
            source=np.array(image),
            conf=confidence_threshold,
            iou=iou_threshold,
            imgsz=640,
            verbose=False,
        )

        raw_detections: list[Detection] = []

        if results and len(results) > 0:
            result = results[0]

            if result.boxes is not None:
                for box in result.boxes:
                    class_id = int(box.cls.item())
                    confidence = float(box.conf.item())

                    x1, y1, x2, y2 = box.xyxy[0].tolist()

                    label = self.class_names.get(class_id, f"class_{class_id}")

                    raw_detections.append(
                        Detection(
                            label=label,
                            confidence=confidence,
                            box=(int(x1), int(y1), int(x2), int(y2)),
                        )
                    )

        filtered_detections = self.remove_duplicate_boxes(
            raw_detections,
            overlap_threshold=0.35,
        )

        annotated_image = self.draw_detections(image, filtered_detections)

        if filtered_detections:
            best_detection = max(filtered_detections, key=lambda d: d.confidence)
            best_label = best_detection.label
            best_confidence = best_detection.confidence
        else:
            best_label = None
            best_confidence = 0.0

        return DetectionResult(
            detections=filtered_detections,
            annotated_image=annotated_image,
            best_label=best_label,
            best_confidence=best_confidence,
            note_count=len(filtered_detections),
        )

    @staticmethod
    def box_area(box: tuple[int, int, int, int]) -> int:
        x1, y1, x2, y2 = box
        return max(0, x2 - x1) * max(0, y2 - y1)

    @classmethod
    def box_iou(cls, box_a: tuple[int, int, int, int], box_b: tuple[int, int, int, int]) -> float:
        ax1, ay1, ax2, ay2 = box_a
        bx1, by1, bx2, by2 = box_b

        inter_x1 = max(ax1, bx1)
        inter_y1 = max(ay1, by1)
        inter_x2 = min(ax2, bx2)
        inter_y2 = min(ay2, by2)

        inter_area = cls.box_area((inter_x1, inter_y1, inter_x2, inter_y2))
        area_a = cls.box_area(box_a)
        area_b = cls.box_area(box_b)

        union = area_a + area_b - inter_area

        if union <= 0:
            return 0.0

        return inter_area / union

    @classmethod
    def overlap_ratio_smaller_box(
        cls,
        box_a: tuple[int, int, int, int],
        box_b: tuple[int, int, int, int],
    ) -> float:
        ax1, ay1, ax2, ay2 = box_a
        bx1, by1, bx2, by2 = box_b

        inter_x1 = max(ax1, bx1)
        inter_y1 = max(ay1, by1)
        inter_x2 = min(ax2, bx2)
        inter_y2 = min(ay2, by2)

        inter_area = cls.box_area((inter_x1, inter_y1, inter_x2, inter_y2))
        smaller_area = min(cls.box_area(box_a), cls.box_area(box_b))

        if smaller_area <= 0:
            return 0.0

        return inter_area / smaller_area

    @classmethod
    def remove_duplicate_boxes(
        cls,
        detections: list[Detection],
        overlap_threshold: float = 0.35,
    ) -> list[Detection]:
        if not detections:
            return []

        detections = sorted(detections, key=lambda d: d.confidence, reverse=True)
        kept: list[Detection] = []

        for detection in detections:
            is_duplicate = False

            for existing in kept:
                iou = cls.box_iou(detection.box, existing.box)
                smaller_overlap = cls.overlap_ratio_smaller_box(detection.box, existing.box)

                if iou >= overlap_threshold or smaller_overlap >= 0.55:
                    is_duplicate = True
                    break

            if not is_duplicate:
                kept.append(detection)

        return kept

    def draw_detections(self, image: Image.Image, detections: list[Detection]) -> Image.Image:
        annotated = image.copy()
        draw = ImageDraw.Draw(annotated)

        try:
            font = ImageFont.truetype("Arial.ttf", 18)
        except Exception:
            font = ImageFont.load_default()

        for detection in detections:
            x1, y1, x2, y2 = detection.box
            label_text = f"{detection.label} {detection.confidence:.0%}"

            draw.rectangle((x1, y1, x2, y2), outline=(0, 255, 120), width=4)

            text_bbox = draw.textbbox((x1, y1), label_text, font=font)
            text_w = text_bbox[2] - text_bbox[0]
            text_h = text_bbox[3] - text_bbox[1]

            label_y = max(0, y1 - text_h - 8)

            draw.rectangle(
                (x1, label_y, x1 + text_w + 8, label_y + text_h + 6),
                fill=(0, 255, 120),
            )
            draw.text(
                (x1 + 4, label_y + 3),
                label_text,
                fill=(0, 0, 0),
                font=font,
            )

        return annotated
