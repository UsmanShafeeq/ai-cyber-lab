"""
Anomaly Detection Training Pipeline for AI Cybersecurity SOC
- Uses Isolation Forest (default) and One-Class SVM (optional)
- Saves trained anomaly detector to /models
- Designed for hybrid detection with supervised model
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.svm import OneClassSVM
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

# Load data
df = pd.read_csv("data/network_logs_advanced.csv")

# Encode categorical features
le_protocol = LabelEncoder()
df["protocol_type"] = le_protocol.fit_transform(df["protocol_type"])

# Drop columns not used for training
X = df.drop(["timestamp", "src_ip", "dst_ip", "label"], axis=1)

# Feature scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train Isolation Forest (unsupervised, fit on all data)
iso_forest = IsolationForest(n_estimators=100, contamination=0.08, random_state=42)
iso_forest.fit(X_scaled)

# Optionally, train One-Class SVM (commented out for speed)
# one_class_svm = OneClassSVM(nu=0.08, kernel='rbf', gamma='scale')
# one_class_svm.fit(X_scaled)

# Save anomaly detector and scaler
os.makedirs("models", exist_ok=True)
joblib.dump(iso_forest, "models/anomaly_detector.pkl")
joblib.dump(scaler, "models/anomaly_scaler.pkl")
joblib.dump(le_protocol, "models/anomaly_protocol_encoder.pkl")
print("Saved Isolation Forest anomaly detector and preprocessors to /models")
