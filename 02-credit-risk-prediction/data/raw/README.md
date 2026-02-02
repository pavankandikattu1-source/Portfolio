# Data Sources

## Home Credit Default Risk (Primary)

**Dataset:** [Kaggle - Home Credit Default Risk](https://www.kaggle.com/c/home-credit-default-risk/data)

**Default path:** `/Users/pavansatvik/Downloads/home-credit-default-risk`

**Override:** Set environment variable `HOME_CREDIT_PATH` to your data folder:
```bash
export HOME_CREDIT_PATH="/path/to/your/home-credit-default-risk"
```

**Required files:**
- `application_train.csv` (main table, target)
- `bureau.csv` (credit bureau aggregates)
- `previous_application.csv` (previous app aggregates)

**Relationships:**
- `application_train.SK_ID_CURR` → `bureau.SK_ID_CURR`, `previous_application.SK_ID_CURR`  
- Bureau aggregates: count of credits, total debt, overdue amounts  
- Previous app aggregates: count of applications, approval rate  

---

## Fallback: Synthetic Data

If Home Credit is not found, run `generate_sample_data.py` to create sample data.
