import os

from panns_inference import AudioTagging
import numpy as np
import librosa
from datetime import datetime
from elasticsearch import Elasticsearch

# load the default model into the gpu.
model = AudioTagging(checkpoint_path=None, device='cuda') # change device to cpu if a gpu is not available
es = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=("elastic", "awesomemusic")
)

# Function to normalize a vector. Normalizing a vector 
# means adjusting the values measured in different scales 
# to a common scale.
def normalize(v):
   # np.linalg.norm computes the vector's norm (magnitude). 
   # The norm is the total length of all vectors in a space.
   norm = np.linalg.norm(v)
   if norm == 0: 
        return v
   
   # Return the normalized vector.
   return v / norm


# Function to get an embedding of an audio file. An embedding is a reduced-dimensionality representation of the file.
def get_embedding (audio_file):
  # Load the audio file using librosa's load function, which returns an audio time series and its corresponding sample rate.
  a, _ = librosa.load(audio_file, sr=44100)
  
  # Reshape the audio time series to have an extra dimension, which is required by the model's inference function.
  query_audio = a[None, :]
  
  # Perform inference on the reshaped audio using the model. This returns an embedding of the audio. 
  _, emb = model.inference(query_audio)

  # Normalize the embedding. This scales the embedding to have a length (magnitude) of 1, while maintaining its direction.
  normalized_v = normalize(emb[0])

  # Return the normalized embedding required for dot_product elastic similarity dense vector
  return normalized_v


#Storing Songs in Elasticsearch with Vector Embeddings:
def store_in_elasticsearch(song, embedding, path, index_name):
  body = {
      'audio-embedding' : embedding,
      'title': song,
      'timestamp': datetime.now(),
  }


  es.index(index=index_name, document=body)
  print ("stored...",song, embedding, path, index_name)
  
if __name__ == "__main__":
    audio_file = "./audio_file.mp3"
    embedding = get_embedding(audio_file)
    print(embedding)
    store_in_elasticsearch('Blurred', embedding, audio_file, "tracks")