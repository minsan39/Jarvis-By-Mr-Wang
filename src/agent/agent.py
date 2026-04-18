from langchain_community.chat_models import ChatZhipuAI
from langchain.messages import AIMessage, HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()


def create_chat_model():
    os.environ["ZHIPUAI_API_KEY"] = os.getenv("ZHIPUAI_API_KEY")
    return ChatZhipuAI(
        model=os.getenv("ZHIPUAI_MODEL"),
        temperature=float(os.getenv("ZHIPUAI_TEMPERATURE", 0.7)),
        streaming=True,
    )


def get_ai_response(user_message: str, history: list = None) -> str:
    chat = create_chat_model()

    messages = [
        SystemMessage(content="你是一个有帮助的AI助手，请友好地回答用户的问题。"),
    ]

    if history:
        for msg in history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=user_message))

    response = chat.invoke(messages)
    return response.content

def get_ai_response_stream(user_message: str, history: list = None) -> str:
    chat = create_chat_model()
    massages = [
        SystemMessage(content="你是一个有帮助的AI助手，请友好地回答用户问题。"),
    ]
    if history:
        for msg in history:
            if msg["role"] == "user":
                massages.append(HumanMessage(content=msg["content"]))
            else:
                massages.append(AIMessage(content=msg["content"]))
    massages.append(HumanMessage(content=user_message))
    response = chat.stream(massages)
    for chunk in response:
        chunk_content = chunk.content
        if chunk_content:
            chunk_content = chunk_content.replace("\n", "<br>")
        yield chunk_content
    
    
