from elasticsearch import Elasticsearch
import os
from dotenv import load_dotenv
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize Elasticsearch client
es = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=(os.getenv("ELASTIC_USERNAME"), os.getenv("ELASTIC_PASSWORD"))
)

def get_all_tracks():
    """Retrieve all tracks with their embeddings from Elasticsearch."""
    try:
        response = es.search(
            index="tracks",
            body={
                "size": 1000,  # Adjust based on your dataset size
                "_source": ["title", "audio-embedding", "timestamp"]
            }
        )
        return response["hits"]["hits"]
    except Exception as e:
        print(f"Error retrieving tracks: {e}")
        return []

def plot_embeddings():
    """Plot audio embeddings in 2D using t-SNE."""
    # Get all tracks
    tracks = get_all_tracks()
    if not tracks:
        print("No tracks found")
        return

    # Extract embeddings and titles
    embeddings = []
    titles = []
    timestamps = []

    for track in tracks:
        source = track["_source"]
        if "audio-embedding" in source:
            embeddings.append(source["audio-embedding"])
            titles.append(source["title"])
            timestamps.append(source["timestamp"])

    if not embeddings:
        print("No embeddings found")
        return

    # Convert to numpy array
    embeddings = np.array(embeddings)
    
    # print(embeddings)

    # Reduce dimensionality to 2D using t-SNE
    tsne = TSNE(n_components=2, random_state=42, perplexity=8)
    embeddings_2d = tsne.fit_transform(embeddings)

    # Create the plot
    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], alpha=0.6)

    # Add labels for each point
    for i, title in enumerate(titles):
        plt.annotate(
            title,
            (embeddings_2d[i, 0], embeddings_2d[i, 1]),
            fontsize=8,
            alpha=0.7
        )

    # Customize the plot
    plt.title("Audio Embeddings Visualization")
    plt.xlabel("t-SNE dimension 1")
    plt.ylabel("t-SNE dimension 2")
    plt.grid(True, alpha=0.3)

    # Add timestamp to filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    plt.savefig(f"embeddings_plot_{timestamp}.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Plot saved as embeddings_plot_{timestamp}.png")

if __name__ == "__main__":
    plot_embeddings() 