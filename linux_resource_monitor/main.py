# ========================
# main.py
# ========================
import requests
import time
import json
import os
from linux_resource_monitor.collector.config import load_config
from linux_resource_monitor.collector.metrics import collect_metrics
from linux_resource_monitor.collector.alerts import check_alerts
from linux_resource_monitor.collector.logger import setup_logger
from linux_resource_monitor.collector.influx_writer import write_metrics_to_influx


def main():
    config = load_config()
    logger = setup_logger()

    # ✅ Get absolute path to project root
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, '..'))
    json_path = os.path.join(project_root, 'latest_metrics.json')

    while True:
        try:
            metrics = collect_metrics()
            check_alerts(metrics, config['thresholds'], config['alert_cooldown'], logger, config.get('slack_webhook_url'))

            # ✅ Write to InfluxDB
            write_metrics_to_influx(metrics, logger)

            # ✅ Send to cloud endpoint
            response = requests.post(config['cloud_endpoint'], json=metrics)
            response.raise_for_status()
            logger.info(f"Metrics sent: {metrics}")

            # ✅ Write latest_metrics.json to project root
            with open(json_path, "w") as f:
                json.dump(metrics, f)

        except Exception as e:
            logger.error(f"Error: {e}")

        time.sleep(config['collection_interval'])


if __name__ == "__main__":
    main()
