# Customer Churn Prediction in Financial Services

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](.)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?style=flat&logo=scikit-learn)](.)
[![SQL](https://img.shields.io/badge/SQL-Analysis-4479A1?style=flat)](.)

> Identify high-risk bank customers likely to leave. Build a predictive model to support targeted retention and revenue-at-risk quantification.

---

## 📌 Business Problem

A bank wants to reduce churn by identifying customers at risk of leaving. **What customer behavior patterns predict churn?** How can we prioritize retention campaigns and quantify revenue impact?

---

## 📊 Key Results

| Metric | Value |
|--------|-------|
| **Churn Rate** | 20.4% |
| **Model (Random Forest)** | AUC **0.85** • Accuracy **86%** |
| **Precision (churn class)** | 78% |
| **Top Predictors** | Age, EstimatedSalary, CreditScore, Balance, NumOfProducts |

### Feature Importance

![Feature Importance](visualizations/feature_importance.png)

### Confusion Matrix

![Confusion Matrix](visualizations/confusion_matrix.png)

---

## 🚀 Quick Start

```bash
cd 01-customer-churn-prediction
pip install -r requirements.txt
python scripts/run_analysis.py
```

**Data:** Place `Churn_Modelling.csv` in `data/raw/` ([Kaggle source](https://www.kaggle.com/datasets/mathchi/churn-for-bank-customers))

---

## 📁 Deliverables

| Deliverable | Location |
|-------------|----------|
| EDA & Cleaning | `notebooks/01_eda.ipynb`, `02_data_cleaning.ipynb` |
| Modeling | `notebooks/03_analysis.ipynb`, `scripts/run_analysis.py` |
| SQL Analysis | `sql/queries.sql` |
| Reports | `reports/analysis_report.md`, `business_recommendations.md` |
| Visualizations | `visualizations/` |

---

## 🛠️ Tech Stack

Python • Pandas • Scikit-learn • Matplotlib • Seaborn • SQL • Power BI

---

## 🎯 Why This Matters for ING

- **Retail banking** relevance (churn, retention)
- **Predictive analytics** and **LTV** thinking
- End-to-end workflow: data → model → business recommendations
