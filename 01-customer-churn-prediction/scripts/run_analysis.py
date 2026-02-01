"""
Customer Churn Prediction - Full pipeline: EDA, cleaning, modeling.
Run from project root: python scripts/run_analysis.py
"""
import os
import sys
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
    roc_auc_score, roc_curve, precision_recall_fscore_support
)

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)

# Paths (run from 01-customer-churn-prediction/)
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(BASE, 'data', 'raw', 'Churn_Modelling.csv')
PROCESSED = os.path.join(BASE, 'data', 'processed', 'churn_cleaned.csv')
VIZ = os.path.join(BASE, 'visualizations')
os.makedirs(VIZ, exist_ok=True)
os.makedirs(os.path.join(BASE, 'data', 'processed'), exist_ok=True)

def load_and_eda():
    df = pd.read_csv(RAW)
    print("Shape:", df.shape)
    print("Missing:", df.isnull().sum().sum())
    churn_rate = df['Exited'].mean() * 100
    print(f"Churn rate: {churn_rate:.2f}%")
    return df, churn_rate

def clean_and_prepare(df):
    # Drop non-predictive
    X = df.drop(columns=['RowNumber', 'CustomerId', 'Surname', 'Exited'])
    y = df['Exited']
    # One-hot encode categoricals
    X = pd.get_dummies(X, columns=['Geography', 'Gender'], drop_first=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=RANDOM_STATE
    )
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc = scaler.transform(X_test)
    # Save processed dataset for Power BI (with Exited and key cols)
    out = df.copy()
    out['Geography_France'] = (out['Geography'] == 'France').astype(int)
    out['Geography_Germany'] = (out['Geography'] == 'Germany').astype(int)
    out['Geography_Spain'] = (out['Geography'] == 'Spain').astype(int)
    out['Gender_Male'] = (out['Gender'] == 'Male').astype(int)
    out.to_csv(PROCESSED, index=False)
    return X_train, X_test, X_train_sc, X_test_sc, y_train, y_test, X.columns.tolist(), scaler

def train_and_evaluate(X_train_sc, X_test_sc, y_train, y_test, feature_names):
    # Logistic Regression
    lr = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    lr.fit(X_train_sc, y_train)
    y_pred_lr = lr.predict(X_test_sc)
    auc_lr = roc_auc_score(y_test, lr.predict_proba(X_test_sc)[:, 1])
    print("\n--- Logistic Regression ---")
    print(classification_report(y_test, y_pred_lr))
    print("AUC:", round(auc_lr, 4))

    # Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
    rf.fit(X_train_sc, y_train)  # RF doesn't need scaling but we use same split
    y_pred_rf = rf.predict(X_test_sc)
    auc_rf = roc_auc_score(y_test, rf.predict_proba(X_test_sc)[:, 1])
    print("\n--- Random Forest ---")
    print(classification_report(y_test, y_pred_rf))
    print("AUC:", round(auc_rf, 4))

    # Feature importance
    imp = pd.Series(rf.feature_importances_, index=feature_names).sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    imp.plot(kind='barh', ax=ax)
    ax.set_title('Feature Importance (Random Forest)')
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'feature_importance.png'), dpi=100)
    plt.close()

    # Confusion matrix RF
    cm = confusion_matrix(y_test, y_pred_rf)
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    ax.set_title('Confusion Matrix (Random Forest)')
    plt.tight_layout()
    plt.savefig(os.path.join(VIZ, 'confusion_matrix.png'), dpi=100)
    plt.close()

    return {
        'auc_lr': auc_lr, 'auc_rf': auc_rf,
        'classification_report_lr': classification_report(y_test, y_pred_lr),
        'classification_report_rf': classification_report(y_test, y_pred_rf),
        'feature_importance': imp,
        'confusion_matrix': cm,
    }

def main():
    print("Loading and EDA...")
    df, churn_rate = load_and_eda()
    print("Cleaning and train/test split...")
    X_train, X_test, X_train_sc, X_test_sc, y_train, y_test, feat_names, _ = clean_and_prepare(df)
    print("Training and evaluating...")
    results = train_and_evaluate(X_train_sc, X_test_sc, y_train, y_test, feat_names)
    print("\nDone. Processed data:", PROCESSED)
    print("Visualizations:", VIZ)
    return df, churn_rate, results

if __name__ == '__main__':
    main()
