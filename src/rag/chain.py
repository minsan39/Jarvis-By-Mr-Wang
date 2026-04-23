from langchain_core.messages import HumanMessage, SystemMessage
from .vectorstore import similarity_search
from src.agent.agent import get_ai_response

def create_rag_chain(question:str)->str:
    docs =similarity_search(question,k=3)

    context = "\n\n".join([doc.page_content for doc in docs])
    
    prompt = f"""请基于以下资料回答用户的问题。如果资料里没有答案，请如实说明。
    资料：{context}
    用户问题：{question}
    回答："""
    return get_ai_response(prompt)
