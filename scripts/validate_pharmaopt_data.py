"""Validate the saved dashboard dataset used by the public application."""

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "pharmaopt_2025_dashboard_corrected_v01.csv.gz"
EXPECTED_ROWS = 221_667


def validate(path: Path = DATA_FILE) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Missing dashboard dataset: {path}")

    frame = pd.read_csv(path, dtype={"package_ndc": "string"}, low_memory=False)
    required = {
        "package_ndc",
        "prediction_year",
        "risk_score_v04",
        "risk_score_v05",
        "fda_event_any",
        "non_discontinuation_event_candidate",
        "discontinuation_notice_candidate",
    }
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    if len(frame) != EXPECTED_ROWS:
        raise ValueError(f"Expected {EXPECTED_ROWS:,} rows, found {len(frame):,}")
    if frame["package_ndc"].isna().any() or frame["package_ndc"].duplicated().any():
        raise ValueError("Package NDC values must be present and unique.")
    if set(frame["prediction_year"].unique()) != {2025}:
        raise ValueError("Dashboard data must contain only prediction year 2025.")

    targets = [
        "fda_event_any",
        "non_discontinuation_event_candidate",
        "discontinuation_notice_candidate",
    ]
    for column in ["risk_score_v04", "risk_score_v05"]:
        values = pd.to_numeric(frame[column], errors="raise").to_numpy()
        if not np.isfinite(values).all():
            raise ValueError(f"Nonfinite values in {column}.")
    for column in targets:
        values = pd.to_numeric(frame[column], errors="raise")
        if not values.isin([0, 1]).all():
            raise ValueError(f"Non-binary values in {column}.")
    derived_event = (
        frame["non_discontinuation_event_candidate"].eq(1)
        | frame["discontinuation_notice_candidate"].eq(1)
    ).astype(int)
    if not frame["fda_event_any"].eq(derived_event).all():
        raise ValueError("FDA event flags do not reconcile to their components.")

    return {
        "rows": len(frame),
        "event_flags": int(frame["fda_event_any"].sum()),
        "non_discontinuation_flags": int(
            frame["non_discontinuation_event_candidate"].sum()
        ),
        "discontinuation_flags": int(
            frame["discontinuation_notice_candidate"].sum()
        ),
    }


if __name__ == "__main__":
    result = validate()
    print(
        "PASS: "
        f"{result['rows']:,} rows, "
        f"{result['event_flags']} FDA-linked event flags, "
        f"{result['non_discontinuation_flags']} non-discontinuation candidates, "
        f"{result['discontinuation_flags']} discontinuation candidates."
    )
