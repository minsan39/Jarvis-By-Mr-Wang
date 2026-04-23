from langchain_community.document_loaders import(
    PyPDFLoader,
    UnstructuredWordDocumentLoader,
    TextLoader,
)
import os

def load_documents(file_path: str):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
    elif ext in [".docx", ".doc"]:
        loader = UnstructuredWordDocumentLoader(file_path)
    elif ext == ".txt":
        loader = TextLoader(file_path, encoding="utf-8")
    else:
        raise ValueError(f"不支持的格式: {ext}")
    
    return loader.load()
