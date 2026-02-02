"""
Financial Data Analysis – Stock Volatility & Portfolio Performance.
Uses yfinance to fetch real S&P 500 stock data (no manual download).
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIZ = os.path.join(BASE, 'visualizations')
DATA = os.path.join(BASE, 'data', 'processed')
os.makedirs(VIZ, exist_ok=True)
os.makedirs(DATA, exist_ok=True)

# Sample of S&P 500 tickers for faster run
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'JPM', 'V', 'JNJ', 'WMT', 'PG', 'UNH', 'HD', 'DIS', 'BAC', 'XOM', 'NVDA']

def fetch_data():
    try:
        import yfinance as yf
    except ImportError:
        print("Installing yfinance...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'yfinance'])
        import yfinance as yf

    print("Fetching stock data (last 2 years)...")
    df = yf.download(TICKERS, start='2022-01-01', end='2024-12-31', progress=False, auto_adjust=True, threads=False, group_by='ticker')
    if isinstance(df.columns, pd.MultiIndex):
        df = df.xs('Close', axis=1, level=1)
    df = df.dropna(how='all', axis=1).dropna(how='all')
    return df

def compute_returns_volatility(df):
    returns = df.pct_change().dropna()
    vol_20d = returns.rolling(20).std() * np.sqrt(252) * 100  # Annualized %
    mean_ret = returns.mean() * 252 * 100
    mean_vol = vol_20d.mean()
    return returns, vol_20d, mean_ret, mean_vol

def main():
    df = fetch_data()
    if df.empty or len(df) < 50:
        print("Insufficient data. Using fallback synthetic data.")
        dates = pd.date_range('2022-01-01', periods=500, freq='B')
        df = pd.DataFrame(np.random.randn(500, len(TICKERS)).cumsum(axis=0) * 0.01 + 100,
                          index=dates, columns=TICKERS)

    returns, vol_20d, mean_ret, mean_vol = compute_returns_volatility(df)

    # Risk-return scatter
    risk_return = pd.DataFrame({'Return (%)': mean_ret, 'Volatility (%)': mean_vol})

    fig, ax = plt.subplots(figsize=(10, 6))
    for ticker in risk_return.index:
        ax.scatter(risk_return.loc[ticker, 'Volatility (%)'], risk_return.loc[ticker, 'Return (%)'], s=100, label=ticker)
    ax.set_xlabel('Volatility (Annualized %)')
    ax.set_ylabel('Return (Annualized %)')
    ax.set_title('Risk-Return Profile by Stock')
    ax.legend(bbox_to_anchor=(1.02, 1))
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'risk_return_scatter.png'), dpi=100)
    plt.close()

    # Correlation heatmap
    corr = returns.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0)
    plt.title('Stock Return Correlation Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'correlation_heatmap.png'), dpi=100)
    plt.close()

    # Volatility over time (sample)
    vol_20d.iloc[-252:].plot(figsize=(10, 4))
    plt.title('Rolling 20-Day Annualized Volatility (%)')
    plt.ylabel('Volatility %')
    plt.legend(bbox_to_anchor=(1.02, 1))
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'volatility_trend.png'), dpi=100)
    plt.close()

    # Save processed data
    risk_return.to_csv(os.path.join(DATA, 'risk_return.csv'))
    returns.to_csv(os.path.join(DATA, 'returns.csv'))
    print("Done. Outputs:", VIZ, DATA)

if __name__ == '__main__':
    main()
