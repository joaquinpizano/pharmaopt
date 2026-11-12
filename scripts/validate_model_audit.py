"""Check that the published modeling notebook retains its timing safeguards."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "notebooks" / "11_pharmaopt_integrated_pipeline_CMS_STRICT_REVIEW.ipynb"


def validate(path: Path = NOTEBOOK) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Missing modeling notebook: {path}")
    notebook = json.loads(path.read_text(encoding="utf-8"))
    source = "\n".join(
        "".join(cell.get("source", []))
        for cell in notebook.get("cells", [])
        if cell.get("cell_type") == "code"
    )
    required_fragments = {
        "chronological training split": 'prediction_year"] < 2025',
        "chronological evaluation split": 'prediction_year"] == 2025',
        "shortage cutoff": "initial_posting_date < %s",
        "recall cutoff": "recall_initiation_date < %s",
        "lagged CMS mapping": "expected_cms_year_map = {2019: 2022, 2020: 2023, 2021: 2024, 2022: 2025}",
        "package-year uniqueness": '["package_ndc", "prediction_year"]',
    }
    missing = [
        label for label, fragment in required_fragments.items()
        if fragment not in source
    ]
    if missing:
        raise ValueError(f"Missing model-audit safeguards: {missing}")


if __name__ == "__main__":
    validate()
    print("PASS: chronological split, cutoff filters, CMS lag, and key checks found.")
