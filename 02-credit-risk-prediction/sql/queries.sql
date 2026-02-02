-- Credit Risk & Loan Default - SQL Analysis
-- Table: credit_risk (credit_score, annual_income, loan_amount, employment_years, debt_to_income, num_open_accounts, delinquencies_2y, has_mortgage, default)

-- Default rate by credit score band
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

-- Default rate by debt-to-income band
SELECT
    CASE
        WHEN debt_to_income < 20 THEN 'Low (<20%)'
        WHEN debt_to_income < 40 THEN 'Medium (20-40%)'
        ELSE 'High (40%+)'
    END AS dti_band,
    COUNT(*) AS total,
    SUM(default) AS defaults,
    ROUND(100.0 * SUM(default) / COUNT(*), 2) AS default_rate_pct
FROM credit_risk
GROUP BY dti_band
ORDER BY MIN(debt_to_income);
