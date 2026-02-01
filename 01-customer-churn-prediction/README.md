# Customer Churn Prediction in Financial Services

**Business Problem:** A bank wants to identify high-risk customers likely to leave. What customer behavior patterns predict churn?

**Dataset:** Bank Customer Churn — `data/raw/Churn_Modelling.csv` (10,000 rows)  
**Stack:** Python (Pandas, Scikit-learn) • SQL • Power BI

---

## Executive Summary

We built a **churn prediction** pipeline on 10,000 bank customers. **Churn rate is 20.4%.** A **Random Forest** model achieved **AUC 0.85** and **86% accuracy**, with top predictors: **Age**, **EstimatedSalary**, **CreditScore**, **Balance**, and **NumOfProducts**. The model supports targeted retention (e.g. high-age, single-product, Germany) and revenue-at-risk quantification. See `reports/analysis_report.md` and `reports/business_recommendations.md` for full findings.

---

## Repository Structure

```
01-customer-churn-prediction/
├── README.md
├── data/
│   ├── raw/                 # Churn_Modelling.csv
│   └── processed/           # churn_cleaned.csv (for Power BI)
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_analysis.ipynb
├── scripts/
│   └── run_analysis.py      # Full pipeline (EDA → cleaning → modeling)
├── sql/
│   ├── queries.sql
│   └── database_schema.sql
├── visualizations/
│   ├── feature_importance.png
│   ├── confusion_matrix.png
│   └── dashboard.pbix        # (add your Power BI file)
├── reports/
│   ├── analysis_report.md
│   └── business_recommendations.md
├── requirements.txt
└── .gitignore
```

---

## Deliverables

| Deliverable | Description |
|-------------|-------------|
| **Data Preprocessing** | Cleaning, EDA, feature engineering (`notebooks/`, `scripts/run_analysis.py`) |
| **SQL Analysis** | Segment customers by product, tenure, balance; churn rate by segment (`sql/queries.sql`) |
| **ML Model** | Logistic Regression & Random Forest; confusion matrix; feature importance |
| **Power BI Dashboard** | Churn risk by age/geography/product; revenue impact; retention actions (add `dashboard.pbix`) |
| **Reports** | Executive summary, methodology, business recommendations |

---

## How to Run

1. **Environment**
   ```bash
   cd 01-customer-churn-prediction
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Data**  
   Data is in `data/raw/Churn_Modelling.csv`. To use your own file, place a CSV with the same schema (RowNumber, CustomerId, Surname, CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary, Exited) and name it `Churn_Modelling.csv`.

3. **Run full analysis (script)**
   ```bash
   python scripts/run_analysis.py
   ```
   This produces `data/processed/churn_cleaned.csv`, `visualizations/feature_importance.png`, and `visualizations/confusion_matrix.png`.

4. **Notebooks**  
   Run in order: `01_eda.ipynb` → `02_data_cleaning.ipynb` → `03_analysis.ipynb` (same logic as the script).

5. **SQL**  
   Load `data/raw/Churn_Modelling.csv` into a table named `bank_churn`, then run `sql/queries.sql`.

6. **Power BI**  
   Connect to `data/processed/churn_cleaned.csv` (or raw + model scores); add a screenshot to `visualizations/key_charts.png`.

---

## Key Results

- **Churn rate:** 20.4% (2,037 of 10,000 customers).
- **Random Forest:** AUC **0.85**, precision (churn) **0.78**, recall (churn) **0.46**, accuracy **86%**.
- **Top predictors:** Age (24%), EstimatedSalary (15%), CreditScore (14%), Balance (14%), NumOfProducts (13%).
- **Recommendations:** Target retention on high-age, single-product, and Germany segments; use model scores for campaign prioritization and revenue-at-risk.

---

## Why This Project Matters for ING

- Direct relevance to **retail banking** (churn, retention)
- Shows **predictive analytics** and **customer lifetime value (LTV)** thinking
- Covers **stakeholder communication** via SQL, notebooks, and Power BI

---

## Skills Demonstrated

Classification modeling • Customer segmentation • Business impact quantification • Predictive analytics • Python • SQL • Power BI
