"""
Generate sample sales time-series data for portfolio demo.
Replace with Superstore or real data: https://www.kaggle.com/datasets/vivek468/superstore-dataset-final
"""
import pandas as pd
import numpy as np

np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=48, freq='MS')  # 4 years monthly

# Trend + seasonality
trend = np.linspace(100, 180, 48)
seasonality = 20 * np.sin(2 * np.pi * np.arange(48) / 12)  # Annual cycle
noise = np.random.normal(0, 5, 48)
sales = np.clip(trend + seasonality + noise, 50, 250)

df = pd.DataFrame({'date': dates, 'sales': sales.astype(int), 'region': 'National'})
df.to_csv('../data/raw/sales_monthly.csv', index=False)
print(f"Generated {len(df)} months. Mean sales: {df['sales'].mean():.0f}")
