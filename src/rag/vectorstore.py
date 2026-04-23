from langchain_community.vectorstores import Chroma
from .embeddings import get_embeddings
from .config import CHROMA_DB_PATH

def get_vectorstore():
    embeddings = get_embeddings()
    return Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )
    
def add_to_vectorstore(documents, ids=None):
    vectorstore = get_vectorstore()
    vectorstore.add_documents(documents=documents, ids=ids)

def similarity_search(query, k=3):
    vectorstore = get_vectorstore()
    return vectorstore.similarity_search(query, k=k)
