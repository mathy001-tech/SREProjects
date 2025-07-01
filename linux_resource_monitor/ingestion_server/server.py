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
