# Credit Risk – Business Recommendations

## 1. Strategic Overview

This document translates the credit risk model outputs into actionable recommendations for approval logic, capital management, and regulatory alignment. The framework supports **COO Risk** functions: translating credit exposures into risk-weighted assets (RWA) and provisions, and ensuring models align with business strategy and regulatory requirements.

---

## 2. Risk Tier Definitions & Decision Framework

| Tier | Default Probability | Approval Logic | Pricing / Conditions |
|------|---------------------|----------------|----------------------|
| **Low** | 0–20% | Auto-approve (subject to policy limits) | Standard rates; no additional conditions |
| **Medium** | 20–50% | Manual or enhanced review | Consider rate uplift (e.g. +50–100 bps); optional collateral |
| **High** | 50–80% | Decline or exception only | If approved: collateral, guarantor, or reduced limit |
| **Critical** | 80%+ | Decline | No approval |

**Implementation note:** Thresholds should be calibrated by product type, region, and portfolio segment. A single global threshold may not optimize risk-adjusted returns across all segments.

---

## 3. RWA & Provisions

### 3.1 Expected Loss (EL)

**EL = PD × LGD × EAD**

- **PD (Probability of Default):** Use model default probability by risk tier or score band.
- **LGD (Loss Given Default):** Use internal or regulatory LGD estimates by collateral type.
- **EAD (Exposure at Default):** Use drawn amount + CCF × undrawn for revolving products.

### 3.2 Risk-Weighted Assets

- Map model scores to regulatory PD bands (e.g. Basel IRB).
- Apply risk weights to compute RWA by segment.
- Use model outputs for **portfolio monitoring** and **capital planning**.

### 3.3 IFRS 9 Provisions

- **Stage 1:** 12-month expected credit loss (ECL).
- **Stage 2:** Lifetime ECL when credit risk has increased significantly.
- **Stage 3:** Lifetime ECL when credit-impaired.

Model default probabilities support **PD term structures** and **stage allocation** when combined with behavioral indicators (e.g. days past due, utilization).

---

## 4. Operational Workflow

| Step | Owner | Action |
|-----|------|--------|
| 1. Score applicants | Credit / IT | Run model on new applications; output default probability |
| 2. Assign risk tier | Credit | Map probability to Low / Medium / High / Critical |
| 3. Apply decision rules | Credit | Approve, decline, or refer per tier and policy |
| 4. Monitor portfolio | Risk / Finance | Track default rates by tier; compare to model predictions |
| 5. Recalibrate | Risk / Modelling | Quarterly/annual validation; adjust thresholds if drift detected |

---

## 5. Regulatory Alignment

| Requirement | How This Model Supports |
|-------------|-------------------------|
| **Basel IRB** | PD estimates by segment for RWA calculation |
| **IFRS 9** | PD inputs for ECL staging and provisioning |
| **Model validation** | ROC-AUC, precision-recall, back-testing framework |
| **Documentation** | Methodology, assumptions, limitations documented |
| **Post-production monitoring** | Track calibration, discrimination, and portfolio stability |

---

## 6. Stakeholder Communication

| Stakeholder | Key Message |
|-------------|-------------|
| **Credit / Underwriting** | Use risk tiers for approval logic; medium tier requires enhanced review |
| **Finance / Treasury** | Model scores feed RWA and provision estimates; align with capital planning |
| **Risk / Modelling** | Validate quarterly; monitor AUC and calibration; document changes |
| **IT / Implementation** | Integrate model into decision engine; ensure data lineage and audit trail |
| **Regulators** | Model methodology, validation results, and monitoring framework available |

---

## 7. Prioritized Next Steps

1. **Validate on holdout portfolio** – Confirm performance on unseen data; assess calibration.
2. **Integrate into credit decision engine** – Deploy scores and tiers into production workflow.
3. **Define segment-specific thresholds** – Optimize approval/decline by product and region.
4. **Establish monitoring dashboard** – Track default rates by tier, model drift, and portfolio mix.
5. **Document for regulatory review** – Prepare model card and validation report for internal and external use.
