# Customer Churn Prediction in Financial Services

**Business Problem:** A bank wants to identify high-risk customers likely to leave. What customer behavior patterns predict churn?

**Dataset:** [Churn for Bank Customers (Kaggle)](https://www.kaggle.com/datasets/mathchi/churn-for-bank-customers)  
**Access date:** [Add when you download]  
**Stack:** Python (Pandas, Scikit-learn) • SQL • Power BI

---

## Executive Summary

[Complete after analysis. Include: main drivers of churn, model performance, revenue impact, and top 3 recommendations.]

---

## Repository Structure

```
01-customer-churn-prediction/
├── README.md
├── data/
│   ├── raw/              # Original CSV (or link to Kaggle)
│   └── processed/        # Cleaned data
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_analysis.ipynb
├── sql/
│   ├── queries.sql
│   └── database_schema.sql
├── visualizations/
│   ├── dashboard.pbix
│   └── key_charts.png
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
| **Data Preprocessing** | Cleaning, EDA, feature engineering (`notebooks/`) |
| **SQL Analysis** | Segment customers by product, tenure, balance; churn rate by segment (`sql/queries.sql`) |
| **ML Model** | Logistic Regression & Random Forest; confusion matrix; feature importance |
| **Power BI Dashboard** | Churn risk by age/geography/product; revenue impact; retention actions by segment |
| **Reports** | Executive summary, methodology, business recommendations |

---

## How to Run

1. **Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Data**  
   Download the dataset from [Kaggle](https://www.kaggle.com/datasets/mathchi/churn-for-bank-customers) and place the CSV in `data/raw/`.

3. **Notebooks**  
   Run in order: `01_eda.ipynb` → `02_data_cleaning.ipynb` → `03_analysis.ipynb`.

4. **SQL**  
   Use `sql/queries.sql` with your database (adapt table/schema if needed).

5. **Power BI**  
   Connect to processed data or exported CSVs; publish dashboard and add a screenshot to `visualizations/key_charts.png`.

---

## Key Results

[After completion, add 2–3 bullets.]

- Churn rate by segment and top predictors
- Model metrics (e.g. AUC, precision, recall)
- Revenue impact and recommended retention actions

---

## Why This Project Matters for ING

- Direct relevance to **retail banking** (churn, retention)
- Shows **predictive analytics** and **customer lifetime value (LTV)** thinking
- Covers **stakeholder communication** via SQL, notebooks, and Power BI

---

## Skills Demonstrated

Classification modeling • Customer segmentation • Business impact quantification • Predictive analytics • Python • SQL • Power BI
