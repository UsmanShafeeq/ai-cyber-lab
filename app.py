import streamlit as st  # Streamlit for dashboard UI
import pandas as pd  # Data manipulation
import numpy as np  # Numerical operations
import joblib  # Model loading
import random  # Random event generation
import time  # Timing for simulation
import plotly.express as px  # Visualization
from datetime import datetime  # Timestamps

# =============================
# Load pre-trained models and preprocessors
# =============================
clf = joblib.load("models/supervised_model.pkl")  # Supervised classifier
scaler = joblib.load("models/feature_scaler.pkl")  # Feature scaler
protocol_encoder = joblib.load("models/protocol_encoder.pkl")  # Protocol encoder
anomaly_detector = joblib.load(
    "models/anomaly_detector.pkl"
)  # Unsupervised anomaly detector
anomaly_scaler = joblib.load(
    "models/anomaly_scaler.pkl"
)  # Scaler for anomaly detection
anomaly_protocol_encoder = joblib.load(
    "models/anomaly_protocol_encoder.pkl"
)  # Protocol encoder for anomaly detection

# =============================
# Streamlit UI setup
# =============================
st.set_page_config(page_title="AI SOC Dashboard", layout="wide")
st.markdown(
    """
<style>
.big-font {font-size:30px !important; font-weight: bold;}
.status-green {background-color:#d4edda; color:#155724; padding:10px; border-radius:10px;}
.status-red {background-color:#f8d7da; color:#721c24; padding:10px; border-radius:10px;}
.status-yellow {background-color:#fff3cd; color:#856404; padding:10px; border-radius:10px;}
</style>
""",
    unsafe_allow_html=True,
)

# Main dashboard title
st.title("🛡️ AI Cybersecurity SOC Dashboard")
st.markdown(
    "<span class='big-font'>Real-Time Network Attack Detection & Monitoring</span>",
    unsafe_allow_html=True,
)

# =============================
# Sidebar controls for simulation
# =============================
st.sidebar.header("Simulation Controls")
num_events = st.sidebar.slider(
    "Number of Events", 20, 200, 50, 10
)  # Number of events to simulate
interval = st.sidebar.slider(
    "Interval (sec)", 0.1, 2.0, 1.0, 0.1
)  # Time interval between events
attack_ratio = st.sidebar.slider(
    "Attack Ratio", 0.01, 0.5, 0.08, 0.01
)  # Ratio of attacks in simulation

# Sidebar status indicators
st.sidebar.header("Status Indicators")
status_placeholder = st.sidebar.empty()

# =============================
# Feature columns for models
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

# =============================
# Placeholders for live graphs and alerts
# =============================
event_log = []  # Stores all events for session
attack_count = 0  # Counter for detected attacks
normal_count = 0  # Counter for normal events
alert_placeholder = st.empty()  # For alert messages
chart_placeholder = st.empty()  # For live chart
pie_placeholder = st.empty()  # For pie chart
table_placeholder = st.empty()  # For event table


# =============================
# Event simulation function
# =============================
def simulate_event():
    """
    Simulate a single network event with realistic feature values.
    Returns a dictionary representing the event.
    """
    protocol = np.random.choice(
        ["TCP", "UDP", "ICMP"], p=[0.7, 0.25, 0.05]
    )  # Protocol selection
    packet_size = np.random.normal(700, 300)  # Typical packet size
    packet_size = max(40, min(9000, int(packet_size)))  # Clamp to valid range
    connection_duration = np.random.exponential(2)  # Duration in seconds
    source_port = (
        random.choice([80, 443, 22, 21, 8080, 3306, 53, 25, 3389])
        if np.random.rand() < 0.7
        else random.randint(1024, 65535)
    )
    destination_port = (
        random.choice([80, 443, 22, 21, 8080, 3306, 53, 25, 3389])
        if np.random.rand() < 0.7
        else random.randint(1024, 65535)
    )
    failed_login_attempts = np.random.poisson(0.2)
    request_rate_per_second = np.random.normal(10, 5)
    src_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
    dst_ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "timestamp": timestamp,
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "protocol_type": protocol,
        "packet_size": packet_size,
        "connection_duration": connection_duration,
        "source_port": source_port,
        "destination_port": destination_port,
        "failed_login_attempts": failed_login_attempts,
        "request_rate_per_second": request_rate_per_second,
    }


def hybrid_predict(event):
    # Prepare DataFrame for model
    df = pd.DataFrame([event])
    df["protocol_type"] = protocol_encoder.transform(df["protocol_type"])
    X = df[feature_cols]
    X_scaled = scaler.transform(X)
    clf_pred = clf.predict(X_scaled)[0]
    clf_prob = clf.predict_proba(X_scaled)[0][1]
    # Anomaly detection
    adf = df.copy()
    # Handle unseen protocol values gracefully
    proto_vals = adf["protocol_type"].values
    safe_proto = []
    for val in proto_vals:
        if val in anomaly_protocol_encoder.classes_:
            safe_proto.append(val)
        else:
            safe_proto.append("TCP")  # Default to TCP if unseen
    adf["protocol_type"] = safe_proto
    adf["protocol_type"] = anomaly_protocol_encoder.transform(adf["protocol_type"])
    X_a = adf[feature_cols]
    X_a_scaled = anomaly_scaler.transform(X_a)
    anomaly_score = anomaly_detector.decision_function(X_a_scaled)[0]
    anomaly_pred = anomaly_detector.predict(X_a_scaled)[0]
    # IsolationForest: -1=anomaly, 1=normal
    is_attack = (clf_pred == 1) or (anomaly_pred == -1)
    return is_attack, clf_pred, clf_prob, anomaly_score


if st.button("Start Live Monitoring", type="primary"):
    event_log.clear()
    attack_count = 0
    normal_count = 0
    for i in range(num_events):
        event = simulate_event()
        is_attack, clf_pred, clf_prob, anomaly_score = hybrid_predict(event)
        event["attack_prob"] = clf_prob
        event["anomaly_score"] = anomaly_score
        event["detected"] = "Attack" if is_attack else "Normal"
        event_log.append(event)
        if is_attack:
            attack_count += 1
            alert_placeholder.markdown(
                f"<div class='status-red'><b>🚨 ATTACK DETECTED!</b> | Probability: {clf_prob:.2f} | Anomaly Score: {anomaly_score:.2f}</div>",
                unsafe_allow_html=True,
            )
            status_placeholder.markdown(
                f"<div class='status-red'>Red: Attack</div>", unsafe_allow_html=True
            )
        elif clf_prob > 0.5:
            alert_placeholder.markdown(
                f"<div class='status-yellow'><b>⚠️ Suspicious Activity</b> | Probability: {clf_prob:.2f} | Anomaly Score: {anomaly_score:.2f}</div>",
                unsafe_allow_html=True,
            )
            status_placeholder.markdown(
                f"<div class='status-yellow'>Yellow: Suspicious</div>",
                unsafe_allow_html=True,
            )
        else:
            normal_count += 1
            alert_placeholder.markdown(
                f"<div class='status-green'><b>✅ Normal Traffic</b></div>",
                unsafe_allow_html=True,
            )
            status_placeholder.markdown(
                f"<div class='status-green'>Green: Normal</div>", unsafe_allow_html=True
            )

        # Live line chart (attack trend)
        df_chart = pd.DataFrame(event_log)
        df_chart["time"] = pd.to_datetime(df_chart["timestamp"])
        chart = px.line(
            df_chart,
            x="time",
            y="attack_prob",
            color="detected",
            title="Attack Probability Over Time",
        )
        chart_placeholder.plotly_chart(chart, use_container_width=True)

        # Pie chart (attack vs normal)
        pie = px.pie(
            names=["Attack", "Normal"],
            values=[attack_count, normal_count],
            color=["Attack", "Normal"],
            color_discrete_map={"Attack": "red", "Normal": "green"},
            title="Traffic Distribution",
        )
        pie_placeholder.plotly_chart(pie, use_container_width=True)

        # Table of last 10 events (no cell coloring for compatibility)
        table_placeholder.dataframe(df_chart.tail(10), use_container_width=True)

        time.sleep(interval)

    alert_placeholder.markdown(
        f"<div class='status-green'><b>✅ Monitoring Complete</b></div>",
        unsafe_allow_html=True,
    )
    status_placeholder.markdown(
        f"<div class='status-green'>Green: Monitoring Complete</div>",
        unsafe_allow_html=True,
    )
