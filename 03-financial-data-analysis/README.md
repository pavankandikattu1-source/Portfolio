# Financial Data Analysis – Stock Volatility & Portfolio Performance

**Business Problem:** Analyze stock volatility across sectors. Which stocks show high volatility risk? What is optimal portfolio allocation?

**Target Role:** ING COO Risk — *Secondary recommendation for Air Traffic Control Consultant*

**Data:** Live data via **yfinance** (S&P 500 constituents). No manual download.

**Stack:** Python (Pandas, NumPy, yfinance) • SQL • Power BI

---

## Executive Summary

Risk-return analysis of major stocks: **volatility** (rolling 20-day annualized), **correlation matrix**, **risk-return scatter**. Demonstrates financial risk metrics, portfolio thinking, and data-driven recommendations. Relevant to credit risk as portfolio phenomenon and enterprise risk.

---

## How to Run

```bash
cd 03-financial-data-analysis
pip install -r requirements.txt
python scripts/run_analysis.py
```

---

## Deliverables

| Deliverable | Location |
|-------------|----------|
| Data fetch | yfinance (AAPL, MSFT, GOOGL, etc.) |
| Volatility | Rolling 20-day annualized % |
| Risk-return | Scatter plot, correlation heatmap |
| Outputs | `visualizations/`, `data/processed/` |
