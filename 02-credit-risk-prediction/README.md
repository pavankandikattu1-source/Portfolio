# Credit Risk & Loan Default Prediction

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](.)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-orange?style=flat&logo=scikit-learn)](.)
[![ING COO Risk](https://img.shields.io/badge/ING_COO_Risk-Primary_Project-FF6200?style=flat)](.)

> End-to-end credit risk framework: predict loan defaults, define risk tiers, and translate model outputs into capital impact. **Primary recommendation for ING Air Traffic Control Consultant role.**

---

## 📌 Business Problem

A lending institution needs to predict which applicants will default. **Which characteristics indicate high risk?** How should credit scoring and approval logic work? How do different thresholds impact loss rates and capital requirements?

---

## 📊 Key Results (Home Credit Default Risk)

| Metric | Value |
|--------|-------|
| **Dataset** | Home Credit (307K applications) |
| **Default Rate** | 8.07% |
| **Models** | Logistic Regression, Random Forest (SMOTE + threshold tuning) |
| **Evaluation** | ROC-AUC ~0.74 (LR), ~0.72 (RF), F1-optimized threshold |
| **Features** | 37 (application + bureau + bureau_balance + previous_application + installments + credit_card + POS_CASH) |
| **Risk Tiers** | Low / Medium / High / Critical by default probability |

### Feature Importance

![Feature Importance](visualizations/feature_importance.png)

### Confusion Matrix

![Confusion Matrix](visualizations/confusion_matrix.png)

---

## 🚀 Quick Start

```bash
cd 02-credit-risk-prediction
pip install -r requirements.txt
python scripts/run_analysis.py
```

**Data:** Uses [Home Credit Default Risk](https://www.kaggle.com/c/home-credit-default-risk/data) from:
```
/Users/pavansatvik/Downloads/home-credit-default-risk
```
Override with `export HOME_CREDIT_PATH="/your/path"`. If not found, falls back to synthetic sample data.

---

## 📁 Deliverables

| Deliverable | Location |
|-------------|----------|
| Data Loader | `scripts/load_home_credit.py` (7 tables: application, bureau, bureau_balance, previous_application, installments_payments, credit_card_balance, POS_CASH_balance) |
| Full Pipeline | `scripts/run_analysis.py` |
| SQL Analysis | `sql/queries.sql` |
| Risk Tiers | Low (0–20%), Medium (20–50%), High (50–80%), Critical (80%+) |
| Reports | `reports/analysis_report.md`, `business_recommendations.md` |

---

## 🛠️ Tech Stack

Python • Pandas • Scikit-learn • Matplotlib • Seaborn • SQL

---

## 🎯 Why This Matters for ING COO Risk

- **Core function:** Credit risk modeling, RWA, provisions
- **Process:** Model design → implementation → validation → post-production monitoring
- **Skills:** Imbalanced data, ROC-AUC, risk segmentation, regulatory alignment
