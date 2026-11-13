import unittest
from pathlib import Path

import pandas as pd

from pharmaopt_metrics import (
    aggregate_product_frame,
    cluster_bootstrap_ranking,
    compare_rankings,
    derive_product_ndc,
    evaluate_product_ranking,
    evaluate_ranking,
    rank_packages,
    seeded_random_review,
)


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "pharmaopt_2025_dashboard_corrected_v01.csv.gz"


class RankingMetricTests(unittest.TestCase):
    def test_ties_use_package_ndc_as_deterministic_order(self):
        frame = pd.DataFrame(
            {
                "package_ndc": ["B", "A", "C"],
                "score": [0.5, 0.5, 0.1],
            }
        )
        ranked = rank_packages(frame, "score")
        self.assertEqual(ranked["package_ndc"].tolist(), ["A", "B", "C"])
        self.assertEqual(ranked["risk_rank"].tolist(), [1, 2, 3])

    def test_budget_metrics_include_precision_recall_and_random_expectation(self):
        frame = pd.DataFrame(
            {
                "package_ndc": ["A", "B", "C", "D"],
                "score": [0.9, 0.8, 0.2, 0.1],
                "event": [1, 0, 1, 0],
            }
        )
        metrics, budgets = evaluate_ranking(frame, "score", "event", [2, 4])
        self.assertAlmostEqual(metrics["average_precision"], 0.8333333333)
        self.assertAlmostEqual(metrics["roc_auc"], 0.75)
        self.assertEqual(budgets["captured"].tolist(), [1, 2])
        self.assertEqual(budgets["precision"].tolist(), [0.5, 0.5])
        self.assertEqual(budgets["recall"].tolist(), [0.5, 1.0])
        self.assertEqual(budgets["random_expected"].tolist(), [1.0, 2.0])

    def test_published_scores_retain_expected_2025_comparison(self):
        frame = pd.read_csv(DATA_PATH, dtype={"package_ndc": "string"})
        self.assertEqual(len(frame), 221667)
        self.assertEqual(frame["fda_event_any"].sum(), 96)
        model_rows, budget_rows = compare_rankings(
            frame,
            ["risk_score_v04", "risk_score_v05"],
            "fda_event_any",
            [500],
        )
        self.assertEqual(
            budget_rows.set_index("model")["captured"].to_dict(),
            {"risk_score_v04": 10, "risk_score_v05": 7},
        )
        summary = model_rows.set_index("model")
        self.assertAlmostEqual(
            summary.loc["risk_score_v04", "average_precision"],
            0.00389709,
            places=8,
        )
        self.assertAlmostEqual(
            summary.loc["risk_score_v05", "average_precision"],
            0.00285783,
            places=8,
        )

    def test_product_derivation_and_aggregation_preserve_repeated_flags(self):
        frame = pd.DataFrame(
            {
                "package_ndc": ["0001-0001-01", "0001-0001-02", "0002-0002-01"],
                "score": [0.9, 0.8, 0.7],
                "event": [1, 1, 0],
            }
        )
        self.assertEqual(
            derive_product_ndc(frame["package_ndc"]).tolist(),
            ["0001-0001", "0001-0001", "0002-0002"],
        )
        products = aggregate_product_frame(frame, "score", "event")
        repeated = products.set_index("product_ndc").loc["0001-0001"]
        self.assertEqual(repeated["package_count"], 2)
        self.assertEqual(repeated["flagged_package_count"], 2)
        self.assertEqual(repeated["event"], 1)

    def test_product_ranking_reports_product_and_package_capture(self):
        frame = pd.DataFrame(
            {
                "package_ndc": ["0001-0001-01", "0001-0001-02", "0002-0002-01"],
                "score": [0.9, 0.8, 0.7],
                "event": [1, 1, 0],
            }
        )
        metrics, budgets = evaluate_product_ranking(frame, "score", "event", [1])
        self.assertEqual(metrics["products"], 2)
        self.assertEqual(budgets.loc[0, "reviewed_products"], 1)
        self.assertEqual(budgets.loc[0, "reviewed_packages"], 2)
        self.assertEqual(budgets.loc[0, "captured_flagged_packages"], 2)
        self.assertEqual(budgets.loc[0, "captured_unique_flagged_products"], 1)

    def test_seeded_random_and_cluster_bootstrap_are_reproducible(self):
        frame = pd.DataFrame(
            {
                "package_ndc": [
                    "0001-0001-01",
                    "0001-0001-02",
                    "0002-0002-01",
                    "0003-0003-01",
                ],
                "score": [0.9, 0.8, 0.7, 0.6],
                "event": [1, 1, 0, 0],
            }
        )
        first = seeded_random_review(frame, "event", [2], seed=7)
        second = seeded_random_review(frame, "event", [2], seed=7)
        self.assertTrue(first.equals(second))
        bootstrap = cluster_bootstrap_ranking(
            frame, "score", "event", [2], replicates=20, seed=7
        )
        self.assertEqual(set(bootstrap["metric"]), {"recall", "average_precision", "roc_auc"})
        self.assertTrue((bootstrap["lower_95"] <= bootstrap["estimate"]).all())
        self.assertTrue((bootstrap["estimate"] <= bootstrap["upper_95"]).all())

    def test_seeded_random_is_invariant_to_input_row_order(self):
        frame = pd.DataFrame(
            {
                "package_ndc": ["0001-0001-01", "0001-0001-02", "0002-0002-01"],
                "score": [0.9, 0.8, 0.7],
                "event": [1, 0, 0],
            }
        )
        shuffled = frame.iloc[[2, 0, 1]].reset_index(drop=True)
        first = seeded_random_review(frame, "event", [2], seed=11)
        second = seeded_random_review(shuffled, "event", [2], seed=11)
        self.assertTrue(first.equals(second))

    def test_cluster_bootstrap_recall_uses_expanded_cluster_ranking(self):
        frame = pd.DataFrame(
            {
                "package_ndc": [
                    "0001-0001-01",
                    "0002-0002-01",
                    "0003-0003-01",
                    "0004-0004-01",
                ],
                "score": [0.9, 0.8, 0.7, 0.6],
                "event": [0, 1, 0, 0],
            }
        )
        result = cluster_bootstrap_ranking(
            frame, "score", "event", [2], replicates=1, seed=11
        )
        recall = result.loc[result["metric"].eq("recall"), "estimate"].iloc[0]
        self.assertEqual(recall, 0.0)


if __name__ == "__main__":
    unittest.main()
