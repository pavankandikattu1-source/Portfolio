# Credit Risk & Loan Default Prediction – Analysis Report

## 1. Executive Summary

End-to-end credit risk framework using **Home Credit Default Risk** (307K applications, 8.07% default rate). Classification models (Logistic Regression, Random Forest) with **SMOTE** for imbalanced data and **threshold tuning** for F1 on the default class. Features combine **application data**, **bureau**, **bureau_balance** (DPD status), **previous_application**, **installments_payments**, **credit_card_balance**, and **POS_CASH_balance** aggregates. **Risk tiers** (Low/Medium/High/Critical) support approval logic and capital provisioning. Aligns with ING COO Risk: model design → implementation → validation → regulatory alignment.

## 2. Data & Relationships

| Table | Rows | Key | Purpose |
|-------|------|-----|---------|
| application_train | 307,511 | SK_ID_CURR | Main table, TARGET (0/1) |
| bureau | 1.7M | SK_ID_CURR | Credit bureau history |
| bureau_balance | 27M | SK_ID_BUREAU | DPD status per bureau credit |
| previous_application | 1.67M | SK_ID_CURR | Prior Home Credit apps |
| installments_payments | 13M | SK_ID_CURR | Payment history |
| credit_card_balance | 3.8M | SK_ID_CURR | Credit card usage |
| POS_CASH_balance | 10M | SK_ID_CURR | Point-of-sale / cash loans |

**Aggregates created:**
- Bureau: count of credits, total debt, overdue amounts, prolongations
- Bureau balance: max DPD, count of DPD occurrences (via bureau link)
- Previous app: count of applications, approval rate, mean credit amount
- Installments: late payment count/rate, payment-to-instalment ratio
- Credit card: mean balance, mean limit, max DPD
- POS/CASH: mean DPD, max DPD default

## 3. Features (37 total)

- **Application:** AGE, AMT_INCOME_TOTAL, AMT_CREDIT, AMT_ANNUITY, EXT_SOURCE_1/2/3, etc.
- **Bureau:** BUREAU_CNT_CREDITS, BUREAU_AMT_CREDIT_SUM, BUREAU_AMT_CREDIT_SUM_DEBT, BUREAU_AMT_CREDIT_SUM_OVERDUE, BUREAU_CNT_CREDIT_PROLONG
- **Bureau balance:** BUREAU_BAL_MAX_DPD, BUREAU_BAL_CNT_DPD
- **Previous:** PREV_CNT_APPLICATIONS, PREV_APPROVAL_RATE, PREV_AMT_CREDIT_MEAN
- **Installments:** INST_CNT_LATE, INST_LATE_RATE, INST_PAYMENT_RATIO_MEAN
- **Credit card:** CC_AMT_BALANCE_MEAN, CC_AMT_LIMIT_MEAN, CC_MAX_DPD_DEF
- **POS/CASH:** POS_DPD_MEAN, POS_DPD_DEF_MAX

## 4. Model Performance

- **Logistic Regression:** ROC-AUC ~0.74, recall (default) 0.67
- **Random Forest:** ROC-AUC ~0.72; threshold tuned to 0.30 for F1 (default) ~0.27
- **Top predictors:** EXT_SOURCE_2, EXT_SOURCE_3, YEARS_EMPLOYED, AMT_ANNUITY, AGE, plus bureau/installment features

## 5. Limitations

- Imbalanced class (8% default); SMOTE and threshold tuning applied; further calibration possible
- No temporal validation; consider back-testing
- Bureau/prev aggregates are simple; more feature engineering possible
