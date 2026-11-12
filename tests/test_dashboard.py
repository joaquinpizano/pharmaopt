import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


class DashboardSmokeTests(unittest.TestCase):
    def app(self):
        return AppTest.from_file(
            str(ROOT / "pharmaopt_dashboard.py"),
            default_timeout=60,
        )

    def test_startup_preserves_top_500_comparison(self):
        app = self.app().run()
        self.assertEqual(len(app.exception), 0)
        values = {metric.label: metric.value for metric in app.metric}
        self.assertEqual(values["Packages in the 2025 study"], "221,667")
        self.assertEqual(values["Packages selected for review"], "500")
        self.assertEqual(values["v0.4: top-500 capture"], "10 of 96")
        self.assertEqual(values["v0.5: top-500 capture"], "7 of 96")

    def test_budget_and_secondary_target_controls_recalculate(self):
        app = self.app().run()
        app.sidebar.slider[0].set_value(10000).run()
        self.assertEqual(len(app.exception), 0)
        values = {metric.label: metric.value for metric in app.metric}
        self.assertEqual(values["Packages selected for review"], "10")

        target = next(
            selectbox
            for selectbox in app.selectbox
            if "historical FDA record" in selectbox.label
        )
        target.set_value(
            "Non-discontinuation event candidates (smaller group)"
        ).run()
        self.assertEqual(len(app.exception), 0)
        values = {metric.label: metric.value for metric in app.metric}
        self.assertEqual(values["2025 dashboard event flags"], "12")
        self.assertEqual(values["v0.4: top-500 capture"], "6 of 12")
        self.assertEqual(values["v0.5: top-500 capture"], "6 of 12")


if __name__ == "__main__":
    unittest.main()
