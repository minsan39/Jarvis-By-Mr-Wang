# Agent 核心设计

## 当前实现

基于 LangChain 的流式对话 Agent：

```
┌──────────────────────────────────────────────────────┐
│                    main.py                           │
│              用户输入 → messages 列表                  │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│              get_ai_response_stream()                 │
│                   (agent.py)                         │
└──────────────────────┬───────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
    ┌──────────┐  ┌──────────┐  ┌─────────┐
    │ System   │  │ History  │  │  User   │
    │ Message  │  │ Messages │  │ Message │
    └──────────┘  └──────────┘  └─────────┘
          │            │            │
          └────────────┼────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                  ChatZhipuAI                          │
│              (智谱AI GLM-4 模型)                       │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                   流式输出 (chunk)                     │
│           chunk.content.replace("\n", "<br>")         │
└──────────────────────────────────────────────────────┘
```

## 核心函数

### 1. create_chat_model()
创建智谱AI聊天模型实例，配置流式输出。

```python
def create_chat_model():
    return ChatZhipuAI(
        model=os.getenv("ZHIPUAI_MODEL"),
        temperature=float(os.getenv("ZHIPUAI_TEMPERATURE", 0.7)),
        streaming=True,
    )
```

### 2. get_ai_response()
非流式响应，直接返回完整回答。

```python
def get_ai_response(user_message: str, history: list = None) -> str:
    # 组装 messages
    # 调用 chat.invoke(messages)
    # 返回 response.content
```

### 3. get_ai_response_stream()
流式响应生成器，实时返回 chunks。

```python
def get_ai_response_stream(user_message: str, history: list = None) -> str:
    for chunk in chat.stream(massages):
        chunk_content = chunk.content
        if chunk_content:
            chunk_content = chunk_content.replace("\n", "<br>")
        yield chunk_content
```

## 消息类型

LangChain 消息类型：
- `SystemMessage`: 系统提示词
- `HumanMessage`: 用户消息
- `AIMessage`: AI 响应

## 流式输出处理

```
AI 输出: "第一段\n\n第二段\n"
  ↓
chunk: "第一段\n\n第二段\n"
  ↓
replace("\n", "<br>"): "第一段<br><br>第二段<br>"
  ↓
main.py 去掉末尾 <br>: "第一段<br><br>第二段"
  ↓
st.markdown(..., unsafe_allow_html=True): 正常渲染换行
```

## 会话历史管理

main.py 中管理会话历史：
```python
# 添加用户消息
st.session_state.messages.append({"role": "user", "content": prompt})

# 添加 AI 响应
st.session_state.messages.append({"role": "assistant", "content": response})

# 传递给 agent（用于上下文）
get_ai_response_stream(prompt, st.session_state.messages[:-1])
```

## 状态管理

```python
st.session_state.messages         # 当前会话的所有消息
st.session_state.current_session  # 当前会话 ID（时间戳）
```

## 待改进点

- [ ] 拼写错误修正：`massages` → `messages`
- [ ] 提取系统提示词到独立配置
- [ ] 支持自定义系统提示词
- [ ] 添加超时处理和重试机制
