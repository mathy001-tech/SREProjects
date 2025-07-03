# ========================
# collector/alerts.py
# ========================

import time
import requests
from influxdb_client import Point  # no need to import InfluxDBClient here anymore

last_alert_time = {}

def check_alerts(metrics, thresholds, cooldown, logger, slack_webhook=None, write_api=None, influx_bucket=None):
    now = time.time()

    if max(metrics["cpu_percent"]) > thresholds['cpu']:
        trigger_alert("cpu", "⚠️ CPU usage exceeded", now, cooldown, logger, slack_webhook, write_api, influx_bucket)

    if metrics['memory']['percent'] > thresholds['memory']:
        trigger_alert("memory", "⚠️ Memory usage exceeded", now, cooldown, logger, slack_webhook, write_api, influx_bucket)

    if metrics['disk']['percent'] > thresholds['disk']:
        trigger_alert("disk", "⚠️ Disk usage exceeded", now, cooldown, logger, slack_webhook, write_api, influx_bucket)

def trigger_alert(resource_key, message, now, cooldown, logger, slack_webhook=None, write_api=None, influx_bucket=None):
    if resource_key not in last_alert_time or (now - last_alert_time[resource_key]) > cooldown:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
        logger.warning(f"{timestamp} ALERT: {message}")
        last_alert_time[resource_key] = now

        # Write alert event to InfluxDB if write_api and bucket provided
        if write_api and influx_bucket:
            try:
                point = (
                    Point("alerts")
                    .tag("resource", resource_key)
                    .field("message", message)
                    .time(int(now * 1e9))  # time in nanoseconds
                )
                write_api.write(bucket=influx_bucket, record=point)
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
