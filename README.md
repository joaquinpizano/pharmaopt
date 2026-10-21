# 💊 PharmaOpt
### Pharmaceutical Supply Chain Intelligence

**An independent healthcare analytics research project combining pharmaceutical data engineering, machine-learning risk rankings, and interactive decision-support tools.**

PharmaOpt explores how publicly available pharmaceutical data can be integrated to help researchers investigate potential supply-chain vulnerabilities and prioritize limited review resources.

![PharmaOpt Dashboard Overview](docs/images/dashboard-overview.png)

## Project Overview

Pharmaceutical supply chains involve complex relationships between products, packaging identifiers, regulatory events, utilization, and availability. PharmaOpt brings several of these data sources into a unified analytical workflow.

The project includes:

- **Data integration:** Standardization and linkage of FDA pharmaceutical datasets using National Drug Codes (NDCs).
- **Risk ranking:** Experimental models that rank pharmaceutical packages for further research and review.
- **Resource allocation:** Interactive simulations that prioritize packages under hypothetical budgets and review costs.
- **Model evaluation:** Retrospective analysis of ranking performance against exploratory FDA event labels.
- **Interactive dashboard:** A Streamlit application for exploring products, comparing models, and examining allocation scenarios.

## Dashboard Features

| Section | Function |
|---|---|
| Overview | Summarizes package coverage and hypothetical resource allocation |
| Drug Explorer | Supports exploration of individual pharmaceutical products |
| Model Evaluation | Compares experimental ranking performance |
| Methodology | Documents assumptions, data sources, and limitations |

The dashboard currently analyzes **221,667 pharmaceutical package records** from the 2025 evaluation dataset.

Users can switch between experimental ranking models v0.4 and v0.5 and adjust hypothetical review budgets, costs, and package limits.

## Model Evaluation

The research workflow uses historical data from 2022–2024 and a retrospective 2025 evaluation.

In the current exploratory evaluation:

- The 2025 evaluation contains 12 identified non-discontinuation FDA event candidates.
- Both v0.4 and v0.5 captured 6 of those 12 candidates within the top 500 ranked packages.
- The models are intended for comparative ranking analysis, not validated predictions of active drug shortages.

These findings are preliminary and depend on the available data, event definitions, and evaluation methodology.

## Technology Stack

- **Python:** Data processing and analytical workflows
- **Pandas and NumPy:** Data manipulation and numerical analysis
- **MySQL:** Structured pharmaceutical data management
- **JupyterLab:** Research, experimentation, and model development
- **Streamlit:** Interactive application development
- **Plotly:** Interactive visualizations

## Running the Dashboard Locally

Install the required Python packages:

```bash
pip install streamlit pandas numpy plotly
```

Launch the application from the project directory:

```bash
streamlit run pharmaopt_dashboard.py
```

**Data requirement:** The dashboard currently expects the enriched evaluation dataset at:

```text
outputs/fda_outcome_definition/pharmaopt_2025_dashboard_enriched_v01.csv
```

This dataset is not included in the public repository. The dashboard therefore cannot run from a fresh clone without preparing or supplying the required data.

## Research Limitations

PharmaOpt is an experimental research prototype, not a production pharmaceutical supply-chain monitoring system.

- FDA event labels are not verified active-shortage outcomes.
- Risk scores are ranking indicators, not calibrated probabilities.
- Retrospective performance does not establish future predictive performance.
- Budget and resource-allocation calculations are hypothetical and do not represent realized cost savings.
- FDA labeler information does not necessarily identify the physical manufacturer.
- Results should not be used independently for clinical, procurement, or patient-care decisions.

## Project Status

**Version 1.0 — Functional research dashboard prototype**

The current version demonstrates integrated pharmaceutical data analysis, experimental ranking comparisons, and interactive allocation scenarios. Further work would be needed to validate outcomes, improve reproducibility, and establish real-world decision-support performance.

## Author

**Joaquin Pizano**  
University of South Florida — Artificial Intelligence and Business Analytics

[LinkedIn](https://www.linkedin.com/in/joaquinpizano) | [GitHub](https://github.com/joaquinpizano)
