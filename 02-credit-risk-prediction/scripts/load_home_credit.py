"""
Load and prepare Home Credit Default Risk dataset.
Combines application_train with bureau and previous_application aggregates.
"""
import os
import pandas as pd
import numpy as np

# Path resolution: 1) HOME_CREDIT_PATH env, 2) data/raw/home-credit/, 3) default
def get_data_path():
    if os.environ.get("HOME_CREDIT_PATH"):
        return os.environ["HOME_CREDIT_PATH"]
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    local = os.path.join(base, "data", "raw", "home-credit")
    if os.path.exists(os.path.join(local, "application_train.csv")):
        return local
    return "/Users/pavansatvik/Downloads/home-credit-default-risk"

def load_application(path):
    """Load main application table."""
    fp = os.path.join(path, "application_train.csv")
    if not os.path.exists(fp):
        return None
    df = pd.read_csv(fp)
    # Convert DAYS_BIRTH to age (negative days from application)
    df["AGE"] = (-df["DAYS_BIRTH"] / 365.25).astype(int)
    # DAYS_EMPLOYED: 365243 is a placeholder for unemployed
    df["DAYS_EMPLOYED"] = df["DAYS_EMPLOYED"].replace(365243, np.nan)
    df["YEARS_EMPLOYED"] = (-df["DAYS_EMPLOYED"] / 365.25).clip(0, 50)
    return df

def aggregate_bureau(path):
    """Aggregate bureau by SK_ID_CURR."""
    fp = os.path.join(path, "bureau.csv")
    if not os.path.exists(fp):
        return None
    bureau = pd.read_csv(fp)
    agg = bureau.groupby("SK_ID_CURR").agg(
        BUREAU_CNT_CREDITS=("SK_ID_BUREAU", "count"),
        BUREAU_AMT_CREDIT_SUM=("AMT_CREDIT_SUM", "sum"),
        BUREAU_AMT_CREDIT_SUM_DEBT=("AMT_CREDIT_SUM_DEBT", "sum"),
        BUREAU_AMT_CREDIT_SUM_OVERDUE=("AMT_CREDIT_SUM_OVERDUE", "sum"),
        BUREAU_CNT_CREDIT_PROLONG=("CNT_CREDIT_PROLONG", "sum"),
    ).reset_index()
    agg.columns = ["SK_ID_CURR", "BUREAU_CNT_CREDITS", "BUREAU_AMT_CREDIT_SUM",
                   "BUREAU_AMT_CREDIT_SUM_DEBT", "BUREAU_AMT_CREDIT_SUM_OVERDUE", "BUREAU_CNT_CREDIT_PROLONG"]
    return agg

def aggregate_previous_app(path):
    """Aggregate previous applications by SK_ID_CURR."""
    fp = os.path.join(path, "previous_application.csv")
    if not os.path.exists(fp):
        return None
    prev = pd.read_csv(fp)
    prev["APPROVED"] = (prev["NAME_CONTRACT_STATUS"] == "Approved").astype(int)
    agg = prev.groupby("SK_ID_CURR").agg(
        PREV_CNT_APPLICATIONS=("SK_ID_PREV", "count"),
        PREV_CNT_APPROVED=("APPROVED", "sum"),
        PREV_AMT_CREDIT_MEAN=("AMT_CREDIT", "mean"),
    ).reset_index()
    agg["PREV_APPROVAL_RATE"] = agg["PREV_CNT_APPROVED"] / agg["PREV_CNT_APPLICATIONS"].replace(0, np.nan)
    return agg

def aggregate_bureau_balance(path):
    """Aggregate bureau_balance (DPD status) via bureau -> SK_ID_CURR. Chunked for memory."""
    fp_bb = os.path.join(path, "bureau_balance.csv")
    fp_b = os.path.join(path, "bureau.csv")
    if not os.path.exists(fp_bb) or not os.path.exists(fp_b):
        return None
    bureau = pd.read_csv(fp_b, usecols=["SK_ID_CURR", "SK_ID_BUREAU"])
    # First aggregate by SK_ID_BUREAU (reduces 27M -> ~1.7M)
    bb_agg = []
    for chunk in pd.read_csv(fp_bb, chunksize=2_000_000, usecols=["SK_ID_BUREAU", "STATUS"]):
        chunk["STATUS_NUM"] = chunk["STATUS"].map({"C": -1, "X": -1, "0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5}).fillna(-1)
        g = chunk.groupby("SK_ID_BUREAU").agg(MAX_DPD=("STATUS_NUM", "max"), CNT_DPD=("STATUS_NUM", lambda x: (x > 0).sum()))
        bb_agg.append(g)
    bb_by_bureau = pd.concat(bb_agg).groupby(level=0).agg(MAX_DPD=("MAX_DPD", "max"), CNT_DPD=("CNT_DPD", "sum")).reset_index()
    bb_by_bureau = bb_by_bureau.merge(bureau, on="SK_ID_BUREAU", how="left")
    agg = bb_by_bureau.groupby("SK_ID_CURR").agg(BUREAU_BAL_MAX_DPD=("MAX_DPD", "max"), BUREAU_BAL_CNT_DPD=("CNT_DPD", "sum")).reset_index()
    return agg

def aggregate_installments(path):
    """Aggregate installments_payments by SK_ID_CURR. Chunked for memory."""
    fp = os.path.join(path, "installments_payments.csv")
    if not os.path.exists(fp):
        return None
    chunks_agg = []
    for chunk in pd.read_csv(fp, chunksize=1_000_000, usecols=["SK_ID_CURR", "AMT_INSTALMENT", "AMT_PAYMENT", "DAYS_INSTALMENT", "DAYS_ENTRY_PAYMENT"]):
        chunk["LATE"] = (chunk["DAYS_ENTRY_PAYMENT"] > chunk["DAYS_INSTALMENT"]).astype(int)
        g = chunk.groupby("SK_ID_CURR").agg(
            LATE=("LATE", "sum"), CNT=("LATE", "count"),
            AMT_PAY=("AMT_PAYMENT", "sum"), AMT_INST=("AMT_INSTALMENT", "sum")
        )
        chunks_agg.append(g)
    if not chunks_agg:
        return None
    combined = pd.concat(chunks_agg)
    agg = combined.groupby(level=0).agg(LATE=("LATE", "sum"), CNT=("CNT", "sum"), AMT_PAY=("AMT_PAY", "sum"), AMT_INST=("AMT_INST", "sum")).reset_index()
    agg.columns = ["SK_ID_CURR", "INST_CNT_LATE", "INST_CNT_TOTAL", "AMT_PAY", "AMT_INST"]
    agg["INST_LATE_RATE"] = agg["INST_CNT_LATE"] / agg["INST_CNT_TOTAL"].replace(0, np.nan)
    agg["INST_PAYMENT_RATIO_MEAN"] = agg["AMT_PAY"] / agg["AMT_INST"].replace(0, np.nan)
    return agg[["SK_ID_CURR", "INST_CNT_LATE", "INST_CNT_TOTAL", "INST_LATE_RATE", "INST_PAYMENT_RATIO_MEAN"]]

def aggregate_credit_card(path):
    """Aggregate credit_card_balance by SK_ID_CURR."""
    fp = os.path.join(path, "credit_card_balance.csv")
    if not os.path.exists(fp):
        return None
    cc = pd.read_csv(fp, usecols=["SK_ID_CURR", "AMT_BALANCE", "AMT_CREDIT_LIMIT_ACTUAL", "SK_DPD_DEF"])
    agg = cc.groupby("SK_ID_CURR").agg(
        CC_AMT_BALANCE_MEAN=("AMT_BALANCE", "mean"),
        CC_AMT_LIMIT_MEAN=("AMT_CREDIT_LIMIT_ACTUAL", "mean"),
        CC_MAX_DPD_DEF=("SK_DPD_DEF", "max"),
    ).reset_index()
    return agg

def aggregate_pos_cash(path):
    """Aggregate POS_CASH_balance by SK_ID_CURR."""
    fp = os.path.join(path, "POS_CASH_balance.csv")
    if not os.path.exists(fp):
        return None
    pos = pd.read_csv(fp, usecols=["SK_ID_CURR", "SK_DPD", "SK_DPD_DEF"])
    agg = pos.groupby("SK_ID_CURR").agg(
        POS_DPD_MEAN=("SK_DPD", "mean"),
        POS_DPD_DEF_MAX=("SK_DPD_DEF", "max"),
    ).reset_index()
    return agg

def build_features(app, bureau_agg, prev_agg, bureau_bal_agg=None, inst_agg=None, cc_agg=None, pos_agg=None):
    """Merge and select features."""
    df = app.copy()
    if bureau_agg is not None:
        df = df.merge(bureau_agg, on="SK_ID_CURR", how="left")
        df[bureau_agg.columns[1:]] = df[bureau_agg.columns[1:]].fillna(0)
    if prev_agg is not None:
        df = df.merge(prev_agg, on="SK_ID_CURR", how="left")
        df["PREV_CNT_APPLICATIONS"] = df["PREV_CNT_APPLICATIONS"].fillna(0)
        df["PREV_CNT_APPROVED"] = df["PREV_CNT_APPROVED"].fillna(0)
        df["PREV_APPROVAL_RATE"] = df["PREV_APPROVAL_RATE"].fillna(0)
        df["PREV_AMT_CREDIT_MEAN"] = df["PREV_AMT_CREDIT_MEAN"].fillna(0)
    if bureau_bal_agg is not None:
        df = df.merge(bureau_bal_agg, on="SK_ID_CURR", how="left")
        df[bureau_bal_agg.columns[1:]] = df[bureau_bal_agg.columns[1:]].fillna(0)
    if inst_agg is not None:
        df = df.merge(inst_agg, on="SK_ID_CURR", how="left")
        for c in ["INST_CNT_LATE", "INST_CNT_TOTAL", "INST_LATE_RATE", "INST_PAYMENT_RATIO_MEAN"]:
            if c in df.columns:
                df[c] = df[c].fillna(0)
    if cc_agg is not None:
        df = df.merge(cc_agg, on="SK_ID_CURR", how="left")
        df[cc_agg.columns[1:]] = df[cc_agg.columns[1:]].fillna(0)
    if pos_agg is not None:
        df = df.merge(pos_agg, on="SK_ID_CURR", how="left")
        df[pos_agg.columns[1:]] = df[pos_agg.columns[1:]].fillna(0)

    # Select numeric/categorical features for modeling
    feature_cols = [
        "AGE", "AMT_INCOME_TOTAL", "AMT_CREDIT", "AMT_ANNUITY", "AMT_GOODS_PRICE",
        "CNT_CHILDREN", "CNT_FAM_MEMBERS", "YEARS_EMPLOYED",
        "EXT_SOURCE_1", "EXT_SOURCE_2", "EXT_SOURCE_3",
        "REGION_POPULATION_RELATIVE", "REGION_RATING_CLIENT",
        "AMT_REQ_CREDIT_BUREAU_YEAR", "DAYS_LAST_PHONE_CHANGE",
        "OBS_30_CNT_SOCIAL_CIRCLE", "DEF_30_CNT_SOCIAL_CIRCLE",
        "OBS_60_CNT_SOCIAL_CIRCLE", "DEF_60_CNT_SOCIAL_CIRCLE",
    ]
    if bureau_agg is not None:
        feature_cols += ["BUREAU_CNT_CREDITS", "BUREAU_AMT_CREDIT_SUM", "BUREAU_AMT_CREDIT_SUM_DEBT",
                        "BUREAU_AMT_CREDIT_SUM_OVERDUE", "BUREAU_CNT_CREDIT_PROLONG"]
    if prev_agg is not None:
        feature_cols += ["PREV_CNT_APPLICATIONS", "PREV_APPROVAL_RATE", "PREV_AMT_CREDIT_MEAN"]
    if bureau_bal_agg is not None:
        feature_cols += ["BUREAU_BAL_MAX_DPD", "BUREAU_BAL_CNT_DPD"]
    if inst_agg is not None:
        feature_cols += ["INST_CNT_LATE", "INST_LATE_RATE", "INST_PAYMENT_RATIO_MEAN"]
    if cc_agg is not None:
        feature_cols += ["CC_AMT_BALANCE_MEAN", "CC_AMT_LIMIT_MEAN", "CC_MAX_DPD_DEF"]
    if pos_agg is not None:
        feature_cols += ["POS_DPD_MEAN", "POS_DPD_DEF_MAX"]

    available = [c for c in feature_cols if c in df.columns]
    X = df[available].copy()
    # Fill NaN with median for numeric
    for c in X.select_dtypes(include=[np.number]).columns:
        X[c] = X[c].fillna(X[c].median())
    return df, X, available

def load_home_credit(path=None):
    """Full pipeline: load and prepare Home Credit data."""
    path = path or get_data_path()
    if not os.path.exists(path):
        return None, None, None

    app = load_application(path)
    if app is None:
        return None, None, None

    bureau_agg = aggregate_bureau(path)
    prev_agg = aggregate_previous_app(path)
    bureau_bal_agg = aggregate_bureau_balance(path)
    inst_agg = aggregate_installments(path)
    cc_agg = aggregate_credit_card(path)
    pos_agg = aggregate_pos_cash(path)
    df, X, feature_cols = build_features(app, bureau_agg, prev_agg, bureau_bal_agg, inst_agg, cc_agg, pos_agg)
    y = app["TARGET"]
    return X, y, feature_cols

if __name__ == "__main__":
    path = get_data_path()
    print("Data path:", path)
    X, y, cols = load_home_credit(path)
    if X is not None:
        print("Shape:", X.shape, "| Default rate:", f"{y.mean():.2%}")
        print("Features:", cols)
    else:
        print("Home Credit data not found at", path)
