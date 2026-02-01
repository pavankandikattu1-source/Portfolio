# Customer Churn Prediction – Analysis Report

## 1. Executive Summary

We analyzed 10,000 bank customers to predict churn (Exited = 1). **Overall churn rate is 20.37%.** A Random Forest model achieved **AUC 0.85** and identified **Age**, **EstimatedSalary**, **CreditScore**, **Balance**, and **NumOfProducts** as the strongest predictors. The model correctly flags ~46% of churners (recall) with 78% precision, enabling targeted retention campaigns. Revenue impact can be quantified as at-risk LTV × churn probability for high-risk segments.

## 2. Methodology

- **Data source:** Bank Customer Churn (Kaggle-style schema); local file `Churn_Modelling.csv` (10,000 rows, 14 columns).
- **Tools:** Python (Pandas, Scikit-learn), SQL (segment analysis), Power BI (dashboard).
- **Steps:** EDA → drop non-predictive columns → one-hot encode Geography/Gender → train/test split (80/20, stratified) → StandardScaler → Logistic Regression & Random Forest → evaluation (confusion matrix, ROC-AUC, feature importance).

## 3. Key Metrics & KPIs

| Metric | Definition |
|--------|------------|
| Churn rate | % of customers who exited in the observation period (20.37%) |
| AUC | Area under ROC curve; Random Forest 0.85, Logistic Regression 0.77 |
| Precision (churn) | Of those predicted as churners, % who actually churned (RF: 78%) |
| Recall (churn) | Of actual churners, % correctly identified (RF: 46%) |

## 4. Findings

### Data quality
- **Shape:** 10,000 rows × 14 columns.
- **Missing values:** None.
- **Target:** Exited (0 = retained, 1 = churned).

### Churn by segment (from EDA)
- Churn varies by **Geography** (Germany typically higher), **Age** (older customers more likely to churn), and **NumOfProducts** (e.g. single-product customers more at risk).

### Model performance
- **Logistic Regression:** AUC 0.77; precision (churn) 0.59, recall (churn) 0.19.
- **Random Forest:** AUC **0.85**; precision (churn) **0.78**, recall (churn) **0.46**; accuracy 86%.
- **Confusion matrix (RF):** See `visualizations/confusion_matrix.png`.

### Feature importance (Random Forest, top 5)
1. **Age** (23.7%)
2. **EstimatedSalary** (14.7%)
3. **CreditScore** (14.3%)
4. **Balance** (14.2%)
5. **NumOfProducts** (13.1%)

Followed by Tenure, IsActiveMember, Geography (Germany, Spain), HasCrCard, Gender_Male.

## 5. Limitations

- **Imbalanced class:** ~20% churn; recall for churn class is moderate; threshold tuning or class weights could improve recall.
- **Temporal:** No time dimension; cross-sectional snapshot only.
- **LTV:** EstimatedSalary/balance used as proxies; true LTV not in dataset.
- **Causality:** Correlations only; no causal claims.

## 6. References

- Dataset: Bank Customer Churn (Kaggle); local copy as `data/raw/Churn_Modelling.csv`.
- Code: `notebooks/01_eda.ipynb`, `02_data_cleaning.ipynb`, `03_analysis.ipynb`; `scripts/run_analysis.py`.
