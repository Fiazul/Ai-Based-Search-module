import faiss
from sentence_transformers import SentenceTransformer
import json

"""
I attempted to include the knowledge base during prompt engineering, but it was too large to be passed as a parameter.
There is a limit to the length of the prompt, so I had to create embeddings instead.
"""
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
