import json
from pathlib import Path


def load_class_labels(path: Path) -> dict[int, str]:
    """Load YOLO class labels from a JSON map of id to readable label."""
    with path.open("r", encoding="utf-8") as label_file:
        raw_labels = json.load(label_file)

    return {int(class_id): label for class_id, label in raw_labels.items()}


def format_denominations(labels: list[str]) -> str:
    if not labels:
        return "No recognised notes"
    return ", ".join(label.replace("AUD", " dollars") for label in labels)
