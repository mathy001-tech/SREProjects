from fastapi.testclient import TestClient
from linux_resource_monitor.ingestion_server.server import app

client = TestClient(app)

def test_ingest_metrics():
    # Send a sample POST request to /ingest endpoint
    response = client.post("/ingest", json={"cpu": 50})

    # Verify status code and JSON response
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
