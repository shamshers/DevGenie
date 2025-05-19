import os
from utils.chunking import chunk_python_code_by_function
from rag.vectorstore import ingest_documents

def ingest_py_file(file_path, metadata=None, collection_name="docs"):
    """
    Read a Python file, chunk it, and ingest each chunk with optional metadata.
    """
    with open(file_path, "r") as f:
        code = f.read()
    chunks = chunk_python_code_by_function(code)
    docs = []
    for i, chunk in enumerate(chunks):
        meta = metadata.copy() if metadata else {}
        meta["file"] = os.path.basename(file_path)
        meta["chunk_id"] = i
        docs.append({"text": chunk, "metadata": meta})
    ingest_documents(docs, collection_name=collection_name)
    print(f"Ingested {len(docs)} chunks from {file_path}")

def ingest_docs_from_folder(folder_path, collection_name="docs"):
    """
    Ingest all .py files in a folder (recursively).
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                ingest_py_file(path, collection_name=collection_name)
