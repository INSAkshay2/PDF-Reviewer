import csv
import logging
from pathlib import Path

from src.models import Document

logger = logging.getLogger(__name__)


def load_csv(file_path: str | Path) -> list[Document]:
    csv_path = Path(file_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    source_file = csv_path.name
    documents: list[Document] = []

    with open(csv_path, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError(f"CSV file '{source_file}' has no columns.")

        for i, row in enumerate(reader):
            text = ". ".join(f"{k}: {v}" for k, v in row.items() if v)
            if not text.strip():
                continue
            documents.append(Document(
                text=text,
                source=source_file,
                source_type="csv",
                page=1,
                metadata={"file_path": str(csv_path), "row": i + 1},
            ))

    if not documents:
        raise ValueError(f"No data rows found in CSV '{source_file}'.")

    return documents
