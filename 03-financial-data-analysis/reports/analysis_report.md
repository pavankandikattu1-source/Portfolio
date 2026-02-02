# Financial Data Analysis – S&P 500 Volatility & Macro Correlation

## 1. Executive Summary

This report presents an end-to-end risk-return and correlation analysis of the **S&P 500** using historical data with macro indicators. The objective is to identify volatility patterns, macro relationships, and risk-return dynamics to support portfolio allocation, risk monitoring, and capital planning—aligned with COO Risk functions.

| Key Metric | Value |
|------------|-------|
| **Dataset size** | 1,681 monthly observations (post-deduplication) |
| **Date range** | 1871–2023 |
| **Data source** | filtered_data.csv (S&P 500, CPI, Long Interest Rate, PE10, Real Price, etc.) |
| **Primary metrics** | Rolling 12-month volatility, 5-year rolling return, macro correlations |
| **Primary use** | Risk regime assessment, portfolio allocation, stress testing inputs |

The analysis combines **equity returns** with **inflation**, **interest rates**, and **valuation (PE10)** to quantify risk-return trade-offs and macro sensitivities. Outputs support VaR, stress testing, and regulatory risk reporting.

---

## 2. Business Context

Financial institutions must balance return targets with risk appetite. Key questions addressed:

- **How does S&P 500 volatility evolve over time, and what drives regime shifts?**
- **How do macro factors (inflation, rates, valuation) correlate with equity returns?**
- **How can risk-return analysis inform portfolio allocation and capital planning?**

This analysis supports investment strategy, risk management, treasury, and regulatory reporting (market risk, VaR, stress tests).

---

## 3. Data & Variables

### 3.1 Source Data

| Variable | Description | Use |
|----------|-------------|-----|
| Date | Monthly observation | Time index |
| SP500 | S&P 500 nominal price | Nominal returns |
| Real Price | Inflation-adjusted S&P 500 | Real returns (primary) |
| Consumer Price Index | CPI | Inflation; CPI change vs returns |
| Long Interest Rate | Long-term interest rate | Rate sensitivity |
| PE10 | Cyclically adjusted P/E (10-year) | Valuation vs returns |
| Dividend, Earnings | Dividend and earnings | Optional analysis |

### 3.2 Derived Metrics

| Metric | Formula | Business Meaning |
|--------|---------|------------------|
| Monthly return | (Real Price_t / Real Price_{t-1}) − 1 | Real equity performance |
| Rolling 12m volatility | std(returns, 12) × √12 × 100 | Annualized risk (stress benchmark) |
| Rolling 5Y return | 60-month compounded return | Long-horizon performance |
| Rolling 5Y volatility | 60-month std × √12 × 100 | Long-horizon risk |

### 3.3 Data Quality

- **Missing values:** Duplicate dates removed (keep last); PE10 zeros treated as missing where applicable.
- **Alignment:** All series aligned on Date index for correlation analysis.
- **Fallback:** If filtered_data.csv not found, script uses yfinance (live stock data).

---

## 4. Methodology

### 4.1 Return Calculation

- **Primary:** Monthly % change in Real Price (inflation-adjusted).
- **Alternative:** SP500 for nominal returns.

### 4.2 Volatility

- **Rolling 12-month:** Annualized volatility = monthly std × √12.
- **Rolling 5-year:** 60-month window for long-horizon risk-return scatter.

### 4.3 Correlation Analysis

- **Window:** Last 30 years for macro correlation (readability, relevance).
- **Variables:** S&P 500 returns vs CPI change, Long Interest Rate, PE10.
- **Output:** Correlation matrix for diversification and stress scenario design.

### 4.4 Tools

Python (Pandas, NumPy, Matplotlib, Seaborn).

---

## 5. Key Findings

### 5.1 Risk-Return Trade-off

- S&P 500 exhibits **time-varying** risk-return profiles across rolling 5-year windows.
- **Efficient frontier** concept: optimal portfolios maximize return for a given risk level.
- Historical stress periods (e.g. 2008, 2020) show elevated volatility and negative returns in rolling windows.

### 5.2 Macro Correlation

| Factor | Typical Relationship | Implication |
|--------|----------------------|-------------|
| **Interest rates** | Negative correlation with equity returns | Rate hikes may pressure valuations |
| **CPI change** | Mixed; inflation can erode real returns | Monitor inflation regime |
| **PE10** | High PE10 may signal lower forward returns | Valuation-aware allocation |

### 5.3 Volatility Regimes

- Volatility is **time-varying**; spikes during recessions and crises.
- Rolling 12-month volatility provides a **stress benchmark** for VaR and capital.
- Long-term median volatility supports **scenario design** (e.g. 2× median stress).

### 5.4 Analysis Outputs

**Risk-Return Scatter (5-Year Rolling Windows)**

![Risk-Return Scatter](../visualizations/risk_return_scatter.png)

**Takeaway:** Each point is a 5-year window. Stress periods (e.g. 1974, 2008) show negative returns and elevated volatility. Use for calibrating expected return/risk assumptions.

**Correlation Matrix (S&P 500 vs Macro, Last 30 Years)**

![Correlation Heatmap](../visualizations/correlation_heatmap.png)

| Variable | vs S&P 500 Return | Interpretation |
|----------|-------------------|----------------|
| CPI_Change | +0.34 | Inflation and equity returns positively correlated in recent decades |
| Interest_Rate | −0.02 | Weak negative; rate sensitivity varies by regime |
| PE10 | +0.10 | Weak positive; high valuation not strongly linked to next-period return in this window |

**Volatility Trend (Rolling 12-Month, Last 50 Years)**

![Volatility Trend](../visualizations/volatility_trend.png)

**Takeaway:** Volatility spikes in 1974, 1987, 2008, 2020. Median volatility provides a stress benchmark for VaR and scenario design.

---

## 6. Main Takeaways

| # | Takeaway |
|---|----------|
| 1 | **S&P 500 volatility** is time-varying; spikes during crises (1974, 2008, 2020). |
| 2 | **CPI change** shows +0.34 correlation with returns (last 30Y); inflation regime matters. |
| 3 | **5-year rolling** risk-return scatter reveals historical trade-offs; use for scenario calibration. |
| 4 | **Volatility regime framework** (Low/Elevated/High/Stress) supports allocation and limits. |
| 5 | **Median volatility** benchmarks stress scenarios (e.g. 2× median for capital planning). |

---

## 7. Volatility Regime Framework

| Regime | Rolling 12m Volatility | Suggested Action |
|--------|------------------------|------------------|
| **Low** | Below median | Standard allocation; consider modest leverage |
| **Elevated** | Median to 1.5× median | Reduce risk; increase diversification |
| **High** | 1.5× to 2× median | Defensive positioning; reduce exposure |
| **Stress** | Above 2× median | Capital preservation; stress test triggers |

---

## 8. Limitations & Next Steps

| Limitation | Mitigation |
|------------|------------|
| Historical data; past ≠ future | Use for scenario design; combine with forward-looking views |
| Single asset (S&P 500) | Extend to multi-asset (bonds, sectors) for portfolio view |
| Simplified metrics | Add transaction costs, liquidity, regime-switching models |
| No causal claims | Correlations only; interpret with care |

**Recommended next steps:** (1) Extend to multi-asset/sector analysis; (2) Integrate volatility regime into allocation rules; (3) Feed outputs into VaR and stress testing; (4) Document for regulatory and internal risk reporting.
