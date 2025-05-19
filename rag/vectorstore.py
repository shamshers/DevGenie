from langchain.vectorstores import Qdrant
from langchain.embeddings import SentenceTransformerEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models as rest
import os

# Set up embeddings and Qdrant client
EMBED_MODEL = "all-MiniLM-L6-v2"

def get_embeddings():
    return SentenceTransformerEmbeddings(model_name=EMBED_MODEL)

def get_qdrant_client():
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    return QdrantClient(url=qdrant_url)

def get_qdrant_vectorstore(collection_name="docs"):
    embeddings = get_embeddings()
    client = get_qdrant_client()
    vectorstore = Qdrant(
        client=client,
        collection_name=collection_name,
        embeddings=embeddings,
    )
    return vectorstore

def create_collection(collection_name="docs"):
    """Create collection if not exists."""
    client = get_qdrant_client()
    if collection_name not in [c.name for c in client.get_collections().collections]:
        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=rest.VectorParams(
                size=384,  # for MiniLM
                distance=rest.Distance.COSINE
            ),
        )

def ingest_documents(docs, collection_name="docs"):
    """
    Ingest a list of docs.
    Each doc should be dict: {"text": "...", "metadata": {...}}
    """
    create_collection(collection_name)
    vectorstore = get_qdrant_vectorstore(collection_name)
    texts = [doc["text"] for doc in docs]
    metadatas = [doc.get("metadata", {}) for doc in docs]
    vectorstore.add_texts(texts=texts, metadatas=metadatas)

def query_similar(query, k=3, collection_name="docs"):
    """Retrieve top-k similar chunks."""
    vectorstore = get_qdrant_vectorstore(collection_name)
    return vectorstore.similarity_search(query, k=k)
