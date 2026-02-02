# Financial Data Analysis – S&P 500 Volatility & Macro Correlation

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](.)
[![ING COO Risk](https://img.shields.io/badge/ING_COO_Risk-Secondary_Project-FF6200?style=flat)](.)

> Risk-return and correlation analysis of **S&P 500** with macro indicators (CPI, interest rates, PE10). Volatility trends, rolling risk-return windows, and macro relationships. **Secondary recommendation for ING Air Traffic Control Consultant role.**

---

## 📌 Business Problem

Analyze S&P 500 volatility and its relationship to macro factors. **What drives risk over time?** How do interest rates and inflation correlate with returns? How can we support portfolio allocation and risk management decisions?

---

## 📊 Key Outputs

| Output | Description |
|--------|-------------|
| **Risk-Return Scatter** | 5-year rolling return vs. volatility (S&P 500) |
| **Correlation Matrix** | S&P 500 returns vs CPI change, interest rate, PE10 |
| **Volatility Trends** | Rolling 12-month annualized volatility over time |

### Risk-Return Profile

![Risk-Return Scatter](visualizations/risk_return_scatter.png)

### Correlation Heatmap

![Correlation Heatmap](visualizations/correlation_heatmap.png)

### Volatility Over Time

![Volatility Trend](visualizations/volatility_trend.png)

---

## 🚀 Quick Start

```bash
cd 03-financial-data-analysis
pip install -r requirements.txt
python scripts/run_analysis.py
```

**Data:** Uses `data/raw/filtered_data.csv` (S&P 500 + macro indicators, 1871–2023). Override with `export FINANCIAL_DATA_PATH="/path/to/filtered_data.csv"`. Falls back to **yfinance** if not found.

---

## 📁 Deliverables

| Deliverable | Location |
|-------------|----------|
| Data | `data/raw/filtered_data.csv` (SP500, CPI, Interest Rate, PE10, etc.) |
| Analysis | `scripts/run_analysis.py` |
| Outputs | `visualizations/`, `data/processed/` |

---

## 🛠️ Tech Stack

Python • Pandas • NumPy • Matplotlib • Seaborn • (yfinance fallback)

---

## 🎯 Why This Matters for ING COO Risk

- **Risk metrics:** Volatility, correlation, risk-return
- **Portfolio thinking:** Credit risk as portfolio phenomenon
- **Quantitative rigor:** Data-driven recommendations
