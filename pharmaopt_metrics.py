"""Transparent ranking metrics for the published PharmaOpt scores."""

from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd


DEFAULT_REVIEW_BUDGETS = (100, 250, 500, 1000, 2500, 5000)
DEFAULT_BOOTSTRAP_SEED = 20251112


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


def derive_product_ndc(
    package_ndc: pd.Series,
    *,
    strict: bool = True,
) -> pd.Series:
    """Derive the FDA product NDC from the labeler-product-package format."""
    values = package_ndc.astype("string").str.strip()
    parts = values.str.split("-")
    valid = values.notna() & parts.str.len().eq(3)
    if strict and not valid.all():
        raise ValueError(
            "Package NDC values must use the three-segment "
            "labeler-product-package format."
        )
    result = parts.str[:2].str.join("-")
    return result.where(valid)


def aggregate_product_frame(
    frame: pd.DataFrame,
    score_column: str,
    target_column: str,
) -> pd.DataFrame:
    """Aggregate package rows to product rows using max score and any label."""
    required = {"package_ndc", score_column, target_column}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Missing product aggregation columns: {sorted(missing)}")
    labels = _validate_target(frame, target_column)
    products = frame[["package_ndc", score_column]].copy()
    products["product_ndc"] = derive_product_ndc(
        products["package_ndc"], strict=False
    )
    products[target_column] = labels
    products = products.loc[products["product_ndc"].notna()].copy()
    return (
        products.groupby("product_ndc", as_index=False)
        .agg(
            **{
                score_column: (score_column, "max"),
                target_column: (target_column, "max"),
                "package_count": ("package_ndc", "size"),
                "flagged_package_count": (target_column, "sum"),
            }
        )
    )


def evaluate_product_ranking(
    frame: pd.DataFrame,
    score_column: str,
    target_column: str,
    review_budgets: Iterable[int] = DEFAULT_REVIEW_BUDGETS,
) -> tuple[dict, pd.DataFrame]:
    """Evaluate a max-score product ranking at a product review budget."""
    products = aggregate_product_frame(frame, score_column, target_column)
    metrics, budgets = evaluate_ranking(
        products.rename(columns={"product_ndc": "package_ndc"}),
        score_column,
        target_column,
        review_budgets,
    )
    ranked = rank_packages(
        products.rename(columns={"product_ndc": "package_ndc"}),
        score_column,
    )
    selected_rows = []
    for budget in budgets["review_budget"]:
        selected = ranked.head(int(budget))
        selected_rows.append(
            {
                "review_budget": int(budget),
                "reviewed_products": len(selected),
                "reviewed_packages": int(selected["package_count"].sum()),
                "captured_unique_flagged_products": int(
                    selected[target_column].sum()
                ),
                "captured_flagged_packages": int(
                    selected["flagged_package_count"].sum()
                ),
            }
        )
    product_details = pd.DataFrame(selected_rows)
    budgets = budgets.merge(product_details, on="review_budget", how="left")
    metrics["unit"] = "product"
    metrics["products"] = len(products)
    return metrics, budgets


def seeded_random_review(
    frame: pd.DataFrame,
    target_column: str,
    review_budgets: Iterable[int] = DEFAULT_REVIEW_BUDGETS,
    seed: int = DEFAULT_BOOTSTRAP_SEED,
) -> pd.DataFrame:
    """Select one deterministic seeded random package sample for each budget."""
    labels = _validate_target(frame, target_column)
    if "package_ndc" not in frame.columns:
        raise ValueError("Missing random-review identifier: package_ndc")
    stable_frame = frame.sort_values("package_ndc", kind="mergesort")
    stable_labels = pd.to_numeric(
        stable_frame[target_column], errors="raise"
    ).to_numpy(int)
    order = np.random.default_rng(seed).permutation(len(stable_frame))
    positive_count = int(labels.sum())
    base_rate = positive_count / len(labels)
    rows = []
    for budget in review_budgets:
        k = min(int(budget), len(frame))
        captured = int(stable_labels[order[:k]].sum())
        precision = captured / k
        rows.append(
            {
                "model": "seeded_random",
                "target": target_column,
                "seed": seed,
                "review_budget": k,
                "captured": captured,
                "precision": precision,
                "recall": captured / positive_count,
                "random_expected": k * base_rate,
                "lift_vs_random": precision / base_rate,
            }
        )
    return pd.DataFrame(rows)


def _weighted_average_precision(
    labels: np.ndarray,
    scores: np.ndarray,
    weights: np.ndarray,
) -> float:
    order = np.argsort(-scores, kind="stable")
    labels = labels[order]
    weights = weights[order]
    scores = scores[order]
    boundaries = np.r_[np.flatnonzero(np.diff(scores)) + 1, len(labels)]
    cumulative = np.cumsum(labels * weights)
    cumulative_weight = np.cumsum(weights)
    positives = float(np.sum(labels * weights))
    if positives == 0:
        return float("nan")
    end_indices = boundaries - 1
    recalls = cumulative[end_indices] / positives
    precisions = np.divide(
        cumulative[end_indices],
        cumulative_weight[end_indices],
        out=np.zeros_like(recalls),
        where=cumulative_weight[end_indices] > 0,
    )
    previous_recalls = np.r_[0.0, recalls[:-1]]
    return float(np.sum((recalls - previous_recalls) * precisions))


def _weighted_roc_auc(
    labels: np.ndarray,
    scores: np.ndarray,
    weights: np.ndarray,
) -> float:
    positives = float(np.sum(weights[labels == 1]))
    negatives = float(np.sum(weights[labels == 0]))
    if positives == 0 or negatives == 0:
        return float("nan")
    order = np.argsort(scores, kind="stable")
    sorted_scores = scores[order]
    sorted_weights = weights[order]
    sorted_labels = labels[order]
    boundaries = np.r_[np.flatnonzero(np.diff(sorted_scores)) + 1, len(labels)]
    group_ids = np.cumsum(np.r_[True, np.diff(sorted_scores) != 0]) - 1
    group_positive = np.bincount(
        group_ids, weights=sorted_weights * sorted_labels
    )
    group_negative = np.bincount(
        group_ids, weights=sorted_weights * (1 - sorted_labels)
    )
    negative_before = np.cumsum(group_negative) - group_negative
    auc_numerator = np.sum(
        group_positive * (negative_before + group_negative / 2)
    )
    return float(auc_numerator / (positives * negatives))


def cluster_bootstrap_ranking(
    frame: pd.DataFrame,
    score_column: str,
    target_column: str,
    review_budgets: Iterable[int] = DEFAULT_REVIEW_BUDGETS,
    replicates: int = 1000,
    seed: int = DEFAULT_BOOTSTRAP_SEED,
) -> pd.DataFrame:
    """Estimate ranking uncertainty by resampling product clusters.

    The observed package order is retained and each product cluster receives a
    bootstrap multiplicity. This avoids treating sibling packages as
    independent observations while preserving the original ranking rule.
    """
    if replicates <= 0:
        raise ValueError("Bootstrap replicates must be positive.")
    ranked = rank_packages(
        frame.assign(
            _product_ndc=derive_product_ndc(
                frame["package_ndc"], strict=False
            ).fillna("__unknown_product__")
        ),
        score_column,
    )
    _validate_target(ranked, target_column)
    labels = pd.to_numeric(ranked[target_column], errors="raise").to_numpy(int)
    products = ranked["_product_ndc"].to_numpy()
    unique_products, inverse = np.unique(products, return_inverse=True)
    rng = np.random.default_rng(seed)
    budget_values = [int(value) for value in review_budgets]
    metric_values = {budget: [] for budget in budget_values}
    ap_values = []
    roc_values = []
    for _ in range(replicates):
        sampled = rng.integers(0, len(unique_products), size=len(unique_products))
        counts = np.bincount(sampled, minlength=len(unique_products))
        weights = counts[inverse].astype(float)
        positive_weight = float(np.sum(labels * weights))
        if positive_weight == 0:
            continue
        scores = ranked[score_column].to_numpy(float)
        ap_values.append(_weighted_average_precision(labels, scores, weights))
        roc_values.append(_weighted_roc_auc(labels, scores, weights))
        for budget in budget_values:
            k = min(budget, len(ranked))
            cumulative_before = np.r_[0.0, np.cumsum(weights[:-1])]
            selected_weights = np.clip(
                k - cumulative_before, 0, weights
            )
            captured = float(np.sum(labels * selected_weights))
            metric_values[budget].append(captured / positive_weight)
    rows = [
        {
            "review_budget": budget,
            "metric": "recall",
            "estimate": float(np.median(metric_values[budget])),
            "lower_95": float(np.quantile(metric_values[budget], 0.025)),
            "upper_95": float(np.quantile(metric_values[budget], 0.975)),
            "seed": seed,
            "replicates": len(metric_values[budget]),
        }
        for budget in budget_values
    ]
    for metric, values in (
        ("average_precision", ap_values),
        ("roc_auc", roc_values),
    ):
        rows.append(
            {
                "review_budget": np.nan,
                "metric": metric,
                "estimate": float(np.median(values)),
                "lower_95": float(np.quantile(values, 0.025)),
                "upper_95": float(np.quantile(values, 0.975)),
                "seed": seed,
                "replicates": len(values),
            }
        )
    return pd.DataFrame(rows)
