from langchain_community.chat_models import ChatZhipuAI
from langchain.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["ZHIPUAI_API_KEY"] = os.getenv("ZHIPUAI_API_KEY")
chat = ChatZhipuAI(
    model=os.getenv("ZHIPUAI_MODEL"),
    temperature=0.7,
    streaming=True,
)

messages = [
    SystemMessage(content="你是一个有帮助的AI助手。"),
    HumanMessage(content="请用三行介绍自己，每行一句话"),
]

print("=== 流式输出每个 chunk ===")
full_content = ""
for i, chunk in enumerate(chat.stream(messages)):
    content = chunk.content
    full_content += content
    if content:
        print(f"chunk {i}: {repr(content)}")

print(f"\n=== 完整内容 ===")
print(repr(full_content))
print(f"\n=== 是否以换行结尾 ===")
print(f"endswith '\\n': {full_content.endswith(chr(10))}")
print(f"endswith whitespace: {full_content != full_content.rstrip()}")
