# Credit Risk & Loan Default Prediction – Analysis Report

## 1. Executive Summary

This report presents an end-to-end credit risk framework built on the **Home Credit Default Risk** dataset. The objective is to predict loan defaults and translate model outputs into actionable risk tiers for approval logic, capital provisioning, and regulatory alignment.

| Key Metric | Value |
|------------|-------|
| **Dataset size** | 307,511 loan applications |
| **Default rate** | 8.07% (24,825 defaults) |
| **Data sources** | 7 tables (application, bureau, bureau_balance, previous_application, installments, credit_card, POS_CASH) |
| **Features engineered** | 37 (application + aggregated behavioral/credit history) |
| **Best model** | Logistic Regression (ROC-AUC 0.74) / Random Forest (ROC-AUC 0.72, threshold-tuned) |
| **Primary use** | Risk tier assignment, approval logic, RWA and provision estimation |

The framework combines **application data** with **credit bureau history**, **payment behavior**, and **prior application outcomes** to produce default probabilities. Risk tiers (Low / Medium / High / Critical) support decision rules aligned with Basel/IFRS 9 expectations.

---

## 2. Business Context

A lending institution must balance growth (approving more loans) with risk (avoiding defaults that erode capital). Key questions addressed:

- **Which applicant characteristics predict default?**
- **How should approval thresholds be set to optimize risk-adjusted returns?**
- **How do model scores translate into RWA and provisions?**

This analysis supports credit decision engines, portfolio monitoring, and regulatory reporting.

---

## 3. Data & Relationships

### 3.1 Source Tables

| Table | Rows | Key | Purpose |
|-------|------|-----|---------|
| application_train | 307,511 | SK_ID_CURR | Main table; applicant attributes, TARGET (0/1) |
| bureau | 1.7M | SK_ID_CURR | Credit bureau history (external credits) |
| bureau_balance | 27M | SK_ID_BUREAU | Days past due (DPD) status per bureau credit |
| previous_application | 1.67M | SK_ID_CURR | Prior Home Credit applications |
| installments_payments | 13M | SK_ID_CURR | Payment history on prior loans |
| credit_card_balance | 3.8M | SK_ID_CURR | Credit card usage and limits |
| POS_CASH_balance | 10M | SK_ID_CURR | Point-of-sale / cash loan balances |

### 3.2 Aggregates Created

| Source | Aggregates | Business Meaning |
|--------|------------|-------------------|
| Bureau | Credit count, total debt, overdue amounts, prolongations | External credit exposure and repayment discipline |
| Bureau balance | Max DPD, count of DPD occurrences | Severity and frequency of past delinquency |
| Previous app | Application count, approval rate, mean credit amount | Prior relationship and approval history |
| Installments | Late payment count/rate, payment-to-instalment ratio | Repayment behavior on existing products |
| Credit card | Mean balance, mean limit, max DPD | Utilization and delinquency on revolving credit |
| POS/CASH | Mean DPD, max DPD default | Cash loan repayment behavior |

### 3.3 Data Quality

- **Missing values:** Handled via median imputation for numeric features; left-merge preserves applicants without bureau/installment history (filled with 0).
- **Target balance:** 8.07% default rate; SMOTE applied on training set to address class imbalance.
- **Outliers:** DAYS_EMPLOYED placeholder (365243) treated as unemployed; clipped to reasonable employment years.

---

## 4. Methodology

### 4.1 Feature Engineering

- **Application:** AGE (from DAYS_BIRTH), YEARS_EMPLOYED (from DAYS_EMPLOYED), income, credit amount, annuity, external scores (EXT_SOURCE_1/2/3), region, social circle defaults.
- **Behavioral:** All aggregates from bureau, bureau_balance, previous_application, installments, credit_card, POS_CASH.

### 4.2 Model Pipeline

1. **Train/test split:** 80/20, stratified on TARGET.
2. **Scaling:** StandardScaler on numeric features.
3. **Imbalance:** SMOTE on training set only (no leakage).
4. **Models:** Logistic Regression, Random Forest.
5. **Threshold tuning:** Optimize F1 for default class (best threshold ~0.30 for RF).

### 4.3 Evaluation Metrics

- **ROC-AUC:** Overall discriminative ability.
- **Precision / Recall / F1:** Trade-off between false positives and missed defaults.
- **Confusion matrix:** Operational view at chosen threshold.

---

## 5. Model Performance

| Model | ROC-AUC | Recall (Default) | Precision (Default) | F1 (Default) |
|-------|---------|------------------|----------------------|--------------|
| Logistic Regression | 0.74 | 0.67 | 0.16 | 0.26 |
| Random Forest (0.5) | 0.72 | 0.08 | 0.29 | 0.13 |
| Random Forest (0.30) | 0.72 | 0.46 | 0.19 | 0.27 |

**Interpretation:** Lowering the decision threshold from 0.5 to 0.30 increases recall (catches more defaults) at the cost of more false positives. For capital and provisioning, a conservative approach may favor higher recall; for approval volume, a higher threshold may be preferred.

### 5.1 Top Predictors (Random Forest)

1. **EXT_SOURCE_2, EXT_SOURCE_3** – External credit scores (strongest signals).
2. **YEARS_EMPLOYED** – Employment stability.
3. **AMT_ANNUITY** – Loan burden relative to income.
4. **AGE** – Life-stage risk.
5. **Bureau/installment features** – Past credit and payment behavior.

---

## 6. Risk Tier Framework

| Tier | Default Probability | Suggested Action |
|------|---------------------|------------------|
| **Low** | 0–20% | Standard approval, competitive pricing |
| **Medium** | 20–50% | Enhanced review, possible rate adjustment or collateral |
| **High** | 50–80% | Decline or require collateral / guarantor |
| **Critical** | 80%+ | Decline |

---

## 7. Limitations & Next Steps

| Limitation | Mitigation |
|------------|------------|
| Imbalanced class (8% default) | SMOTE and threshold tuning applied; consider cost-sensitive learning |
| No temporal validation | Implement back-testing on time-split data |
| Simple aggregates | Explore ratio features, trend features, interaction terms |
| Single threshold | Calibrate thresholds by segment (product, region) |
| No LGD/EAD | Integrate with loss given default and exposure at default for full EL |

**Recommended next steps:** (1) Validate on holdout portfolio; (2) Integrate into credit decision engine; (3) Monitor model drift and recalibrate; (4) Align risk tiers with RWA and IFRS 9 provisioning.
