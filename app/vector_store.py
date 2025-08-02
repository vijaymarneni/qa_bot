import faiss
from sentence_transformers import SentenceTransformer
import numpy as np
import pickle
import os

model = SentenceTransformer('all-MiniLM-L6-v2')
index = None
documents = []

def load_store():
    global index, documents
    if os.path.exists("vector_store.index"):
        index = faiss.read_index("vector_store.index")
        with open("documents.pkl", "rb") as f:
            documents = pickle.load(f)

def save_store():
    faiss.write_index(index, "vector_store.index")
    with open("documents.pkl", "wb") as f:
        pickle.dump(documents, f)

def ingest_text(text: str):
    global index, documents
    chunks = [text [i:i+512] for i in range(0, len(text), 512)]
    embeddings = model.encode(chunks)
    if index is None:
        index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    documents.extend(chunks)
    save_store()

def query(q: str, top_k:int = 3) ->str:
    if index is None:
        return "Knowledge base is empty."
    q_emb = model.encode([q])
    D, I = index.search(np.array(q_emb), top_k)
    return "\n---\n".join([documents[i] for i in I[0]])

