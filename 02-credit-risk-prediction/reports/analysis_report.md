# Credit Risk & Loan Default Prediction – Analysis Report

## Executive Summary

End-to-end credit risk framework: classification models predict loan default from applicant characteristics. **Imbalanced data** handled via class_weight. **Risk tiers** (Low/Medium/High/Critical) support approval logic and capital provisioning. Aligns with ING COO Risk: model design → implementation → validation → regulatory alignment.

## Methodology

- **Data:** Sample credit risk dataset (credit_score, income, loan_amount, DTI, employment, etc.). Replace with Lending Club or production data.
- **Models:** Logistic Regression & Random Forest with class_weight='balanced'.
- **Evaluation:** ROC-AUC, precision-recall, confusion matrix, feature importance.

## Key Findings

- Top predictors: credit_score, debt_to_income, delinquencies_2y, loan_amount.
- Risk tiers enable approval thresholds and loss provisioning.
- Model outputs support RWA and regulatory reporting.

## Limitations

- Sample data; validate on real portfolio.
- No temporal validation; consider back-testing.
