# 💊 PharmaOpt
### Pharmaceutical Supply Chain Intelligence

**An independent healthcare analytics research project combining pharmaceutical data engineering, experimental machine-learning risk rankings, and interactive decision-support tools.**

PharmaOpt explores how publicly available pharmaceutical data can be integrated to investigate potential supply-chain vulnerabilities, identify patterns in regulatory events, and prioritize limited research resources.

![PharmaOpt Dashboard Overview](docs/images/dashboard-overview.png)

## Project Overview

Pharmaceutical supply chains involve complex relationships between drug products, National Drug Codes (NDCs), regulatory events, and product availability.

PharmaOpt integrates pharmaceutical datasets into a unified analytical workflow to explore how data-driven tools could support supply-chain research and decision-making.

**Core capabilities:**

- **Data Integration:** Standardizes and links pharmaceutical datasets using National Drug Codes (NDCs).
- **Risk Ranking:** Develops experimental models to prioritize pharmaceutical packages for further investigation.
- **Resource Allocation:** Simulates how hypothetical review budgets could be allocated across ranked products.
- **Model Evaluation:** Evaluates historical ranking performance against exploratory FDA event labels.
- **Interactive Analytics:** Provides an interactive Streamlit dashboard for exploring products, comparing models, and analyzing allocation scenarios.

## Interactive Dashboard

PharmaOpt includes a custom Streamlit dashboard designed to make complex pharmaceutical data easier to explore and interpret.

### Dashboard Features

| Section | Description |
|---|---|
| **Overview** | Displays package coverage, ranking priorities, and hypothetical resource allocation |
| **Drug Explorer** | Allows users to explore pharmaceutical products and their associated ranking information |
| **Model Evaluation** | Compares the performance of experimental risk-ranking models |
| **Methodology** | Explains data sources, research assumptions, and model limitations |

The dashboard currently analyzes **221,667 pharmaceutical package records** from the 2025 evaluation dataset.

Users can compare experimental models **v0.4 and v0.5**, adjust hypothetical review budgets, modify per-package review costs, and explore different prioritization scenarios.

## Data Engineering and Integration

PharmaOpt uses publicly available pharmaceutical data, including FDA drug product, shortage, and enforcement information, alongside additional research datasets
