# ========================
# tests/test_metrics.py
# ========================
from linux_resource_monitor.collector.metrics import collect_metrics


def test_collect_metrics():
    metrics = collect_metrics()
    assert 'cpu_percent' in metrics
    assert 'memory' in metrics
    assert 'disk' in metrics
    assert isinstance(metrics['cpu_percent'], list)