# ========================
# collector/alerts.py
# ========================

import time
import requests
from influxdb_client import InfluxDBClient, Point  # <-- import influx client

# Initialize InfluxDB client here (or pass it in as a parameter)
INFLUX_URL = "http://localhost:8086"
INFLUX_TOKEN = "your-influx-token"
INFLUX_ORG = "your-org"
INFLUX_BUCKET = "AlertsMonitoring"

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = client.write_api()

last_alert_time = {}

def check_alerts(metrics, thresholds, cooldown, logger, slack_webhook=None):
    now = time.time()

    if max(metrics["cpu_percent"]) > thresholds['cpu']:
        trigger_alert("cpu", "⚠️ CPU usage exceeded", now, cooldown, logger, slack_webhook)

    if metrics['memory']['percent'] > thresholds['memory']:
        trigger_alert("memory", "⚠️ Memory usage exceeded", now, cooldown, logger, slack_webhook)

    if metrics['disk']['percent'] > thresholds['disk']:
        trigger_alert("disk", "⚠️ Disk usage exceeded", now, cooldown, logger, slack_webhook)

def trigger_alert(resource_key, message, now, cooldown, logger, slack_webhook=None):
    if resource_key not in last_alert_time or (now - last_alert_time[resource_key]) > cooldown:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
        logger.warning(f"{timestamp} ALERT: {message}")
        last_alert_time[resource_key] = now

        # Write alert event to InfluxDB
        try:
            point = (
                Point("alerts")
                .tag("resource", resource_key)
                .field("message", message)
                .time(int(now * 1e9))  # time in nanoseconds
            )
            write_api.write(bucket=INFLUX_BUCKET, record=point)
            logger.info("Alert event written to InfluxDB.")
        except Exception as e:
            logger.error(f"Failed to write alert event to InfluxDB: {e}")

        if slack_webhook:
            send_slack_alert(slack_webhook, message, logger)

def send_slack_alert(webhook_url, message, logger):
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            logger.info("Slack alert sent successfully.")
        else:
            logger.error(f"Slack alert failed with status {response.status_code}: {response.text}")
    except Exception as e:
        logger.error(f"Exception occurred while sending Slack alert: {e}")
