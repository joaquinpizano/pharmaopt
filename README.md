# PharmaOpt

PharmaOpt is a pharmaceutical supply-chain analytics project focused on integrating public FDA and CMS datasets to analyze drug shortages, recalls, product information, and utilization patterns.

The project combines Python, MySQL, SQL, and Jupyter Notebook to clean, structure, validate, and analyze pharmaceutical data across multiple sources.

---

## Project Objectives

- Integrate FDA drug shortage, NDC, and recall datasets
- Build a structured relational database in MySQL
- Match NDC identifiers across multiple datasets
- Analyze shortage and recall patterns
- Evaluate manufacturer and product-level trends
- Incorporate Medicare Part D utilization data
- Develop pharmaceutical supply-risk analytics
- Build toward predictive modeling and dashboard reporting

---

## Current Results

| Metric | Result |
|---|---:|
| Drug product records | 138,217 |
| Drug package records | 256,383 |
| Shortage events | 1,601 |
| Recall events | 17,975 |
| Recall-package relationships | 25,577 |
| Shortage NDC match rate | 88.7% |
| Recall-package match rate | 76.92% |

---

## Technologies Used

- Python
- Pandas
- Jupyter Notebook
- MySQL
- SQL
- Excel
- FDA public datasets
- CMS Medicare Part D data

---

## Repository Structure

```text
pharmaopt/
│
├── notebooks/
│   ├── 01_fda_shortage_audit.ipynb
│   ├── 02_fda_ndc_audit.ipynb
│   ├── 03_fda_recall_audit.ipynb
│   ├── 04_fda_data_integration.ipynb
│   ├── 05_mysql_data_load.ipynb
│   ├── 06_pharmaopt_analytics.ipynb
│   └── 07_cms_partd_utilization.ipynb
│
├── sql/
│   ├── pharmaopt_schema.sql
│   ├── pharmaopt_analysis_queries.sql
│   ├── pharmaopt_data_validation.sql
│   └── pharmaopt_business_analysis.sql
│
└── README.md
