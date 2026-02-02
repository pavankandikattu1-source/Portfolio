# Sales Performance & Time-Series Forecasting – Analysis Report

## 1. Executive Summary

This report presents time-series analysis and forecasting for retail sales data. The objective is to identify **trends**, **seasonality**, and produce **12-month forecasts** to support planning and resource allocation.

| Key Metric | Value |
|------------|-------|
| **Data period** | 2020–2023 (monthly) |
| **Forecast horizon** | 12 months |
| **Method** | Linear trend extrapolation + 6-month moving average |
| **YoY growth (latest)** | 22.4% |
| **Primary use** | Budgeting, inventory planning, capacity planning |

The analysis supports strategic planning, capacity planning, and coordination across functions—skills relevant to COO Risk roles focused on process optimization and implementation.

---

## 2. Methodology

- **Data:** Superstore-style sales (synthetic monthly series with region).
- **Approach:** 6-month moving average for smoothing; linear regression for trend; 12-month extrapolation for forecast.
- **Validation:** YoY growth computed for trend assessment.
- **Tools:** Python (Pandas, Matplotlib, scikit-learn).

---

## 3. Key Findings

### 3.1 Trend

- Sales show **upward trend** over the observation period.
- Linear trend extrapolation captures growth for 12-month forecast.
- YoY growth of **22.4%** (latest) indicates strong momentum.

### 3.2 Seasonality

- 6-month moving average smooths short-term fluctuations.
- Seasonal patterns visible in raw series (e.g. quarterly variation).
- Seasonality supports inventory and staffing planning.

### 3.3 12-Month Forecast

- Forecast extends from last observation through next 12 months.
- Linear trend assumes historical growth continues; uncertainty increases with horizon.
- Use for planning; update quarterly with latest data.

---

## 4. Analysis Outputs

**Sales Performance & 12-Month Forecast**

![Sales Forecast](../visualizations/sales_forecast.png)

**Takeaway:** Actual sales (blue), 6-month MA (dashed), and 12-month forecast (green). Forecast provides a baseline for budgeting; combine with scenario analysis for upside/downside.

### 4.1 Forecast Values (Sample)

| Month | Forecast |
|-------|----------|
| Month 1 | ~174 |
| Month 6 | ~181 |
| Month 12 | ~190 |

*Full forecast in `data/processed/forecast_12m.csv`.*

---

## 5. Main Takeaways

| # | Takeaway |
|---|----------|
| 1 | **Upward trend** with ~22% YoY growth; plan for continued expansion. |
| 2 | **12-month forecast** provides baseline for budget and capacity; update quarterly. |
| 3 | **6-month MA** smooths noise; use for trend detection and reporting. |
| 4 | **Seasonality** visible in raw data; consider seasonal decomposition (e.g. Prophet) for finer forecasts. |
| 5 | **Uncertainty** increases with horizon; use confidence intervals or scenarios for planning. |

---

## 6. Limitations

| Limitation | Mitigation |
|------------|------------|
| Single series | Disaggregate by region/product for granular planning |
| Linear trend | Consider Prophet, ARIMA for non-linear or seasonal patterns |
| No confidence intervals | Add prediction intervals for uncertainty quantification |
| Structural breaks | Monitor for regime changes; recalibrate when needed |

**Recommended next steps:** (1) Disaggregate by region/product; (2) Add seasonal decomposition; (3) Implement Prophet or ARIMA for improved accuracy; (4) Document assumptions for stakeholder alignment.
