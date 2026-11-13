export type BudgetMetric = {
  model: "risk_score_v04" | "risk_score_v05";
  review_budget: number;
  captured: number;
  precision: number;
  recall: number;
  random_expected: number;
  lift_vs_random: number;
};

export const budgetMetrics: BudgetMetric[] = [
  [100, 1, .01, .0104167, .0433, 23.09, 0, 0, 0, .0433, 0],
  [250, 5, .02, .0520833, .1083, 46.18, 3, .012, .03125, .1083, 27.71],
  [500, 10, .02, .104167, .2165, 46.18, 7, .014, .072917, .2165, 32.33],
  [1000, 10, .01, .104167, .4331, 23.09, 7, .007, .072917, .4331, 16.16],
  [2500, 11, .0044, .114583, 1.0827, 10.16, 14, .0056, .145833, 1.0827, 12.93],
  [5000, 17, .0034, .177083, 2.1654, 7.85, 17, .0034, .177083, 2.1654, 7.85],
].flatMap((row) => {
  const [k, c04, p04, r04, , lift04, c05, p05, r05, , lift05] = row as number[];
  return [
    { model: "risk_score_v04" as const, review_budget: k, captured: c04, precision: p04, recall: r04, random_expected: k * 96 / 221667, lift_vs_random: lift04 },
    { model: "risk_score_v05" as const, review_budget: k, captured: c05, precision: p05, recall: r05, random_expected: k * 96 / 221667, lift_vs_random: lift05 },
  ];
});

export const modelMetrics = {
  risk_score_v04: { averagePrecision: 0.00389709, rocAuc: 0.77512 },
  risk_score_v05: { averagePrecision: 0.00285783, rocAuc: 0.749306 },
};

export const productMetrics = {
  risk_score_v04: { reviewedPackages: 636, flaggedPackages: 10, flaggedProducts: 9 },
  risk_score_v05: { reviewedPackages: 689, flaggedPackages: 7, flaggedProducts: 7 },
};

export const bootstrapMetrics = {
  risk_score_v04: { recall: "4.55%-17.48%", ap: "0.001887-0.008510" },
  risk_score_v05: { recall: "2.50%-12.77%", ap: "0.001467-0.006108" },
};

export const budgets = [100, 250, 500, 1000, 2500, 5000];

export function calculateReviewPlan(
  budget: number,
  reviewCost: number,
  capacity: number,
  totalPackages: number,
) {
  const selectedCount = Math.min(Math.floor(budget / reviewCost), capacity, totalPackages);
  const cost = selectedCount * reviewCost;
  return {
    selectedCount,
    cost,
    remaining: budget - cost,
  };
}
