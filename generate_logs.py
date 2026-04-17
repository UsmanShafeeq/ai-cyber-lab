import pandas as pd  # Data manipulation
import random  # Random number generation

import pandas as pd  # Data manipulation
import random  # Random number generation


# =============================
# Function to generate synthetic network log data
# =============================
def generate_data(samples=1000):
    """
    Generate synthetic network log data for training/testing.
    Each row simulates a network session with features and a label.
    """
    data = []  # List to store generated samples

    for _ in range(samples):
        packets = random.randint(10, 2000)  # Number of packets in session
        duration = random.uniform(0.1, 10.0)  # Duration in seconds
        failed_logins = random.randint(0, 50)  # Failed login attempts

        # Simple rule-based labeling for attacks
        if packets > 1500 or failed_logins > 30:
            label = 1  # Attack
        else:
            label = 0  # Normal

        data.append([packets, duration, failed_logins, label])

    # Create DataFrame from generated data
    df = pd.DataFrame(data, columns=["packets", "duration", "failed_logins", "label"])

    # Save to CSV for use in model training
    df.to_csv("data/network_logs.csv", index=False)
    print("Dataset generated successfully!")


# =============================
# Main execution
# =============================
generate_data()
