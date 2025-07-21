import faiss
import os
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

model = SentenceTransformer('all-MiniLM-L6-v2')
index_path = "vectorstore_index/index.faiss"
data_path = "vectorstore_index/texts.npy"

def create_or_load_faiss(chunks):
    if os.path.exists(index_path):
        index = faiss.read_index(index_path)
        texts = np.load(data_path, allow_pickle=True)
        return index, texts.tolist()

    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    os.makedirs("vectorstore_index", exist_ok=True)
    faiss.write_index(index, index_path)
    np.save(data_path, np.array(chunks))
    return index, chunks

def search_similar(query, index, texts, top_k=3):
    query_vec = model.encode([query])
    D, I = index.search(np.array(query_vec), top_k)
    return [texts[i] for i in I[0]]

def build_or_load_vectorstore(chunks):
    index_path = "vectorstore_index/faiss_index"

    if not chunks:
        raise ValueError("🚨 Error: No chunks were generated from the PDF!")

    if os.path.exists(index_path):
        return FAISS.load_local(index_path, embeddings=embedding_model, allow_dangerous_deserialization=True)
    
    vectorstore = FAISS.from_texts(chunks, embedding_model)
    vectorstore.save_local(index_path)
    return vectorstore
