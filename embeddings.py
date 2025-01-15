import faiss
from sentence_transformers import SentenceTransformer
import json

faiss_index = faiss.read_index("knowledgebase_index.faiss")
with open("metadata.json", "r") as f:
    metadata = json.load(f)

texts = metadata["texts"]
original_data = metadata["data"]


model = SentenceTransformer("all-MiniLM-L6-v2")


def search_knowledge_base(prompt, top_k=5):

    query_embedding = model.encode([prompt])

    distances, indices = faiss_index.search(query_embedding, top_k)

    results = [original_data[idx] for idx in indices[0]]
    return results


prompt = "I need a photography device. which can be useful or useless, price must be cheap. I need it in black color"
results = search_knowledge_base(prompt)
print("Relevant results:", results)
