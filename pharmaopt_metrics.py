"""Transparent ranking metrics for the published PharmaOpt scores."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


DEFAULT_REVIEW_BUDGETS = (100, 250, 500, 1000, 2500, 5000)


def rank_packages(frame: pd.DataFrame, score_column: str) -> pd.DataFrame:
    """Return a deterministic descending ranking for one score column."""
    required = {"package_ndc", score_column}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing ranking columns: {sorted(missing)}")

    scores = pd.to_numeric(frame[score_column], errors="raise")
    if not np.isfinite(scores.to_numpy()).all():
        raise ValueError(f"Nonfinite ranking scores in {score_column}")

    ranked = frame.assign(**{score_column: scores}).sort_values(
        [score_column, "package_ndc"],
        ascending=[False, True],
        kind="mergesort",
    ).reset_index(drop=True)
    ranked["risk_rank"] = np.arange(1, len(ranked) + 1)
    return ranked


def _validate_target(frame: pd.DataFrame, target_column: str) -> np.ndarray:
    if target_column not in frame.columns:
        raise ValueError(f"Missing evaluation target: {target_column}")
    target = pd.to_numeric(frame[target_column], errors="raise").to_numpy()
    if not np.isin(target, [0, 1]).all():
        raise ValueError(f"Evaluation target must be binary: {target_column}")
    if target.sum() == 0 or target.sum() == len(target):
        raise ValueError(f"Evaluation target needs both classes: {target_column}")
    return target.astype(int)


def _average_precision(labels: np.ndarray, scores: np.ndarray) -> float:
    order = np.argsort(-scores, kind="stable")
    ordered_labels = labels[order]
    ordered_scores = scores[order]
    boundaries = np.r_[np.flatnonzero(np.diff(ordered_scores)) + 1, len(labels)]
    cumulative = np.cumsum(ordered_labels)
    previous_recall = 0.0
    result = 0.0
    positives = float(labels.sum())
    start = 0
    for end in boundaries:
        true_positives = float(cumulative[end - 1])
        recall = true_positives / positives
        precision = true_positives / end
        result += (recall - previous_recall) * precision
        previous_recall = recall
        start = end
    return float(result)


def _roc_auc(labels: np.ndarray, scores: np.ndarray) -> float:
    order = np.argsort(scores, kind="stable")
    sorted_scores = scores[order]
    ranks = np.empty(len(scores), dtype=float)
    boundaries = np.r_[0, np.flatnonzero(np.diff(sorted_scores)) + 1, len(scores)]
    for start, end in zip(boundaries[:-1], boundaries[1:]):
        ranks[order[start:end]] = (start + 1 + end) / 2
    positives = float(labels.sum())
    negatives = float(len(labels) - labels.sum())
    return float(
        (ranks[labels == 1].sum() - positives * (positives + 1) / 2)
        / (positives * negatives)
    )


def evaluate_ranking(
    frame: pd.DataFrame,
    score_column: str,
    target_column: str,
    review_budgets: Iterable[int] = DEFAULT_REVIEW_BUDGETS,
) -> tuple[dict, pd.DataFrame]:
    """Measure ranking quality and budget-specific review capture."""
    labels = _validate_target(frame, target_column)
    ranked = rank_packages(
        frame.assign(_source_index=np.arange(len(frame))),
        score_column,
    )
    scores = ranked[score_column].to_numpy(dtype=float)
    ordered_labels = labels[ranked["_source_index"].to_numpy()]
    positive_count = int(labels.sum())
    base_rate = positive_count / len(labels)

    metrics = {
        "model": score_column,
        "target": target_column,
        "positives": positive_count,
        "positive_rate": base_rate,
        "average_precision": _average_precision(ordered_labels, scores),
        "roc_auc": _roc_auc(ordered_labels, scores),
    }

    rows = []
    for budget in review_budgets:
        if not isinstance(budget, (int, np.integer)) or budget <= 0:
            raise ValueError("Review budgets must be positive integers.")
        k = min(int(budget), len(ranked))
        captured = int(ordered_labels[:k].sum())
        precision = captured / k
        recall = captured / positive_count
        rows.append(
            {
                "model": score_column,
                "target": target_column,
                "review_budget": k,
                "captured": captured,
                "precision": precision,
                "recall": recall,
                "random_expected": k * base_rate,
                "lift_vs_random": precision / base_rate,
            }
        )
    return metrics, pd.DataFrame(rows)


def compare_rankings(
    frame: pd.DataFrame,
    score_columns: Iterable[str],
    target_column: str,
    review_budgets: Iterable[int] = DEFAULT_REVIEW_BUDGETS,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return model-level and budget-level comparison tables."""
    model_rows = []
    budget_frames = []
    for score_column in score_columns:
        metrics, budgets = evaluate_ranking(
            frame,
            score_column,
            target_column,
            review_budgets,
        )
        model_rows.append(metrics)
        budget_frames.append(budgets)
    return pd.DataFrame(model_rows), pd.concat(budget_frames, ignore_index=True)
