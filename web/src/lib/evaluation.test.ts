import { describe, expect, it } from "vitest";
import { budgetMetrics, calculateReviewPlan, modelMetrics } from "./evaluation";

describe("review planning", () => {
  it("matches the Streamlit budget, cost, and capacity calculation", () => {
    expect(calculateReviewPlan(500000, 1000, 500, 221667)).toEqual({
      selectedCount: 500,
      cost: 500000,
      remaining: 0,
    });
  });

  it("caps selection at the cohort size and preserves unused budget", () => {
    expect(calculateReviewPlan(30000000, 100, 500000, 221667)).toEqual({
      selectedCount: 221667,
      cost: 22166700,
      remaining: 7833300,
    });
  });
});

describe("Evaluation v2 presentation data", () => {
  it("preserves the published 500-package comparison", () => {
    expect(budgetMetrics.filter((metric) => metric.review_budget === 500)).toEqual(
      expect.arrayContaining([
        expect.objectContaining({ model: "risk_score_v04", captured: 10, precision: 0.02, recall: 0.104167 }),
        expect.objectContaining({ model: "risk_score_v05", captured: 7, precision: 0.014, recall: 0.072917 }),
      ]),
    );
  });

  it("exposes the published ranking metrics without implying probabilities", () => {
    expect(modelMetrics.risk_score_v04.averagePrecision).toBeCloseTo(0.00389709);
    expect(modelMetrics.risk_score_v05.rocAuc).toBeCloseTo(0.749306);
  });
});
