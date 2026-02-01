# Customer Churn Prediction – Analysis Report

## 1. Executive Summary

[After running notebooks and model: summarize key findings in 2–3 paragraphs.]

- Overall churn rate and main drivers
- Top predictive features
- Model performance (e.g. AUC, precision/recall)
- Revenue impact (LTV × churn probability)

## 2. Methodology

- **Data source:** [Kaggle – Churn for Bank Customers](https://www.kaggle.com/datasets/mathchi/churn-for-bank-customers) (access date: YYYY-MM-DD)
- **Tools:** Python (Pandas, Scikit-learn), SQL, Power BI
- **Steps:** EDA → cleaning → feature engineering → Logistic Regression & Random Forest → evaluation

## 3. Key Metrics & KPIs

| Metric | Definition |
|--------|------------|
| Churn rate | % of customers who exited in observation period |
| LTV | Estimated lifetime value (adapt to data availability) |
| Risk score | Model probability of churn (0–1) |

## 4. Findings

[Populate after analysis.]

- Churn by geography, age, product, tenure
- Feature importance from Random Forest
- Confusion matrix and threshold choice

## 5. Limitations

- [ ] Data period and representativeness
- [ ] Imbalanced class (churn vs non-churn)
- [ ] Assumptions on LTV if not in dataset

## 6. References

- Dataset: https://www.kaggle.com/datasets/mathchi/churn-for-bank-customers
