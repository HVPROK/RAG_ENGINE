from fastapi import FastAPI
from routes import ingest, query

app = FastAPI(title="Web-Aware RAG Engine")

app.include_router(ingest.router, prefix="/ingest", tags=["Ingestion"])
app.include_router(query.router, prefix="/query", tags=["Query"])

@app.get("/")
def root():
    return {"message": "RAG Engine API is running 🚀"}