-- Credit Risk & Loan Default - SQL Analysis
-- Supports both: (A) Home Credit schema, (B) Simple credit_risk table

-- =============================================================================
-- A. Home Credit Default Risk - application_train
-- =============================================================================
-- Default rate by external score band (EXT_SOURCE_2)
/*
SELECT
    CASE
        WHEN EXT_SOURCE_2 < 0.3 THEN 'Low (<0.3)'
        WHEN EXT_SOURCE_2 < 0.6 THEN 'Medium (0.3-0.6)'
        ELSE 'High (0.6+)'
    END AS score_band,
    COUNT(*) AS total,
    SUM(TARGET) AS defaults,
    ROUND(100.0 * SUM(TARGET) / COUNT(*), 2) AS default_rate_pct
FROM application_train
WHERE EXT_SOURCE_2 IS NOT NULL
GROUP BY score_band
ORDER BY MIN(EXT_SOURCE_2);
*/

-- Default rate by income band
/*
SELECT
    CASE
        WHEN AMT_INCOME_TOTAL < 100000 THEN 'Low (<100k)'
        WHEN AMT_INCOME_TOTAL < 200000 THEN 'Medium (100k-200k)'
        ELSE 'High (200k+)'
    END AS income_band,
    COUNT(*) AS total,
    SUM(TARGET) AS defaults,
    ROUND(100.0 * SUM(TARGET) / COUNT(*), 2) AS default_rate_pct
FROM application_train
GROUP BY income_band
ORDER BY MIN(AMT_INCOME_TOTAL);
*/

-- Bureau: default rate by number of prior credits
/*
SELECT
    CASE
        WHEN b.cnt_credits = 0 THEN '0'
        WHEN b.cnt_credits <= 5 THEN '1-5'
        WHEN b.cnt_credits <= 10 THEN '6-10'
        ELSE '11+'
    END AS bureau_credits_band,
    COUNT(*) AS total,
    SUM(a.TARGET) AS defaults,
    ROUND(100.0 * SUM(a.TARGET) / COUNT(*), 2) AS default_rate_pct
FROM application_train a
LEFT JOIN (
    SELECT SK_ID_CURR, COUNT(*) AS cnt_credits
    FROM bureau
    GROUP BY SK_ID_CURR
) b ON a.SK_ID_CURR = b.SK_ID_CURR
GROUP BY bureau_credits_band
ORDER BY bureau_credits_band;
*/

-- =============================================================================
-- B. Simple credit_risk table (synthetic/sample schema)
-- =============================================================================
-- Default rate by credit score band
/*
SELECT
    CASE
        WHEN credit_score < 580 THEN 'Poor (<580)'
        WHEN credit_score < 670 THEN 'Fair (580-669)'
        WHEN credit_score < 740 THEN 'Good (670-739)'
        ELSE 'Excellent (740+)'
    END AS credit_band,
    COUNT(*) AS total,
    SUM(default) AS defaults,
    ROUND(100.0 * SUM(default) / COUNT(*), 2) AS default_rate_pct
FROM credit_risk
GROUP BY credit_band
ORDER BY MIN(credit_score);
*/
