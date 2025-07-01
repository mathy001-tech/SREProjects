# Linux Resource Monitoring Service

## Overview
This project is a lightweight Linux resource monitoring service implemented in Python. It periodically collects CPU, memory, and disk usage metrics, sends them to a cloud ingestion endpoint, visualizes data on a dashboard, and triggers alerts when thresholds are exceeded.

## Project Structure

LinuxResourceMonitor_Assignment/
├── linux_resource_monitor/         
│   ├── collector/                  # Metrics collection & alerting logic
│   │   ├── alerts.py               
│   │   └── metrics.py              
│   ├── ingestion_server/           # FastAPI server for metrics ingestion
│   │   └── server.py               
│   ├── dashboard/                  # Dash-based dashboard app
│   │   └── app.py                  
│   ├── config.yaml                 # Configuration file
│   └── main.py                     # Main entry point
├── tests/                          # Unit tests
│   ├── test_alerts.py              
│   ├── test_ingestion_server.py    
│   └── test_metrics.py             
├── requirements.txt                # Python dependencies
├── linux-resource-monitor.service  # Systemd service file for deployment
├── README.md                       


## Features
✔ Periodic system metrics collection using psutil
✔ FastAPI-based ingestion server for cloud/remote ingestion
✔ Dash-based interactive web dashboard
✔ Slack alerting for resource threshold breaches
✔ Configurable thresholds and webhook URLs via config.yaml
✔ Systemd service for background operation (or LaunchAgent for macOS)
✔ Structured JSON logging for monitoring and debugging
✔ Unit test coverage with pytest

## Setup & Installation

### 1. Clone the repo
```bash
git clone https://github.com/your_repo/linux_resource_monitor.git
cd linux_resource_monitor

## 2. Create and Activate Virual Environment
python3 -m venv venv
source venv/bin/activate

## 3. Install Dependencies
pip install -r requirements.txt

## 4. Configuration
Edit the config.yaml file to:
Set CPU, memory, and disk usage thresholds
Provide Slack webhook URL for alerts
Set server host/port details

## ✅ Usage Instructions

## 1. Run the Monitoring Service (Standalone)

python -m linux_resource_monitor.main

## 2. Start the Ingestion Server

python -m linux_resource_monitor.ingestion_server.server

Accessible by default at: http://127.0.0.1:8000/ingest

## 3. Start the Dashboard
python -m linux_resource_monitor.dashboard.app
Dashboard available at: http://127.0.0.1:8050

##4. Deploy as a Systemd Service (Linux)

# Copy the provided linux-resource-monitor.service to:

sudo cp linux-resource-monitor.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable linux-resource-monitor
sudo systemctl start linux-resource-monitor

## Check service status:

sudo systemctl status linux-resource-monitor

## ✅ Testing
## Run unit tests with:

pytest

## ✅ Cloud Ingestion Endpoint (Validation)

The FastAPI server exposes a /ingest endpoint. You can test it manually with:

curl -X POST http://127.0.0.1:8000/ingest -H "Content-Type: application/json" -d '{"cpu": 50, "memory": 40, "disk": 30}'

## A valid response:
 
 {"status": "success"}

 ## ✅ Dashboard & Alerts
Dash dashboard runs at http://127.0.0.1:8050 showing real-time metrics.

Alerts sent to Slack if thresholds are exceeded.

## ✅ Assumptions & Limitations

Tested on macOS and Linux.

Requires internet access for Slack alerts.

Local dashboard intended for personal system monitoring.

Ingestion server is local by default; can be deployed to the cloud with FastAPI.

You must provide your own Slack webhook URL.

Email alerting is planned but not implemented in this version.
























## Start Metrics Collection & Ingestion Server

cd linux_resource_monitor
python -m main

## Start the Dashboard

cd linux_resource_monitor/dashboard
python app.py

Access the dashboard at: http://localhost:8050

## Ingestion Code location
The ingestion server code is located at:

linux_resource_monitor/ingestion_server/server.py

## Example Validation Commands:

# Send sample metrics to the ingestion endpoint
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"cpu": 45, "memory": 60, "disk": 70}'

##Expected Response:

{"message": "Metrics received successfully"}
