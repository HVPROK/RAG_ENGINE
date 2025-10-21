from fastapi import APIRouter
import redis
import json
import os
from database.db import SessionLocal, URLIngestion

router = APIRouter()

r = redis.Redis(host=os.getenv("REDIS_HOST"), port=int(os.getenv("REDIS_PORT")), db=0)

@router.post("/ingest-url")
async def ingest_url(data: dict):
    url = data.get("url")

    # Save metadata
    db = SessionLocal()
    record = URLIngestion(url=url, status="pending")
    db.add(record)
    db.commit()

    # Push job to Redis queue
    r.rpush("url_queue", json.dumps({"url": url}))
    return {"message": "URL accepted for processing", "status": "pending"}
