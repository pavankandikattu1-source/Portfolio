"""
Credit Risk & Loan Default Prediction - Full pipeline.
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
from sklearn.metrics import (
    confusion_matrix, classification_report,
    roc_auc_score, precision_recall_curve, average_precision_score
)
RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, 'data', 'raw', 'credit_risk.csv')
PROCESSED = os.path.join(BASE, 'data', 'processed', 'credit_risk_processed.csv')
VIZ = os.path.join(BASE, 'visualizations')
os.makedirs(VIZ, exist_ok=True)
os.makedirs(os.path.join(BASE, 'data', 'processed'), exist_ok=True)

def main():
    # Generate sample data if not exists
    if not os.path.exists(RAW):
        import subprocess
        script_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.run(['python', os.path.join(script_dir, 'generate_sample_data.py')], cwd=script_dir, check=True)

    df = pd.read_csv(RAW)
    print("Shape:", df.shape, "| Default rate:", f"{df['default'].mean():.2%}")

    X = df.drop(columns=['default'])
    y = df['default']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )

    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)

    # Logistic Regression (class_weight for imbalanced data)
    lr = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, class_weight='balanced')
    lr.fit(X_train_sc, y_train)
    y_pred_lr = lr.predict(X_test_sc)
    print("\n--- Logistic Regression ---")
    print(classification_report(y_test, y_pred_lr))
    print("ROC-AUC:", round(roc_auc_score(y_test, lr.predict_proba(X_test_sc)[:, 1]), 4))

    # Random Forest (class_weight for imbalanced data)
    rf = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE, class_weight='balanced')
    rf.fit(X_train_sc, y_train)
    y_pred_rf = rf.predict(X_test_sc)
    print("\n--- Random Forest ---")
    print(classification_report(y_test, y_pred_rf))
    print("ROC-AUC:", round(roc_auc_score(y_test, rf.predict_proba(X_test_sc)[:, 1]), 4))

    # Feature importance
    imp = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    imp.plot(kind='barh', ax=ax)
    ax.set_title('Credit Risk: Feature Importance (Random Forest)')
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'feature_importance.png'), dpi=100)
    plt.close()

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred_rf)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.xlabel('Predicted'); plt.ylabel('Actual'); plt.title('Confusion Matrix (Random Forest)')
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'confusion_matrix.png'), dpi=100)
    plt.close()

    # Save processed with risk scores
    df_out = df.copy()
    df_out['default_prob'] = rf.predict_proba(scaler.transform(X))[:, 1]
    df_out['risk_tier'] = pd.cut(df_out['default_prob'], bins=[0, 0.2, 0.5, 0.8, 1], labels=['Low', 'Medium', 'High', 'Critical'])
    df_out.to_csv(PROCESSED, index=False)
    print("\nDone. Outputs:", PROCESSED, VIZ)

if __name__ == '__main__':
    main()
