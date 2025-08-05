# recommenders/semantic_search.py

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_similar_bios(query_bio, top_k=5):
    print("[INFO] Encoding query...")
    query_vector = model.encode(query_bio).tolist()

    print(f"[INFO] Searching for top {top_k} matches...")
    results = client.search(
        collection_name="user_bios",
        query_vector=query_vector,
        limit=top_k
    )

    print("[RESULTS]")
    for idx, hit in enumerate(results, 1):
        payload = hit.payload
        print(f"{idx}. User ID: {payload.get('user_id')}, Bio: {payload.get('bio')}, Score: {hit.score:.4f}")

    client.close()  # <--- Properly close client

if __name__ == "__main__":
    query_bio = "Software engineer working on machine learning at big tech company"
    search_similar_bios(query_bio)

