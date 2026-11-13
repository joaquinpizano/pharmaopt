# PharmaOpt v2 research and development assessment

**Assessment date:** 2026-11-12
**Scope:** Published repository, saved 2025 dashboard cohort, model-audit
notebook, validation scripts, SQL schema, and existing tests.

## Executive conclusion

The published evidence supports a narrow conclusion: the saved v0.4 ranking
is better than the saved v0.5 ranking on this retrospective 2025
package-level event-label comparison. At a 500-package review budget, v0.4
captures 10 of 96 flags and v0.5 captures 7. Both rankings substantially
exceed the expected count from uniform random review, but absolute precision
is still only 2.00% and 1.40%, respectively.

This is not prospective shortage-prediction evidence. The 96 flags are
FDA-linked event-review indicators, including 84 discontinuation-notice
candidates and 12 non-discontinuation candidates. The 2025 cohort was
revisited during development, and the repository does not include every raw
source table needed to independently rebuild the model panel.

The smallest useful next phase is **not** RAG or generative AI. It is a
frozen, leakage-audited evaluation harness that evaluates v0.4, v0.5, random
review, and explicitly documented non-ML baselines on package and product
grains, with bootstrap uncertainty and event-type stratification. Narrative
retrieval should follow only after source snapshots, provenance, and
identifier-linkage tests are established.

## 1. Audit scope and evidence

Reviewed:

- [pharmaopt_metrics.py](../pharmaopt_metrics.py): deterministic ranking,
  Average Precision, ROC-AUC, Precision@K, Recall@K, random expected count,
  and lift.
- [test_pharmaopt_metrics.py](../tests/test_pharmaopt_metrics.py) and
  [test_dashboard.py](../tests/test_dashboard.py): regression expectations
  for the published cohort and dashboard.
- [validate_pharmaopt_data.py](../scripts/validate_pharmaopt_data.py):
  row, key, year, score, and label integrity checks.
- [validate_model_audit.py](../scripts/validate_model_audit.py): checks for
  chronological splitting, event/recall cutoffs, CMS lag, and package-year
  keys.
- [model-audit.md](model-audit.md) and
  [11_pharmaopt_integrated_pipeline_CMS_STRICT_REVIEW.ipynb](../notebooks/11_pharmaopt_integrated_pipeline_CMS_STRICT_REVIEW.ipynb):
  target construction, feature definitions, split, and timing caveats.
- [15_pharmaopt_fda_outcome_definition.ipynb](../notebooks/15_pharmaopt_fda_outcome_definition.ipynb):
  package-year event aggregation.
- [pharmaopt_schema.sql](../sql/pharmaopt_schema.sql) and FDA audit notebooks:
  source fields and matching structure.

The active file is
`pharmaopt_2025_dashboard_corrected_v01.csv.gz`. It contains 221,667 unique
2025 package NDCs, saved v0.4/v0.5 scores, labels, and descriptive package
fields; it does not contain the raw model features or event narratives.

## 2. Reproduced ranking metrics

### Evaluation population

| Quantity | Value |
|---|---:|
| 2025 package rows | 221,667 |
| Positive `fda_event_any` flags | 96 |
| Event prevalence | 0.04331% |
| Discontinuation candidates | 84 |
| Non-discontinuation candidates | 12 |
| Training rows documented in notebook (2022–2024) | 541,240 |
| Training shortage labels documented in notebook | 330 |
| Evaluation rows documented in notebook | 221,667 |
| Evaluation shortage labels documented in notebook | 96 |

`fda_event_any` is the maximum of the two event-candidate flags after
grouping FDA records by linked `package_ndc` and `prediction_year`. It is not
a verified future shortage label. The original model target is also an FDA
shortage-event label rather than a confirmed active-shortage state.

### Model-level metrics

| Model | Average precision / PR-AUC | ROC-AUC | 500 precision | 500 recall | 500 captured |
|---|---:|---:|---:|---:|---:|
| v0.4 | 0.003897090 | 0.775120 | 2.00% | 10.42% | 10/96 |
| v0.5 | 0.002857830 | 0.749306 | 1.40% | 7.29% | 7/96 |

The ranking implementation uses descending score order with `package_ndc` as
the deterministic tie-breaker. This reproduces the repository’s expected
Average Precision values and top-500 captures.

### Precision@K, Recall@K, and event capture

| K | v0.4 captured | v0.4 Precision@K | v0.4 Recall@K | v0.5 captured | v0.5 Precision@K | v0.5 Recall@K | Random expected |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 1 | 1.00% | 1.04% | 0 | 0.00% | 0.00% | 0.043 |
| 250 | 5 | 2.00% | 5.21% | 3 | 1.20% | 3.13% | 0.108 |
| 500 | 10 | 2.00% | 10.42% | 7 | 1.40% | 7.29% | 0.217 |
| 1,000 | 10 | 1.00% | 10.42% | 7 | 0.70% | 7.29% | 0.433 |
| 2,500 | 11 | 0.44% | 11.46% | 14 | 0.56% | 14.58% | 1.083 |
| 5,000 | 17 | 0.34% | 17.71% | 17 | 0.34% | 17.71% | 2.165 |

The random column is the expected event count under uniform review:
`K × 96 / 221,667`. Its expected precision is the base rate, 0.04331%, and
its expected recall is `K / 221,667` when sampling without replacement. It is
an expectation, not a realized random draw.

### Simple-baseline comparison

The saved dashboard cohort contains no utilization, prior-event, or raw
feature columns, so it cannot support a fair re-fit of popularity, prior
shortage, or demand baselines. The defensible baselines reproducible from the
published artifact are therefore:

1. **Uniform random review / prevalence baseline:** shown above.
2. **Saved-score rankings:** v0.4 and v0.5, evaluated with the same
   deterministic ordering and labels.

At K=500, v0.4 captures 10 versus 0.217 expected randomly, and v0.5 captures
7 versus 0.217. This corresponds to precision lift versus random of 46.18x
for v0.4 and 32.33x for v0.5. Lift is useful for ranking discrimination but
does not convert the labels into probabilities or operational benefit.

Adding a lexical NDC ordering or an arbitrary model score as a purported
business baseline would not be substantively defensible. A future benchmark
should add named, pre-specified baselines only when their source features and
time availability are available: prevalence/random, prior package event,
prior product event, utilization/popularity, and a simple regularized model.

## 3. Missed-event analysis

### Top 500 versus outside the top 500

| Ranking | Group | Packages | Event flags | Flag rate | Non-discontinuation | Discontinuation |
|---|---|---:|---:|---:|---:|---:|
| v0.4 | Top 500 | 500 | 10 | 2.000% | 6 | 4 |
| v0.4 | Outside top 500 | 221,167 | 86 | 0.0389% | 6 | 80 |
| v0.5 | Top 500 | 500 | 7 | 1.400% | 6 | 1 |
| v0.5 | Outside top 500 | 221,167 | 89 | 0.0402% | 6 | 83 |

The outside group includes the remaining 221,167 rows in the displayed
output only as a denominator correction: operationally it is the 221,167
rows after excluding the top 500 from the 221,667-row cohort. Its event count
is 86 for v0.4 and 89 for v0.5.

The most important pattern is label composition. Both models capture 6 of 12
non-discontinuation candidates in the top 500. The v0.4 advantage is entirely
in discontinuation candidates at this budget: 4 versus 1. Most missed flags
are therefore not a broad failure to capture the smaller non-discontinuation
group; they are missed discontinuation candidates.

### Exact flagged-package ranks

The first 20 flagged rows by rank show repeated packages from the same
product/manufacturer groups rather than 20 independent event situations.
For v0.4, flagged ranks include 57, 180–181, 187, 248, 267–269, and 400–401,
followed by flags at 2,000 and beyond. For v0.5, the corresponding early hits
include 197–201, 255–257, and 265, with later hits beginning at 1,667.

At K=500, the two rankings select 344 of the same 500 packages and share all
7 v0.5 event hits. v0.4 adds three event hits that v0.5 does not. At K=2,500,
v0.5 captures four additional hits, while the rankings share 10 event hits.
At K=5,000 they share 16 of 17 hits each.

### Package-level versus product-level concentration

The published dashboard does not include `product_ndc`, so the following is a
diagnostic heuristic: the product identifier is approximated by the first two
hyphen-separated segments of `package_ndc`. It must not replace the FDA
`product_id` relationship in a production evaluation.

| Diagnostic | Value |
|---|---:|
| Derived product groups | 112,967 |
| Products with at least one event flag | 83 |
| Flagged package rows | 96 |
| Products with 1 flagged package | 74 |
| Products with 2 flagged packages | 6 |
| Products with 3 flagged packages | 2 |
| Products with 4 flagged packages | 1 |

Thus 96 package flags represent 83 derived product groups. At K=500, v0.4
captures 10 packages from 9 derived products and v0.5 captures 7 packages
from 7 derived products. This matters because package-level Precision@K can
reward selecting multiple packages from one product, while a product-level
review workflow may count that as one opportunity.

### Score behavior and likely failure modes

Both rankings are highly concentrated at the top: the top-500 score ranges
are approximately 0.9968–1.0 for both models, while the outside rows extend
down to near zero. This separation makes the exact ordering of the many
high-scoring rows decisive. v0.5 changes that ordering enough to lose three
v0.4 top-500 hits, despite adding recall-language-derived features.

The notebook documents that v0.5 adds 16 qualitative historical risk
features and a linked recall-history indicator to the v0.4 feature set. Both
models use balanced logistic regression with the `liblinear` solver, but the
repository notes that prior experiments used different training solvers.
Therefore the v0.4/v0.5 result is an experiment-level comparison, not a
clean causal estimate of the value of recall language alone.

## 4. Label quality, leakage, imbalance, and matching

### Label quality

- The 2025 labels are aggregated FDA-linked event indicators, not verified
  future shortages.
- The 84/12 composition mixes discontinuation-notice candidates with other
  event candidates.
- A package can have multiple underlying FDA records; aggregation uses `max`
  flags and retains a record count in the outcome-definition notebook.
- The dashboard labels are joined on `package_ndc + prediction_year`, while
  the model target is constructed from linked shortage records by package and
  year.
- The 2025 cohort was repeatedly inspected during development, so it is a
  development holdout rather than an untouched final test.

### Temporal leakage

Evidence supporting the current safeguards:

- Training is `prediction_year < 2025`; evaluation is
  `prediction_year == 2025`.
- Shortage events use the year’s date window.
- Prior recall features filter `recall_initiation_date < index_date`.
- CMS mappings are explicitly lagged: 2019→2022, 2020→2023, 2021→2024,
  2022→2025.
- Package-year uniqueness and binary-target checks are present.

Remaining risks are material:

- Current-year active-product breadth uses the year-specific population and
  does not fully prove January 1 availability.
- CMS publication timing is not independently verified beyond the conservative
  source-year mapping.
- Recall descriptions may have been edited after the historical cutoff;
  `report_date` is used as a provisional availability proxy.
- The published repository lacks all raw source snapshots needed to rerun
  every feature calculation independently.

### Class imbalance

The evaluation prevalence is 96 / 221,667 = 0.04331%. This makes accuracy
uninformative and makes small absolute changes in captured events look large
in percentage terms. Precision@K, Recall@K, Average Precision, event counts,
and uncertainty intervals should be reported together. The class-balanced
training loss is not a correction for label uncertainty or selection bias.

### Package/product matching

The schema has a normalized `drug_product` table keyed by FDA `product_id`, a
`drug_package` table keyed by `package_ndc`, and nullable
`linked_package_ndc` fields for shortage and recall records. The recall audit
notebook reports 17,784/17,975 records with
`openfda.original_packager_product_ndc` (98.94%) but 14,739/17,975 with
package/product NDC fields (82.00%). This supports using exact linked package
keys where available, while treating unmatched and product-only matches as
explicit uncertainty rather than forcing package matches.

## 5. RAG feasibility assessment

### Source inventory

| Source | Structured identifiers | Narrative or explanatory fields | Potential use |
|---|---|---|---|
| FDA NDC/product/package directory | `product_id`, `product_ndc`, `package_ndc`, SPL ID, names, labeler | `package_description` | Canonical entity resolution and package context |
| FDA shortage records | source and linked package NDC, dates, status, availability, update type | `shortage_reason`, `therapeutic_category`, `presentation`, `resolved_note` | Event timeline and reason lookup |
| FDA recall records | recall number, linked package bridge, dates, classification, status, firm | `product_description`, `reason_for_recall`, `distribution_pattern`, notification text | Narrative evidence and recall context |
| CMS Part D features | normalized generic and year, claims/fills/cost | None in the saved dashboard artifact | Demand/popularity features, not narrative retrieval |
| Rule-based recall-risk outputs | recall number and linked package bridge | Derived categories from recall text | Auditable structured text signals |

The SQL schema explicitly preserves the most useful text fields in the
shortage and recall tables. The recall audit notebook also confirms that
`reason_for_recall` and `product_description` are populated in the inspected
recall extract. These are useful evidence documents, but they are not
necessarily contemporaneous, complete, or causal explanations.

### Matching reliability

The safest retrieval key is:

1. exact FDA `package_ndc` linked through the package bridge;
2. exact `product_id` / `product_ndc` when a package link is unavailable;
3. ingredient or normalized generic-name matching only as a separately labeled
   fallback.

A recall can affect many packages, and the schema models this as a recall
event plus a recall-package bridge. Unmatched links are nullable by design.
Therefore a retrieved narrative must display its matching level
(package/product/ingredient), match method, source identifier, and source
date. A generic-name match should never be presented as package-specific
evidence.

### Recommended retrieval baseline

Start with a non-generative, auditable retrieval service:

1. SQL exact matching on package NDC, product NDC, FDA product ID, recall
   number, and normalized generic/brand/labeler fields.
2. A keyword search index over `shortage_reason`, `resolved_note`,
   `reason_for_recall`, `product_description`, and
   `distribution_pattern`.
3. Filters for source date, event date, status, classification, and match
   level.
4. Results containing the original text, source table, source identifier,
   event date, retrieval date, and an exact source URL or record reference.

This provides useful evidence for a reviewer without introducing unsupported
claims. It also creates a measurable retrieval benchmark: exact-package
recall, product-level recall, top-k relevance, duplicate rate, and stale-date
rate.

### Whether embeddings/vector search add value

Not yet established. Embeddings could help with paraphrased reasons or
cross-source terminology, but the current repository provides no labeled
retrieval set, no documented source snapshot dates, and no evidence that
keyword/SQL matching fails on the intended review questions. The source
corpus is relatively structured and identifier-rich, so vector search should
be an experiment after the lexical baseline, not the next dependency.

Only adopt embeddings if a frozen relevance set shows a material improvement
in recall or reviewer time without increasing wrong-entity matches. A vector
index would also add refresh, deletion, provenance, and reproducibility
burden.

### Citation and generative-AI risks

Any future answer layer must:

- cite the exact FDA record, identifier, source date, and retrieved text span;
- distinguish event date, publication/report date, and retrieval date;
- state the match level and confidence;
- refuse to infer active shortage, causality, availability, clinical impact,
  or future risk from a narrative alone;
- avoid merging evidence from different products merely because names are
  similar;
- preserve the original source text alongside any summary;
- return “no supporting source found” rather than a plausible unsupported
  answer.

An LLM is not needed to implement the first retrieval phase. If introduced
later, it should summarize retrieved, cited evidence only, with automated
unsupported-claim and citation-coverage tests.

## 6. Prioritized implementation roadmap

| Priority | Improvement | Analytical value | Feasibility | Engineering effort | Portfolio impact | Decision |
|---:|---|---|---|---|---|---|
| 1 | Frozen evaluation harness with bootstrap CIs, random baseline, explicit simple baselines, and package/product metrics | Very high | High | Medium | High | Do next |
| 2 | Source snapshot and provenance manifest for NDC, shortage, recall, and CMS inputs | Very high | Medium | Medium | High | Required before new claims |
| 3 | Exact-key plus keyword evidence retrieval with cited records | High | High | Medium | High | First RAG phase |
| 4 | Matching audit for unmatched/product-only recall and shortage links | High | Medium | Medium | High | Run with retrieval |
| 5 | Refit v0.4/v0.5 under one solver/configuration and nested temporal validation | High | Medium | High | Medium | Model follow-up |
| 6 | Product-level or grouped review-budget evaluation | High | Medium | Medium | High | Pair with harness |
| 7 | Embedding/vector retrieval experiment against a labeled relevance set | Unknown until baseline | Medium | High | Medium | Gate on evidence |
| 8 | LLM evidence summarization with citation and claim controls | Unknown | Low/medium | High | High but risky | Defer |

Model improvements and evidence/AI work should remain separate:

- **Model track:** labels, temporal design, package/product grain, baselines,
  calibration only if justified, uncertainty, and prospective validation.
- **Evidence track:** source snapshots, exact matching, lexical retrieval,
  citations, provenance, and reviewer evaluation.
- **Generative track:** optional cited summarization after the evidence track
  proves source and match reliability.

## 7. Proposed next coding phase

Implement a development-only evaluation harness; do not change production
scores, validated datasets, or the Streamlit dashboard.

### Acceptance criteria

1. Reads the existing saved cohort without rewriting it.
2. Reproduces v0.4 and v0.5 metrics and all six K values in this report.
3. Reports random expected count and prevalence baseline at each K.
4. Accepts an FDA `product_id` mapping when available and reports both
   package-level and product-level metrics.
5. Reports all-event, discontinuation, and non-discontinuation results.
6. Produces bootstrap confidence intervals with a documented resampling unit
   (package or product) and seed.
7. Detects duplicate package-year keys, missing identifiers, nonbinary labels,
   and score ties.
8. Emits a machine-readable result file and a human-readable table without
   changing dashboard inputs.
9. Includes tests for the 96/84/12 counts, tie ordering, K boundaries, and
   package/product aggregation.

### Testing plan

- Run the existing unit and dashboard smoke tests unchanged.
- Add focused metric tests using a small synthetic tied-score fixture.
- Add a regression test for every currently reproduced v0.4/v0.5 count.
- Add tests that prove product-group resampling does not treat sibling
  packages as independent observations.
- Add validation for exact temporal cutoff fields before any future model
  refit.
- For retrieval, create a manually reviewed, versioned set of package-level,
  product-level, and no-match queries; measure exact-match recall,
  top-k keyword relevance, citation completeness, and wrong-entity rate.

## 8. Validation results

Commands run:

```text
python -m unittest discover -s tests -p "test_*.py"
PASS: 5 tests, 0 failures

python scripts/validate_pharmaopt_data.py
PASS: 221,667 rows, 96 FDA-linked event flags,
      12 non-discontinuation candidates, 84 discontinuation candidates.

python scripts/validate_model_audit.py
PASS: chronological split, cutoff filters, CMS lag, and key checks found.
```

The repository’s `requirements-dev.txt` installation was also attempted. The
runtime requirements installed successfully, but the pinned scikit-learn
1.7.2 package attempted a source build under the available Python 3.15 and
failed because no Windows C/C++ compiler was available. This did not block the
focused tests, which do not import scikit-learn. No repository files,
production outputs, validated datasets, or dashboard code were changed.
