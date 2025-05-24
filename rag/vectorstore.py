from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
from transformers import AutoTokenizer, AutoModel
import torch
# ... (add embedding code above)

def ingest_documents(docs, collection_name):
    qdrant = QdrantClient(host="localhost", port=6333)
    dim = 768  # for gte-base, adjust if using another model
    if not qdrant.collection_exists(collection_name):
        qdrant.recreate_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
        )
    points = []
    for idx, doc in enumerate(docs):
        text = doc["text"]
        metadata = doc.get("metadata", {})
        vector = get_embedding(text)
        points.append(
            PointStruct(
                id=idx,
                vector=vector,
                payload={**metadata, "text": text}
            )
        )
    if points:
        qdrant.upsert(collection_name=collection_name, points=points)
        print(f"Upserted {len(points)} points to Qdrant.")



# Pick a model that outputs sentence embeddings; 'sentence-transformers' models work, but you can use others, e.g.:
MODEL_NAME = "thenlper/gte-base"  # Compact, good for general use

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME)

def get_embedding(text):
    # Tokenize input
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    # Get model outputs
    with torch.no_grad():
        outputs = model(**inputs)
    # Mean Pooling (take average over token embeddings)
    last_hidden = outputs.last_hidden_state  # [batch, seq, hidden]
    attention_mask = inputs["attention_mask"]
    mask_expanded = attention_mask.unsqueeze(-1).expand(last_hidden.size()).float()
    sum_embeddings = torch.sum(last_hidden * mask_expanded, dim=1)
    sum_mask = torch.clamp(mask_expanded.sum(dim=1), min=1e-9)
    embedding = (sum_embeddings / sum_mask).squeeze().cpu().numpy()
    return embedding.tolist()
