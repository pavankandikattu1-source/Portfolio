-- Customer Churn Prediction - SQL Analysis
-- Dataset: Bank Customer Churn (Churn_Modelling.csv)
-- Table: bank_churn (load from data/raw/Churn_Modelling.csv)
-- Purpose: Segment customers, churn rate by segment, support ML features

-- =============================================================================
-- 1. Churn rate by product type (NumOfProducts)
-- =============================================================================
SELECT
    NumOfProducts,
    COUNT(*) AS total_customers,
    SUM(Exited) AS churned,
    ROUND(100.0 * SUM(Exited) / COUNT(*), 2) AS churn_rate_pct
FROM bank_churn
GROUP BY NumOfProducts
ORDER BY NumOfProducts;

-- =============================================================================
-- 2. Churn rate by tenure band
-- =============================================================================
SELECT
    CASE
        WHEN Tenure < 2 THEN '0-1'
        WHEN Tenure < 5 THEN '2-4'
        WHEN Tenure < 8 THEN '5-7'
        ELSE '8+'
    END AS tenure_band,
    COUNT(*) AS total_customers,
    SUM(Exited) AS churned,
    ROUND(100.0 * SUM(Exited) / COUNT(*), 2) AS churn_rate_pct
FROM bank_churn
GROUP BY tenure_band
ORDER BY tenure_band;

-- =============================================================================
-- 3. Churn rate by geography
-- =============================================================================
SELECT
    Geography,
    COUNT(*) AS total_customers,
    SUM(Exited) AS churned,
    ROUND(100.0 * SUM(Exited) / COUNT(*), 2) AS churn_rate_pct
FROM bank_churn
GROUP BY Geography
ORDER BY churn_rate_pct DESC;

-- =============================================================================
-- 4. Balance segment (zero vs non-zero balance)
-- =============================================================================
SELECT
    CASE WHEN Balance = 0 THEN 'Zero' ELSE 'Non-zero' END AS balance_segment,
    COUNT(*) AS total_customers,
    SUM(Exited) AS churned,
    ROUND(100.0 * SUM(Exited) / COUNT(*), 2) AS churn_rate_pct
FROM bank_churn
GROUP BY balance_segment;

-- =============================================================================
-- 5. Customer segmentation view (for Power BI / reporting)
-- =============================================================================
-- Run after creating bank_churn table:
/*
CREATE OR REPLACE VIEW v_customer_churn_segments AS
SELECT
    CustomerId,
    CreditScore,
    Geography,
    Gender,
    Age,
    Tenure,
    Balance,
    NumOfProducts,
    HasCrCard,
    IsActiveMember,
    EstimatedSalary,
    Exited,
    CASE
        WHEN Tenure < 2 AND NumOfProducts = 1 THEN 'New_Single_Product'
        WHEN Tenure >= 5 AND NumOfProducts >= 2 THEN 'Loyal_Multi_Product'
        WHEN Balance = 0 THEN 'Zero_Balance'
        ELSE 'Standard'
    END AS segment
FROM bank_churn;
*/
