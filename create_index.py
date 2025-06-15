# Create elasticsearch client
from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv

load_dotenv()

es = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=(os.getenv("ELASTIC_USERNAME"), os.getenv("ELASTIC_PASSWORD"))
)

# print(es.info())

# Here we're defining the index configuration. We're setting up mappings for our index which determine the data types for the fields in our documents.
index_config = {
  "mappings": {
    # "_source": {
    #       "excludes": ["audio-embedding"]
    #   },
  "properties": { 
      "audio-embedding": {
        "type": "dense_vector",
        "dims": 2048,
        "index": True,
        "similarity": "cosine"
      },
      "timestamp": {
        "type": "date"
      },
      "title": {
        "type": "text"
      }
    }
  }
}

# Index name for creating in Elasticsearch
index_name = "tracks"

# Checking and creating the index
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    
result = es.indices.create(index=index_name, ignore=400, body=index_config)
print("index created: ", result)

