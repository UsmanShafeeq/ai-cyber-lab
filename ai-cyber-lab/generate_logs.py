import pandas as pd
import random


def generate_data(samples=1000):
    data = []

    for _ in range(samples):
        packets = random.randint(10, 2000)
        duration = random.uniform(0.1, 10.0)
        failed_logins = random.randint(0, 50)

        # SAFE RULE-based label (simulation only)
        if packets > 1500 or failed_logins > 30:
            label = 1  # attack
        else:
            label = 0  # normal

        data.append([packets, duration, failed_logins, label])

    df = pd.DataFrame(data, columns=["packets", "duration", "failed_logins", "label"])

    df.to_csv("data/network_logs.csv", index=False)
    print("Dataset generated successfully!")


generate_data()
