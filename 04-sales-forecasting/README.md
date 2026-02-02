# Sales Performance & Time-Series Forecasting

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](.)
[![Time-Series](https://img.shields.io/badge/Time--Series-Forecasting-2196F3?style=flat)](.)

> Forecast sales with trend and seasonality. Supports planning, strategic topics, and coordination. Aligns with ING COO Risk: **building a planning**, solving impediments, coordinating implementations.

---

## 📌 Business Problem

A retail superstore wants to forecast Q1–Q4 sales. **What are seasonal patterns and growth trends?** How can we support planning and resource allocation?

---

## 📊 Key Outputs

| Output | Description |
|--------|-------------|
| **12-Month Forecast** | Linear trend extrapolation with moving averages |
| **YoY Growth** | Year-over-year growth metrics |
| **Seasonality** | Trend + seasonal component in sample data |

### Sales Forecast

![Sales Forecast](visualizations/sales_forecast.png)

---

## 🚀 Quick Start

```bash
cd 04-sales-forecasting
pip install -r requirements.txt
python scripts/run_analysis.py
```

**Data:** Script auto-generates sample monthly sales. Replace with [Superstore dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final) for production.

---

## 📁 Deliverables

| Deliverable | Location |
|-------------|----------|
| Data Generation | `scripts/generate_sample_data.py` |
| Forecast | `scripts/run_analysis.py` |
| Outputs | `visualizations/sales_forecast.png`, `data/processed/forecast_12m.csv` |

---

## 🛠️ Tech Stack

Python • Pandas • NumPy • Scikit-learn • Matplotlib

---

## 🎯 Why This Matters for ING COO Risk

- **Planning:** Building a planning, forecasting
- **Strategic topics:** Growth drivers, seasonal patterns
- **Coordination:** Cross-team alignment on targets
