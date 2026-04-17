"""
Advanced Network Log Generator for AI Cybersecurity SOC
Generates realistic, imbalanced network traffic data for supervised and anomaly detection.
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Parameters
total_records = 10000
attack_ratio = 0.08  # 8% attacks, 92% normal


# Feature distributions
def generate_protocol():
    return np.random.choice(["TCP", "UDP", "ICMP"], p=[0.7, 0.25, 0.05])


def generate_port():
    # Common ports: 80, 443, 22, 21, 8080, 3306, 53, 25, 3389
    common_ports = [80, 443, 22, 21, 8080, 3306, 53, 25, 3389]
    if np.random.rand() < 0.7:
        return random.choice(common_ports)
    else:
        return random.randint(1024, 65535)


def generate_ip():
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


rows = []
start_time = datetime.now() - timedelta(hours=1)
for i in range(total_records):
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
    timestamp = start_time + timedelta(seconds=i * random.randint(1, 3))
    label = 1 if is_attack else 0
    rows.append(
        {
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
            "label": label,
        }
    )

df = pd.DataFrame(rows)
df.to_csv("data/network_logs_advanced.csv", index=False)
print("Generated data/network_logs_advanced.csv")
