import unittest
from pathlib import Path

import pandas as pd

from pharmaopt_metrics import compare_rankings, evaluate_ranking, rank_packages


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


if __name__ == "__main__":
    unittest.main()
