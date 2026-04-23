import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_PATH = os.path.join("data", "chroma_db")
DOCUMENTS_PATH = os.path.join("knowledge_base")
CHUNK_SIZE = 500# 每块文本多少字
CHUNK_OVERLAP = 50 # 块与块之间重叠多少字（防止切断句子）
TOP_K = 3# 检索时返回最相关的3个块


