import faiss
from sentence_transformers import SentenceTransformer
import json


with open("knowledge_base.json", "r") as f:
    knowledge_base = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

names = [item["name"] for item in knowledge_base]
categories = ["; ".join(item["category"]) for item in knowledge_base]
descriptions = [item["description"] for item in knowledge_base]

texts = [f"{name}. {category}. {description}" for name, category,
         description in zip(names, categories, descriptions)]

embeddings = model.encode(texts)

dimension = embeddings.shape[1]
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(embeddings)


faiss.write_index(faiss_index, "knowledgebase_index.faiss")

# Save metadata (optional, for mapping results back to the original data)
with open("metadata.json", "w") as f:
    json.dump({"texts": texts, "data": knowledge_base}, f)
