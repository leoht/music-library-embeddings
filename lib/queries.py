from datetime import datetime
from typing import List, Dict, Any
from elasticsearch import Elasticsearch

# Elasticsearch constants
INDEX_NAME = "tracks"
MAX_TRACKS = 1000
MAX_SIMILAR_TRACKS = 3
EMBEDDING_FIELD = "audio-embedding"

def get_all_tracks(es: Elasticsearch) -> List[Dict[str, Any]]:
    """Get all tracks from the database, excluding audio embeddings."""
    response = es.search(
        index=INDEX_NAME,
        body={
            "_source": {"exclude": [EMBEDDING_FIELD]},
            "query": {"match_all": {}},
            "size": MAX_TRACKS
        }
    )
    return [{"_id": track["_id"], **track["_source"]} for track in response["hits"]["hits"]]

def create_track(es: Elasticsearch, title: str, embedding: List[float]) -> Dict[str, str]:
    """Create a new track with the given title and audio embedding."""
    doc = {
        "title": title,
        EMBEDDING_FIELD: embedding,
        "timestamp": datetime.now()
    }
    response = es.index(index=INDEX_NAME, body=doc)
    return {"id": response["_id"], "track_name": title}

def get_track_with_similar(es: Elasticsearch, track_id: str) -> Dict[str, Any]:
    """Get a track and its similar tracks based on audio embedding similarity."""
    # Get the track
    response = es.get(index=INDEX_NAME, id=track_id)
    track = response["_source"]
    
    # Get similar tracks
    similar = es.search(
        index=INDEX_NAME,
        body={
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": f"cosineSimilarity(params.query_vector, '{EMBEDDING_FIELD}') + 1.0",
                        "params": {"query_vector": track[EMBEDDING_FIELD]}
                    }
                }
            },
            "size": MAX_SIMILAR_TRACKS,
            "_source": {"exclude": [EMBEDDING_FIELD]}
        }
    )
    
    similar_tracks = [
        {"_id": hit["_id"], **hit["_source"]}
        for hit in similar["hits"]["hits"]
        if hit["_id"] != track_id
    ]
    
    return {
        "_id": response["_id"],
        **response["_source"],
        "similar_tracks": similar_tracks
    } 