import os
from utils.pdf_utils import extract_text_from_pdf
from utils.chunking import chunk_text
from rag.vectorstore import ingest_documents

PDF_FOLDER = "/Users/shamshersingh/PycharmProjects/devgenie/data/docs"
COLLECTION_NAME = "docs"

def main():
    all_docs = []
    for fname in os.listdir(PDF_FOLDER):
        if fname.lower().endswith('.pdf'):
            fpath = os.path.join(PDF_FOLDER, fname)
            print(f"Extracting {fpath}")
            text = extract_text_from_pdf(fpath)
            chunks = chunk_text(text, max_length=400, overlap=40)
            # Add filename as metadata for context
            docs = [{"text": chunk, "metadata": {"source": fname, "type": "pdf_doc"}} for chunk in chunks]
            all_docs.extend(docs)
    print(f"Ingesting {len(all_docs)} chunks to Qdrant...")
    ingest_documents(all_docs, collection_name=COLLECTION_NAME)
    print("Done!")

if __name__ == "__main__":
    main()
