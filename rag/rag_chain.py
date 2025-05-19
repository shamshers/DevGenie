from langchain.chains import RetrievalQA
from langchain.llms.anthropic import Anthropic
from langchain.vectorstores import Qdrant
from langchain.embeddings import SentenceTransformerEmbeddings

def get_rag_chain():
    # Qdrant must be running and populated with docs for full use.
    llm = Anthropic(model="claude-3-opus-20240229")
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Qdrant(collection_name="docs", embeddings=embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return chain
