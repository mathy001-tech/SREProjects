# ========================
# collector/metrics.py
# ========================
import psutil
import socket
import time

def collect_metrics():
    return {
        "hostname": socket.gethostname(),
        "timestamp": time.time(),
        "cpu_percent": psutil.cpu_percent(percpu=True),
        "memory": psutil.virtual_memory()._asdict(),
        "disk": psutil.disk_usage('/')._asdict()
    }
