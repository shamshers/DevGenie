import os
from utils.chunking import chunk_text
from rag.vectorstore import ingest_documents

DOCS_FOLDER = "docs"
COLLECTION_NAME = "docs"

def get_all_files(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            yield os.path.join(root, file)

def load_and_chunk_file(filepath):
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_text(text, max_length=400, overlap=40)
    # Optionally add metadata (filename, type)
    metadata = {
        "source": os.path.basename(filepath),
        "type": "doc_chunk"
    }
    return [{"text": chunk, "metadata": metadata} for chunk in chunks]

def main():
    all_docs = []
    for filepath in get_all_files(DOCS_FOLDER):
        print(f"Chunking {filepath} ...")
        doc_chunks = load_and_chunk_file(filepath)
        all_docs.extend(doc_chunks)
    print(f"Total chunks: {len(all_docs)}")
    ingest_documents(all_docs, collection_name=COLLECTION_NAME)
    print("Ingestion to Qdrant complete!")

if __name__ == "__main__":
    main()
