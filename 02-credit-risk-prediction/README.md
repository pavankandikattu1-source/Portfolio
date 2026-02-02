# Credit Risk & Loan Default Prediction

**Business Problem:** A lending institution wants to predict loan defaults. Which applicant characteristics indicate high risk? How should credit scoring work?

**Target Role:** ING COO Risk | Credit Risk Modelling — *Primary recommendation for Air Traffic Control Consultant*

**Dataset:** Sample data generated for demo (`scripts/generate_sample_data.py`). Replace with [Kaggle Lending Club](https://www.kaggle.com/datasets/omermetinn/loans-data-set) or similar for production.

**Stack:** Python (Pandas, Scikit-learn) • SQL • Power BI

---

## Executive Summary

End-to-end credit risk framework: classification models (Logistic Regression, Random Forest) with **imbalanced data handling** (class_weight), **ROC-AUC** and **precision-recall** evaluation, **risk tier definitions**, and business translation to loss/capital impact. Mirrors COO Risk work: model design → implementation → validation → regulatory alignment.

---

## How to Run

```bash
cd 02-credit-risk-prediction
pip install -r requirements.txt
python scripts/run_analysis.py   # Generates data if needed, runs full pipeline
```

---

## Deliverables

| Deliverable | Location |
|-------------|----------|
| Data generation / preprocessing | `scripts/generate_sample_data.py`, `run_analysis.py` |
| SQL analysis | `sql/queries.sql` |
| ML models | Logistic Regression, Random Forest (class_weight) |
| Risk tiers | Low / Medium / High / Critical by default probability |
| Reports | `reports/analysis_report.md`, `business_recommendations.md` |

---

## Why This Project Matters for ING COO Risk

- **Core function:** Credit risk modeling, RWA, provisions
- **Process:** Model design → implementation → validation → post-production monitoring
- **Skills:** Imbalanced data, ROC-AUC, risk segmentation, regulatory considerations
- **Consultant framing:** Problem diagnosis → solution design → implementation → business translation
