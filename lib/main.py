from datetime import datetime
from typing import List, Dict, Any

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

from lib.audio import get_embedding
from lib.queries import get_all_tracks, create_track, get_track_with_similar, INDEX_NAME

# Load environment variables
load_dotenv()

# Constants
ELASTICSEARCH_HOST = "http://localhost:9200"
ELASTICSEARCH_INDEX = "tracks"
MAX_SIMILAR_TRACKS = 3
MAX_TRACKS = 1000

# Initialize FastAPI app
app = FastAPI(
    title="Music Maker API",
    description="API for managing and searching music tracks using audio embeddings",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Elasticsearch client
es = Elasticsearch(
    hosts=[ELASTICSEARCH_HOST],
    basic_auth=(os.getenv("ELASTIC_USERNAME"), os.getenv("ELASTIC_PASSWORD"))
)

@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint returning API status."""
    return {"message": "Music library API is running"}

@app.get("/tracks")
async def get_tracks():
    try:
        return get_all_tracks(es)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tracks")
async def create_track(track_name: str = Form(...), audio_file: UploadFile = File(...)):
    if not audio_file.content_type.startswith('audio/'):
        raise HTTPException(status_code=400, detail="Please upload an audio file")

    try:
        emb = get_embedding(audio_file.file.name)
        return create_track(es, track_name, emb)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        audio_file.file.close()

@app.get("/tracks/{id}")
async def get_track(id: str):
    try:
        return get_track_with_similar(es, id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))