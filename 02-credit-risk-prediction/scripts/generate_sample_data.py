"""
Generate sample credit risk data for portfolio demo.
Replace with real data (e.g. Kaggle Lending Club) for production use.
"""
import pandas as pd
import numpy as np

np.random.seed(42)
n = 3000

# Realistic credit risk features
credit_score = np.clip(np.random.normal(650, 80, n).astype(int), 300, 850)
annual_income = np.clip(np.random.lognormal(10.5, 0.6, n).astype(int), 20000, 200000)
loan_amount = np.clip(np.random.lognormal(9.5, 0.7, n).astype(int), 5000, 100000)
employment_years = np.clip(np.random.exponential(5, n).astype(int), 0, 40)
debt_to_income = np.clip(np.random.beta(2, 5, n) * 60, 5, 60)
num_open_accounts = np.random.poisson(5, n)
delinquencies_2y = np.random.poisson(0.3, n)
has_mortgage = np.random.binomial(1, 0.6, n)

# Default probability (higher for low score, high DTI, etc.)
logit = -4 + 0.01 * (850 - credit_score) + 0.02 * debt_to_income - 0.00001 * annual_income
logit += 0.1 * delinquencies_2y - 0.05 * employment_years
prob = 1 / (1 + np.exp(-logit))
default = (np.random.random(n) < prob).astype(int)

df = pd.DataFrame({
    'credit_score': credit_score,
    'annual_income': annual_income,
    'loan_amount': loan_amount,
    'employment_years': employment_years,
    'debt_to_income': debt_to_income,
    'num_open_accounts': num_open_accounts,
    'delinquencies_2y': delinquencies_2y,
    'has_mortgage': has_mortgage,
    'default': default
})

df.to_csv('../data/raw/credit_risk.csv', index=False)
print(f"Generated {len(df)} rows. Default rate: {df['default'].mean():.2%}")
