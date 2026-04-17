# AI Cyber Lab

A professional cyber security AI lab for network anomaly detection, log generation, and real-time simulation. This repository provides tools for generating synthetic network logs, training machine learning models (both supervised and unsupervised), and simulating real-time network events for research and educational purposes.

## Features

- **Log Generation:** Generate basic and advanced synthetic network logs for training and testing.
- **Model Training:** Train anomaly detection and supervised models for cyber threat detection.
- **Real-Time Simulation:** Simulate network events and stream logs in real-time.
- **Dashboard:** Visualize network activity and model predictions.
- **API:** RESTful API for integration and automation.

## Project Structure

```
app.py                       # Main application entry point
api/                         # REST API implementation
src/                         # Source code for log generation, training, and simulation
  generate_advanced_logs.py
  realtime_simulator.py
  train_anomaly_detector.py
  train_supervised_model.py
utils/                       # Utility scripts (e.g., preprocessing)
dashboard/                   # Dashboard UI and backend
models/                      # Saved models
model.py                     # Model definitions
train_model.py               # Model training script
generate_logs.py             # Log generation script
realtime_simulator.py        # Real-time simulation script
data/                        # Data and logs
  network_logs.csv
  network_logs_500.csv
  network_logs_advanced.csv
  logs/streamed_events.csv
  model/                     # Model artifacts
```

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/ai-cyber-lab.git
   cd ai-cyber-lab
   ```
2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Unix or MacOS
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the main application:**
   ```bash
   python app.py
   ```

## Usage

- **Generate Logs:**
  ```bash
  python generate_logs.py
  ```
- **Train Model:**
  ```bash
  python train_model.py
  ```
- **Simulate Real-Time Events:**
  ```bash
  python realtime_simulator.py
  ```

## Contribution Guidelines

- Write clear, concise, and well-documented code.
- Add meaningful comments (target: 100+ comments across the codebase).
- Follow PEP8 style guide for Python code.
- Submit pull requests with detailed descriptions.

## License

This project is licensed under the MIT License.

## Contact

For questions or collaboration, please open an issue or contact the maintainer at [your-email@example.com].
