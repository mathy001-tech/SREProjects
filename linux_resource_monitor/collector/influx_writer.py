from influxdb_client import InfluxDBClient, Point, WriteOptions

# Replace these with your actual values
bucket = "AlertsMonitoring"
org = "ABC"
token = "RjhW99VuHu_tXQhdqC_DGDKPqoS9qO8L-JoJrxHOTMhRSj8vgoZwg36bVufSHviTeB7QygDzy4LKrQe5BLOU2w=="
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=WriteOptions(batch_size=1))

def write_metrics_to_influx(metrics, logger):
    # Calculate average CPU percent
    cpu_percent_list = metrics.get("cpu_percent", [])
    cpu_avg = sum(cpu_percent_list) / len(cpu_percent_list) if cpu_percent_list else 0

    point = (
        Point("system_metrics")
        .tag("host", metrics.get("hostname"))
        .field("cpu_percent_avg", cpu_avg)
        .field("memory_used", metrics['memory']['used'])
        .field("memory_percent", metrics['memory']['percent'])
        .field("disk_used", metrics['disk']['used'])
        .field("disk_percent", metrics['disk']['percent'])
    )
    write_api.write(bucket=bucket, org=org, record=point)
    logger.info("Metrics written to InfluxDB")
