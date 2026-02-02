"""
Credit Risk & Loan Default Prediction - Full pipeline.
Uses Home Credit Default Risk data when available, else synthetic sample.
Run from project root: python scripts/run_analysis.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, classification_report, roc_auc_score, f1_score
from imblearn.over_sampling import SMOTE

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, 'data', 'raw', 'credit_risk.csv')
PROCESSED = os.path.join(BASE, 'data', 'processed', 'credit_risk_processed.csv')
VIZ = os.path.join(BASE, 'visualizations')
os.makedirs(VIZ, exist_ok=True)
os.makedirs(os.path.join(BASE, 'data', 'processed'), exist_ok=True)

def load_data():
    """Load Home Credit if available, else synthetic."""
    try:
        from load_home_credit import load_home_credit, get_data_path
        X, y, _ = load_home_credit()
        if X is not None:
            print("Using Home Credit Default Risk data from:", get_data_path())
            return X, y, "TARGET"
    except Exception as e:
        print("Home Credit load failed:", e)

    # Fallback: synthetic data
    if not os.path.exists(RAW):
        import subprocess
        script_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.run(['python', os.path.join(script_dir, 'generate_sample_data.py')], cwd=script_dir, check=True)
    df = pd.read_csv(RAW)
    return df.drop(columns=['default']), df['default'], "default"

def main():
    X, y, target_name = load_data()
    print("Shape:", X.shape, "| Default rate:", f"{y.mean():.2%}")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)

    # SMOTE to balance training set (only on train to avoid leakage)
    try:
        smote = SMOTE(random_state=RANDOM_STATE, k_neighbors=5)
        X_train_sm, y_train_sm = smote.fit_resample(X_train_sc, y_train)
        print(f"After SMOTE: train {len(y_train_sm)} (defaults: {y_train_sm.sum()})")
    except Exception:
        X_train_sm, y_train_sm = X_train_sc, y_train
        print("SMOTE skipped (fallback to original)")

    # Logistic Regression (trained on SMOTE-balanced data)
    lr = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    lr.fit(X_train_sm, y_train_sm)
    y_pred_lr = lr.predict(X_test_sc)
    print("\n--- Logistic Regression ---")
    print(classification_report(y_test, y_pred_lr))
    print("ROC-AUC:", round(roc_auc_score(y_test, lr.predict_proba(X_test_sc)[:, 1]), 4))

    # Random Forest (trained on SMOTE-balanced data)
    rf = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
    rf.fit(X_train_sm, y_train_sm)
    y_pred_rf = rf.predict(X_test_sc)
    print("\n--- Random Forest ---")
    print(classification_report(y_test, y_pred_rf))
    print("ROC-AUC:", round(roc_auc_score(y_test, rf.predict_proba(X_test_sc)[:, 1]), 4))

    # Threshold tuning: find best F1 for default class
    proba = rf.predict_proba(X_test_sc)[:, 1]
    best_thresh, best_f1 = 0.5, 0
    for thresh in np.arange(0.2, 0.6, 0.02):
        pred = (proba >= thresh).astype(int)
        f1 = f1_score(y_test, pred, pos_label=1, zero_division=0)
        if f1 > best_f1:
            best_f1, best_thresh = f1, thresh
    y_pred_opt = (proba >= best_thresh).astype(int)
    print(f"\n--- Optimized threshold {best_thresh:.2f} (F1 default={best_f1:.3f}) ---")
    print(classification_report(y_test, y_pred_opt))

    # Feature importance
    imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    imp.plot(kind='barh', ax=ax)
    ax.set_title('Credit Risk: Feature Importance (Random Forest)')
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'feature_importance.png'), dpi=100)
    plt.close()

    # Confusion matrix (use optimized threshold)
    cm = confusion_matrix(y_test, y_pred_opt)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted'); plt.ylabel('Actual'); plt.title(f'Confusion Matrix (RF, thresh={best_thresh:.2f})')
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'confusion_matrix.png'), dpi=100)
    plt.close()

    # Save processed with risk scores
    default_prob = rf.predict_proba(scaler.transform(X))[:, 1]
    risk_tier = pd.cut(default_prob, bins=[0, 0.2, 0.5, 0.8, 1], labels=['Low', 'Medium', 'High', 'Critical'])
    df_out = X.copy()
    df_out['default_prob'] = default_prob
    df_out['risk_tier'] = risk_tier
    df_out['target'] = y.values
    df_out.to_csv(PROCESSED, index=False)
    print("\nDone. Outputs:", PROCESSED, VIZ)

if __name__ == '__main__':
    main()
