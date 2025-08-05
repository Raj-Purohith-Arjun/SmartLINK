import json
import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import numpy as np

# Load bios from parsed JSONL
def load_bios(jsonl_path='ingest/parsed_bios.jsonl'):
    bios = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            bios.append(json.loads(line))
    return bios

# Embed bios using sentence-transformers
def embed_texts(texts, model_name='sentence-transformers/all-MiniLM-L6-v2'):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings

# ... your existing imports and code ...

def embed_and_upload():
    print("[INFO] Loading bios...")
    bios = load_bios()
    texts = [bio["bio"] for bio in bios]
    
    print("[INFO] Embedding bios...")
    vectors = embed_texts(texts)

    client = QdrantClient(host="localhost", port=6333)

    client.recreate_collection(
        collection_name="user_bios",
        vectors_config=VectorParams(size=len(vectors[0]), distance=Distance.COSINE),
    )
    print("[INFO] Collection 'user_bios' created.")

    points = [
        PointStruct(
            id=idx + 1,
            vector=vectors[idx],
            payload={
                "user_id": bio["user_id"],
                "bio": bio["bio"]
            }
        )
        for idx, bio in enumerate(bios)
    ]

    print("[INFO] Uploading points to Qdrant...")
    client.upsert(collection_name="user_bios", points=points)
    print(f"[SUCCESS] Uploaded {len(points)} vectors to Qdrant.")

    client.close()  # <--- Properly close client

if __name__ == "__main__":
    embed_and_upload()
