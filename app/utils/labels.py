import json
from pathlib import Path


def load_class_labels(path: Path) -> dict[int, str]:
    """Load YOLO class labels from a JSON map of id to readable label."""
    with path.open("r", encoding="utf-8") as label_file:
        raw_labels = json.load(label_file)

    return {int(class_id): label for class_id, label in raw_labels.items()}


def human_readable_label(label: str) -> str:
    """Convert internal labels such as 20_dollar or 20AUD into speech-friendly text."""
    cleaned = label.strip()
    if cleaned.endswith("_dollar"):
        return cleaned.replace("_dollar", " dollars")
    if cleaned.endswith("AUD"):
        return cleaned.replace("AUD", " dollars")
    return cleaned.replace("_", " ")


def format_denominations(labels: list[str]) -> str:
    if not labels:
        return "No recognised notes"
    return ", ".join(human_readable_label(label) for label in labels)
