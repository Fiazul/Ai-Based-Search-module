from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
from pathlib import Path
import os

file_path = 'knowledge_base.json'
DB_FAISS_PATH = 'faiss_database'


class JSONLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data


def create_vector_db():

    loader = JSONLoader(file_path)
    data = loader.load()

    documents = []
    for item in data:
        text = f"{item['name']} {item['category']} {item['description']}"
        documents.append(text)

    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    db = FAISS.from_texts(documents, embeddings)
    db.save_local(DB_FAISS_PATH)


if __name__ == "__main__":
    create_vector_db()
