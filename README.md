
# PharmaOpt

**Pharmaceutical Supply Chain Intelligence | Data Engineering · Machine Learning · NLP · Optimization**

[**Launch Live Dashboard**](https://pharmaopt.streamlit.app/) | [**GitHub Repository**](https://github.com/joaquinpizano/pharmaopt)

![PharmaOpt Dashboard](dashboard-overview.png)

> **Project Status: Active Development**
>
> PharmaOpt is an independent pharmaceutical supply-chain analytics research project. Its machine learning models produce experimental risk rankings, not validated shortage predictions or calibrated probabilities.

## Project Overview

PharmaOpt is an independent analytics project developed by Joaquin Pizano, an Artificial Intelligence & Business Analytics student at the University of South Florida.

The project investigates how publicly available pharmaceutical data can be integrated and analyzed to identify potential supply-risk signals and support transparent resource-allocation research.

It combines data engineering, relational databases, machine learning, natural language processing, and mathematical optimization into a single research workflow.

The project also includes a publicly deployed Streamlit dashboard that allows users to explore the 2025 pharmaceutical package dataset and compare experimental model results.

**Live Application:** https://pharmaopt.streamlit.app/

## Interactive Dashboard

The PharmaOpt dashboard contains four sections:

**Overview**
- Summary statistics and key indicators
- Pharmaceutical package-level data
- High-level risk-ranking results

**Drug Explorer**
- Interactive drug and package exploration
- Searchable and filterable records
- Experimental model scores

**Model Evaluation**
- Comparison of model versions v0.4 and v0.5
- Precision-recall evaluation
- Top-ranked package analysis

**Methodology**
- Data sources and definitions
- Modeling assumptions
- Research limitations and interpretation guidance

The deployed 2025 dataset contains **221,667 pharmaceutical package records**.

## Data Sources

PharmaOpt integrates publicly available datasets from:

- FDA National Drug Code (NDC) Directory
- FDA Drug Shortages
- FDA Drug Enforcement / Recall Reports
- CMS Medicare Part D Utilization

CMS utilization is used as a partial demand-pressure proxy and does not represent total U.S. pharmaceutical demand.

## Data Integration Results

| Research Component | Result |
|---|---|
| FDA Product Records | 138,217 |
| FDA Package NDCs | 256,383 |
| FDA Shortage Records | 1,601 |
| Unique Shortage NDCs | 1,570 |
| Successfully Matched Shortage NDCs | 1,393 |
| NDC Match Rate | 88.73% |
| FDA Recall Events | 17,975 |
| Historical Package-Year Observations | 762,907 |
| 2025 Dashboard Package Records | 221,667 |

The historical modeling dataset spans 2022–2025.

Unmatched NDC identifiers were preserved rather than forcing potentially inaccurate matches.

## Machine Learning Research

PharmaOpt investigates rare-event pharmaceutical supply-risk ranking using historical FDA and CMS data.

The research compares two experimental models:

### Model v0.4

Uses FDA-linked historical signals and CMS utilization features to rank pharmaceutical packages.

### Model v0.5

Extends the previous model with additional features derived from recall-language analysis.

### Model Evaluation Results

| Metric | v0.4 | v0.5 |
|---|---:|---:|
| 2025 PR-AUC | .003897 | 0.002858 |
| Positive Flags Captured in Top 500 | 10 of 96 | 7 of 96 |

**Key Finding:** Adding the tested recall-language features did not improve ranking performance.

This negative result is retained as part of the research process.

The 2025 evaluation cohort was examined during model development and therefore is not considered an independent final test.

The 96 FDA-linked positive flags in the 2025 dashboard include 84 discontinuation-notice candidates and 12 non-discontinuation-event candidates. They are not 96 independently verified active drug shortages.

## Natural Language Processing

PharmaOpt includes recall-language analysis designed to identify and categorize potential pharmaceutical quality and supply-risk signals.

Research components include:

- FDA recall-reason text analysis
- Rule-based recall categorization
- Natural language feature engineering
- Weakly supervised NLP experiments
- Evaluation of additional recall-derived model features

The rule-based recall taxonomy categorized **97.61% of the 17,975 recall records**.

These classifications describe recall language and should not be interpreted as independently validated shortage-risk outcomes.

## Resource Allocation Optimization

PharmaOpt also explores mathematical optimization as a potential pharmaceutical operations decision-support tool.

Using OR-Tools, the project compares hypothetical allocation strategies under operational constraints.

In a lisdexamfetamine case study, a balanced allocation policy produced a **14.87% reduction in the modeled demand-weighted unmet-demand objective** relative to proportional allocation.

This result comes from a simulation, not an observed improvement in real-world pharmaceutical availability.

## Technology Stack

**Programming and Analysis**
- Python
- pandas
- scikit-learn
- SQL
- MySQL
- Jupyter Notebook

**Machine Learning and Optimization**
- Rare-event classification and ranking
- NLP and TF-IDF
- OR-Tools
- Precision-recall evaluation

**Visualization and Deployment**
- Streamlit
- Plotly
- GitHub
- Tableau
- Excel

## Repository Structure

```text
pharmaopt/
├── README.md
├── pharmaopt_dashboard.py
├── requirements.txt
├── dashboard-overview.png
├── pharmaopt_2025_dashboard_enriched_v01 (1).csv.gz
├── docs/
├── notebooks/
└── sql/
```

The compressed dataset is stored in the repository root and is used by the deployed Streamlit dashboard.

Its filename and location must remain consistent with the `DATA_FILE` path in `pharmaopt_dashboard.py`.

## Research Limitations

PharmaOpt is an ongoing research prototype with several important limitations.

**Historical Data Quality**

Later FDA data snapshots may not accurately reconstruct historical pharmaceutical shortage conditions.

**Outcome Definitions**

Discontinuation notices, FDA-listed shortage records, and independently verified active shortages are not interchangeable.

**Rare-Event Modeling**

Historical positive outcomes are extremely uncommon, making model evaluation challenging.

**Model Validation**

The 2025 cohort has been repeatedly examined during development and is not an untouched final evaluation dataset.

**Risk Score Interpretation**

Model outputs represent experimental rankings rather than calibrated probabilities.

**Optimization Assumptions**

Allocation simulations rely on modeled supply, utilization proxies, and specified constraints rather than observed inventory and demand.

PharmaOpt is intended for educational research and portfolio demonstration, not medical or operational decision-making.

## Current Development Status

- [x] Integrate FDA pharmaceutical datasets
- [x] Develop relational MySQL data structures
- [x] Evaluate NDC matching and data quality
- [x] Build historical package-year modeling dataset
- [x] Develop experimental model v0.4
- [x] Evaluate recall-language model v0.5
- [x] Explore NLP-based recall analysis
- [x] Build constrained allocation simulations
- [x] Develop interactive Streamlit dashboard
- [x] Deploy dashboard publicly
- [ ] Further validate historical shortage labels
- [ ] Establish an independent final evaluation cohort
- [ ] Improve model evaluation and reproducibility
- [ ] Expand pharmaceutical operations research

## About the Developer

**Joaquin Pizano**

University of South Florida  
B.S. Artificial Intelligence & Business Analytics

PharmaOpt is an independent research and portfolio project developed to explore applications of analytics, machine learning, and optimization within pharmaceutical supply chains.

**Links**

- [Live PharmaOpt Dashboard](https://pharmaopt.streamlit.app/)
- [GitHub](https://github.com/joaquinpizano)
- [LinkedIn](https://www.linkedin.com/in/joaquinpizano/)
- Email: joaquinpizano@usf.edu

---

*Independent student research project. Not affiliated with or endorsed by the FDA, CMS, or the University of South Florida.*
