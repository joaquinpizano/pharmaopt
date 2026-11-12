# PharmaOpt model audit

This audit records the evidence available in the published repository before
the product improvements in this release. It does not create new outcome
labels or claim prospective shortage-prediction performance.

## Modeling target

The integrated modeling notebook constructs one row per `package_ndc` and
`prediction_year` for 2022–2025. `shortage_target` is `1` when the package is
linked to an FDA `shortage_event` whose `initial_posting_date` falls within the
calendar year represented by that row; otherwise it is `0`. This is a
historical FDA shortage-event label, not a confirmed active-shortage state,
clinical outcome, or purchasing outcome.

The public dashboard uses the saved model scores from that experiment. Its
interactive evaluation labels are separate dashboard fields:

- `fda_event_any`: 96 2025 FDA-linked event flags.
- `discontinuation_notice_candidate`: 84 candidates.
- `non_discontinuation_event_candidate`: 12 candidates.

These dashboard labels are event-review indicators and must not be described
as active shortages.

## Evaluation design

The corrected notebook uses a chronological split:

- Training: 2022–2024, 541,240 package-year rows and 330 shortage labels.
- Evaluation: 2025, 221,667 package-year rows and 96 shortage labels.

The 2025 rows were repeatedly inspected during development, so this is a
previously inspected development holdout rather than an untouched prospective
test. The public dashboard's 500-package comparison is therefore a
retrospective ranking diagnostic.

The models are class-balanced logistic-regression pipelines. v0.4 uses the
historical shortage, product, recall, and CMS feature set. v0.5 adds
recall-language-derived features. Both produce ranking scores; the scores are
not calibrated probabilities.

## Leakage and timing checks

Confirmed safeguards in the integrated notebook include:

- prior shortage and recall features are filtered before each row's
  January 1 prediction cutoff;
- CMS features use the documented lagged mapping
  2019→2022, 2020→2023, 2021→2024, and 2022→2025;
- package-year keys and target values are checked for duplicates and valid
  binary values;
- the final split is chronological rather than random.

Remaining timing risks are documented rather than silently treated as solved:

- current-year active-product breadth is derived from the full year-specific
  population, so availability at January 1 is not fully demonstrated;
- CMS publication timing is not independently verified beyond the conservative
  source-year mapping;
- recall-language features use `report_date` as a provisional availability
  proxy, while descriptions may be edited after the historical cutoff;
- the repository contains the published scored dataset, not every raw source
  table required to rebuild the training panel from scratch.

These limitations mean that a substantial model rebuild or a claim of
prospective validity is not supported by the published inputs alone.

## Baselines and metrics for this release

The application now reports Precision@K, Recall@K, average precision, and
ROC-AUC for the saved v0.4 and v0.5 rankings against each selected 2025
dashboard event flag. It also shows a random-expectation baseline for each
review budget. The random baseline is an expected count, not a ranking model.

No estimated savings, clinical benefit, shortage prevention, probability, or
automated purchasing decision is inferred from these measurements.
