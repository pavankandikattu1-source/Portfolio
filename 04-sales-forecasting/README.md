# Sales Performance & Time-Series Forecasting

**Business Problem:** A retail superstore wants to forecast Q1–Q4 sales by region and product category. What are seasonal patterns and growth trends?

**Target Role:** ING COO Risk — *Planning, strategic topics, coordination*

**Dataset:** Sample monthly sales (`scripts/generate_sample_data.py`). Replace with [Superstore](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) for production.

**Stack:** Python (Pandas, Scikit-learn) • SQL • Power BI

---

## Executive Summary

Time-series analysis: **seasonal decomposition**, **trend**, **12-month forecast** with linear extrapolation. Demonstrates planning capability, forecasting, and uncertainty communication. Aligns with "building a planning" and strategic topics in COO Risk.

---

## How to Run

```bash
cd 04-sales-forecasting
pip install -r requirements.txt
python scripts/run_analysis.py
```

---

## Deliverables

| Deliverable | Location |
|-------------|----------|
| Data generation | `scripts/generate_sample_data.py` |
| Forecast | 12-month linear trend extrapolation |
| Visualizations | `visualizations/sales_forecast.png` |
