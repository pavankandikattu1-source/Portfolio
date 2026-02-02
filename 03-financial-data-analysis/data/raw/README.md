# Financial Data – Raw Data

## Dataset: S&P 500 + Macro Indicators

**File:** `filtered_data.csv`

| Column | Description |
|--------|-------------|
| Date | Monthly observation date |
| SP500 | S&P 500 price index |
| Dividend | Dividend |
| Earnings | Earnings |
| Consumer Price Index | CPI |
| Long Interest Rate | Long-term interest rate |
| Real Price | Inflation-adjusted S&P 500 price |
| Real Dividend | Inflation-adjusted dividend |
| Real Earnings | Inflation-adjusted earnings |
| PE10 | Cyclically adjusted price-to-earnings ratio (10-year) |

**Source:** S&P 500 historical data with macro indicators (e.g. Robert Shiller data, Yahoo Finance).

**Path:** Place `filtered_data.csv` in this folder, or set:
```bash
export FINANCIAL_DATA_PATH="/path/to/filtered_data.csv"
```

If not found, the script falls back to **yfinance** (live S&P 500 stock data).
