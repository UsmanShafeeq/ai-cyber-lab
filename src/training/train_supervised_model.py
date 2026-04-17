"""
Advanced ML Model Training Pipeline for AI Cybersecurity SOC
- Uses XGBoost (if available), otherwise RandomForest
- Includes feature scaling, cross-validation, and metrics reporting
- Saves trained model to /models
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)
import joblib
import os

try:
    from xgboost import XGBClassifier

    xgb_available = True
except ImportError:
    xgb_available = False

# Load data
df = pd.read_csv("data/network_logs_advanced.csv")

# Encode categorical features
le_protocol = LabelEncoder()
df["protocol_type"] = le_protocol.fit_transform(df["protocol_type"])

# Drop columns not used for training
X = df.drop(["timestamp", "src_ip", "dst_ip", "label"], axis=1)
y = df["label"]

# Feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# Model selection
if xgb_available:
    model = XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric="logloss",
        random_state=42,
    )
else:
    model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)

# Cross-validation
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="f1")
print(f"Cross-validated F1 scores: {cv_scores}")
print(f"Mean F1: {cv_scores.mean():.4f}")

# Train
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1-score:", f1_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model and scaler
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/supervised_model.pkl")
joblib.dump(scaler, "models/feature_scaler.pkl")
joblib.dump(le_protocol, "models/protocol_encoder.pkl")
print("Saved model, scaler, and encoder to /models")
