import redis
import requests
import asyncio
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
import json

r = redis.Redis(host="redis", port=6379, db=0)
model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(host="qdrant", port=6333)

async def process_url_job():
    while True:
        _, job_data = r.blpop("url_queue")
        job = json.loads(job_data)
        url = job["url"]
        print(f"Processing: {url}")

        content = fetch_content(url)
        chunks = chunk_text(content)
        vectors = model.encode(chunks).tolist()
        store_in_qdrant(url, chunks, vectors)

        print(f"Completed processing: {url}")

def fetch_content(url):
    html = requests.get(url, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(" ", strip=True)

def chunk_text(text, max_len=512):
    words = text.split()
    chunks = [" ".join(words[i:i+max_len]) for i in range(0, len(words), max_len)]
    return chunks

def store_in_qdrant(url, chunks, vectors):
    qdrant.upsert(
        collection_name="web_knowledge",
        points=[
            models.PointStruct(
                id=i,
                vector=vectors[i],
                payload={"url": url, "content": chunks[i]}
            ) for i in range(len(vectors))
        ]
    )

if __name__ == "__main__":
    asyncio.run(process_url_job())