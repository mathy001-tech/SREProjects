# ========================
# ingestion_server/server.py
# ========================

from fastapi import FastAPI, Request
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI()

@app.post("/ingest")
async def ingest_metrics(request: Request):
    data = await request.json()
    logging.info(f"Received metrics: {data}")
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("linux_resource_monitor.ingestion_server.server:app", host="127.0.0.1", port=8000, reload=True)
