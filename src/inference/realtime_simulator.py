"""
Real-Time Network Traffic Simulator for AI Cybersecurity SOC
- Streams realistic network events with time-series behavior
- Designed for integration with dashboard and logging
"""

import time
import random
import numpy as np
from datetime import datetime, timedelta
import pandas as pd


# Feature distributions (should match training data)
def generate_protocol():
    return np.random.choice(["TCP", "UDP", "ICMP"], p=[0.7, 0.25, 0.05])


def generate_port():
    common_ports = [80, 443, 22, 21, 8080, 3306, 53, 25, 3389]
    if np.random.rand() < 0.7:
        return random.choice(common_ports)
    else:
        return random.randint(1024, 65535)


def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def simulate_event(ts, attack_ratio=0.08):
    is_attack = np.random.rand() < attack_ratio
    protocol = generate_protocol()
    packet_size = (
        np.random.normal(700, 300) if not is_attack else np.random.normal(1500, 600)
    )
    packet_size = max(40, min(9000, int(packet_size)))
    connection_duration = (
        np.random.exponential(2) if not is_attack else np.random.exponential(8)
    )
    connection_duration = round(connection_duration, 2)
    source_port = generate_port()
    destination_port = generate_port()
    failed_login_attempts = (
        np.random.poisson(0.2) if not is_attack else np.random.poisson(3)
    )
    request_rate_per_second = (
        np.random.normal(10, 5) if not is_attack else np.random.normal(50, 30)
    )
    request_rate_per_second = max(0.1, round(request_rate_per_second, 2))
    src_ip = generate_ip()
    dst_ip = generate_ip()
    label = 1 if is_attack else 0
    return {
        "timestamp": ts,
        "src_ip": src_ip,
        "dst_ip": dst_ip,
        "protocol_type": protocol,
        "packet_size": packet_size,
        "connection_duration": connection_duration,
        "source_port": source_port,
        "destination_port": destination_port,
        "failed_login_attempts": failed_login_attempts,
        "request_rate_per_second": request_rate_per_second,
        "label": label,
    }


def stream_events(num_events=100, interval=1.0, attack_ratio=0.08, log_path=None):
    """
    Streams events in real-time. Optionally logs to CSV.
    """
    ts = datetime.now()
    all_events = []
    for i in range(num_events):
        event = simulate_event(ts, attack_ratio)
        print(event)
        all_events.append(event)
        if log_path:
            df = pd.DataFrame([event])
            df.to_csv(log_path, mode="a", header=not bool(i), index=False)
        ts += timedelta(seconds=random.randint(1, 3))
        time.sleep(interval)
    return all_events


if __name__ == "__main__":
    # Example: stream 20 events, 1 per second, log to data/logs/streamed_events.csv
    stream_events(num_events=20, interval=1.0, log_path="data/logs/streamed_events.csv")
