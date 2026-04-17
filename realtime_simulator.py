import random  # Random event generation
import time  # Timing for simulation
import joblib  # Model loading
import pandas as pd  # Data manipulation

# =============================
# Load pre-trained model and preprocessors
# =============================
model = joblib.load("models/supervised_model.pkl")  # Supervised classifier
scaler = joblib.load("models/feature_scaler.pkl")  # Feature scaler
protocol_encoder = joblib.load("models/protocol_encoder.pkl")  # Protocol encoder

# =============================
# Feature columns for the model
# =============================
feature_cols = [
    "protocol_type",
    "packet_size",
    "connection_duration",
    "source_port",
    "destination_port",
    "failed_login_attempts",
    "request_rate_per_second",
]

print("Starting real-time simulation...\n")

# =============================
# Main simulation loop
# =============================
while True:
    # Simulate a network event with realistic values
    protocol = random.choice(["TCP", "UDP", "ICMP"])
    packet_size = random.randint(40, 9000)
    connection_duration = round(random.uniform(0.01, 10.0), 2)
    source_port = (
        random.choice([80, 443, 22, 21, 8080, 3306, 53, 25, 3389])
        if random.random() < 0.7
        else random.randint(1024, 65535)
    )
    destination_port = (
        random.choice([80, 443, 22, 21, 8080, 3306, 53, 25, 3389])
        if random.random() < 0.7
        else random.randint(1024, 65535)
    )
    failed_login_attempts = random.randint(0, 10)
    request_rate_per_second = round(random.uniform(0.1, 100.0), 2)

    # Create event dictionary
    event = {
        "protocol_type": protocol,
        "packet_size": packet_size,
        "connection_duration": connection_duration,
        "source_port": source_port,
        "destination_port": destination_port,
        "failed_login_attempts": failed_login_attempts,
        "request_rate_per_second": request_rate_per_second,
    }

    # Preprocess features for model
    df = pd.DataFrame([event])
    df["protocol_type"] = protocol_encoder.transform(df["protocol_type"])
    X = df[feature_cols]
    X_scaled = scaler.transform(X)
    prediction = model.predict(X_scaled)

    # Output result
    if prediction[0] == 1:
        print("🚨 ALERT: Suspicious Activity Detected!")
    else:
        print("✅ Normal Traffic")
    time.sleep(1)
