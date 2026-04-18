from langchain_community.chat_models import ChatZhipuAI
from langchain.messages import AIMessage, HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["ZHIPUAI_API_KEY"] = os.getenv("ZHIPUAI_API_KEY")
chat = ChatZhipuAI(
    model=os.getenv("ZHIPUAI_MODEL"),
    temperature=os.getenv("ZHIPUAI_TEMPERATURE"),
    streaming=True,
)
messages = [
    AIMessage(content="你好"),
    SystemMessage(content="你是一个ai助手"),
    HumanMessage(content="帮助用户解决问题"),
]
response = chat.invoke(messages)
print(response.content)  # 显示ai助手的回复