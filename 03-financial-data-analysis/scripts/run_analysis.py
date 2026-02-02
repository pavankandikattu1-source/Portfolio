"""
Financial Data Analysis – S&P 500 Volatility & Macro Correlation.
Uses filtered_data.csv (S&P 500 + macro indicators) when available, else yfinance fallback.
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
DATA = os.path.join(BASE, 'data')
RAW = os.path.join(DATA, 'raw')
PROCESSED = os.path.join(DATA, 'processed')
os.makedirs(VIZ, exist_ok=True)
os.makedirs(PROCESSED, exist_ok=True)
os.makedirs(RAW, exist_ok=True)

# Path resolution: 1) FINANCIAL_DATA_PATH env, 2) data/raw/, 3) Downloads
def get_data_path():
    if os.environ.get("FINANCIAL_DATA_PATH"):
        return os.environ["FINANCIAL_DATA_PATH"]
    local = os.path.join(RAW, "filtered_data.csv")
    if os.path.exists(local):
        return local
    return "/Users/pavansatvik/Downloads/filtered_data.csv"

def load_filtered_data():
    """Load S&P 500 + macro data from filtered_data.csv."""
    path = get_data_path()
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date").drop_duplicates(subset=["Date"], keep="last").set_index("Date")
    return df

def fetch_yfinance_fallback():
    """Fallback: fetch S&P 500 stocks via yfinance."""
    try:
        import yfinance as yf
    except ImportError:
        import subprocess
        subprocess.check_call(['pip', 'install', 'yfinance'])
        import yfinance as yf
    TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'JPM', 'V', 'JNJ', 'WMT', 'PG']
    print("Fetching stock data (yfinance fallback)...")
    df = yf.download(TICKERS, start='2022-01-01', end='2024-12-31', progress=False, auto_adjust=True, threads=False, group_by='ticker')
    if isinstance(df.columns, pd.MultiIndex):
        df = df.xs('Close', axis=1, level=1)
    df = df.dropna(how='all', axis=1).dropna(how='all')
    return df

def run_filtered_analysis(df):
    """Analysis using S&P 500 + macro data."""
    # Use Real Price (inflation-adjusted) or SP500 for returns
    price_col = "Real Price" if "Real Price" in df.columns else "SP500"
    prices = df[price_col].dropna()

    returns = prices.pct_change().dropna()
    # Rolling 12-month volatility (annualized: monthly_std * sqrt(12))
    vol_12m = returns.rolling(12).std() * np.sqrt(12) * 100
    vol_12m = vol_12m.dropna()

    # Correlation with macro indicators (use recent 30 years for readability)
    df_recent = df.loc[df.index >= (df.index.max() - pd.DateOffset(years=30))] if len(df) > 360 else df
    ret_recent = df_recent[price_col].pct_change().dropna()

    corr_data = pd.DataFrame({"SP500_Return": ret_recent}, index=ret_recent.index)
    if "Consumer Price Index" in df_recent.columns:
        cpi_chg = df_recent["Consumer Price Index"].pct_change()
        corr_data["CPI_Change"] = cpi_chg.loc[corr_data.index]
    if "Long Interest Rate" in df_recent.columns:
        corr_data["Interest_Rate"] = df_recent["Long Interest Rate"].loc[corr_data.index]
    if "PE10" in df_recent.columns:
        pe = df_recent["PE10"].replace(0, np.nan)
        corr_data["PE10"] = pe.loc[corr_data.index]

    corr_data = corr_data.dropna(how='all').dropna()
    corr = corr_data.corr()

    # Risk-return: rolling 5-year windows
    roll_ret = returns.rolling(60).apply(lambda x: (1 + x).prod() - 1 if len(x) == 60 else np.nan)
    roll_vol = returns.rolling(60).std() * np.sqrt(12) * 100
    rr = pd.DataFrame({"Return_5Y": roll_ret, "Volatility_5Y": roll_vol}).dropna()
    rr = rr.loc[rr.index >= (rr.index.max() - pd.DateOffset(years=50))] if len(rr) > 600 else rr

    # 1. Risk-return scatter (rolling 5Y windows)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(rr["Volatility_5Y"], rr["Return_5Y"] * 100, alpha=0.6, s=20, c=rr.index.astype(np.int64), cmap='viridis')
    ax.set_xlabel('5-Year Rolling Volatility (Annualized %)')
    ax.set_ylabel('5-Year Rolling Return (%)')
    ax.set_title('S&P 500: Risk-Return by Rolling 5-Year Window')
    ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'risk_return_scatter.png'), dpi=100)
    plt.close()

    # 2. Correlation heatmap (SP500 returns vs macro)
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0, vmin=-0.5, vmax=0.5)
    plt.title('S&P 500 Returns vs Macro Indicators (30Y)')
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'correlation_heatmap.png'), dpi=100)
    plt.close()

    # 3. Volatility trend over time
    vol_plot = vol_12m.loc[vol_12m.index >= (vol_12m.index.max() - pd.DateOffset(years=50))] if len(vol_12m) > 600 else vol_12m
    fig, ax = plt.subplots(figsize=(10, 4))
    vol_plot.plot(ax=ax)
    ax.set_title('S&P 500: Rolling 12-Month Annualized Volatility (%)')
    ax.set_ylabel('Volatility %')
    ax.axhline(vol_plot.median(), color='red', linestyle='--', alpha=0.7, label=f'Median: {vol_plot.median():.1f}%')
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'volatility_trend.png'), dpi=100)
    plt.close()

    # Save processed
    rr.to_csv(os.path.join(PROCESSED, 'risk_return.csv'))
    corr.to_csv(os.path.join(PROCESSED, 'correlation_matrix.csv'))
    return "filtered_data"

def run_yfinance_analysis(df):
    """Analysis using yfinance multi-stock data."""
    returns = df.pct_change().dropna()
    vol_20d = returns.rolling(20).std() * np.sqrt(252) * 100
    mean_ret = returns.mean() * 252 * 100
    mean_vol = vol_20d.mean()
    risk_return = pd.DataFrame({'Return (%)': mean_ret, 'Volatility (%)': mean_vol})
    corr = returns.corr()

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

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm', center=0)
    plt.title('Stock Return Correlation Matrix')
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'correlation_heatmap.png'), dpi=100)
    plt.close()

    vol_20d.iloc[-252:].plot(figsize=(10, 4))
    plt.title('Rolling 20-Day Annualized Volatility (%)')
    plt.ylabel('Volatility %')
    plt.legend(bbox_to_anchor=(1.02, 1))
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'volatility_trend.png'), dpi=100)
    plt.close()

    risk_return.to_csv(os.path.join(PROCESSED, 'risk_return.csv'))
    returns.to_csv(os.path.join(PROCESSED, 'returns.csv'))
    return "yfinance"

def main():
    df = load_filtered_data()
    if df is not None and len(df) > 60:
        print("Using S&P 500 + macro data from:", get_data_path())
        print("Shape:", df.shape, "| Date range:", df.index.min(), "to", df.index.max())
        data_source = run_filtered_analysis(df)
    else:
        print("filtered_data.csv not found. Using yfinance fallback.")
        df = fetch_yfinance_fallback()
        if df.empty or len(df) < 50:
            print("Insufficient data. Using synthetic.")
            dates = pd.date_range('2022-01-01', periods=500, freq='B')
            df = pd.DataFrame(np.random.randn(500, 5).cumsum(axis=0) * 0.01 + 100, index=dates, columns=['A', 'B', 'C', 'D', 'E'])
        data_source = run_yfinance_analysis(df)

    print("Done. Data source:", data_source, "| Outputs:", VIZ, PROCESSED)

if __name__ == '__main__':
    main()
