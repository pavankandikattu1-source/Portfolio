"""
Sales Performance & Time-Series Forecasting.
Uses sample data or load Superstore CSV for production.
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, 'data', 'raw', 'sales_monthly.csv')
VIZ = os.path.join(BASE, 'visualizations')
DATA = os.path.join(BASE, 'data', 'processed')
os.makedirs(VIZ, exist_ok=True)
os.makedirs(DATA, exist_ok=True)
os.makedirs(os.path.dirname(RAW), exist_ok=True)

def ensure_data():
    if not os.path.exists(RAW):
        import subprocess
        script_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.run(['python', os.path.join(script_dir, 'generate_sample_data.py')], cwd=script_dir, check=True)

def main():
    ensure_data()
    df = pd.read_csv(RAW)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date').sort_index()

    # Simple moving average forecast (no Prophet/ARIMA for lighter deps)
    df['ma_3'] = df['sales'].rolling(3).mean()
    df['ma_6'] = df['sales'].rolling(6).mean()

    # Naive trend extrapolation for 12-month forecast
    from sklearn.linear_model import LinearRegression
    X = np.arange(len(df)).reshape(-1, 1)
    y = df['sales'].values
    model = LinearRegression().fit(X, y)
    future_idx = np.arange(len(df), len(df) + 12).reshape(-1, 1)
    forecast = model.predict(future_idx)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df['sales'], label='Actual', marker='o', markersize=3)
    ax.plot(df.index, df['ma_6'], label='6-month MA', linestyle='--')
    future_dates = pd.date_range(df.index[-1] + pd.offsets.MonthBegin(1), periods=12, freq='MS')
    ax.plot(future_dates, forecast, label='12-month forecast', linestyle=':', color='green')
    ax.set_title('Sales Performance & 12-Month Forecast')
    ax.set_ylabel('Sales')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'sales_forecast.png'), dpi=100)
    plt.close()

    # YoY growth
    df['yoy'] = df['sales'].pct_change(12) * 100
    print("YoY growth (last):", f"{df['yoy'].dropna().iloc[-1]:.1f}%")

    # Save forecast
    pd.DataFrame({'date': future_dates, 'forecast': forecast}).to_csv(os.path.join(DATA, 'forecast_12m.csv'), index=False)
    print("Done. Outputs:", VIZ, DATA)

if __name__ == '__main__':
    main()
