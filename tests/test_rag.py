import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.rag.loader import load_documents
from src.rag.chunker import split_text
from src.rag.vectorstore import add_to_vectorstore
from src.rag.chain import create_rag_chain

file_path = "tests/test.txt"

print("1. 加载文档...")
doc = load_documents(file_path)
print(f"   加载了 {len(doc)} 个文档")

print("2. 切分文档...")
chunks = split_text(doc)
print(f"   切成 {len(chunks)} 块")

print("3. 存入向量库...")
add_to_vectorstore(chunks)
print("   已存入向量库")

print("4. 测试问答...")
answer = create_rag_chain("Python的创始人是谁？")
print(f"\n回答: {answer}")
