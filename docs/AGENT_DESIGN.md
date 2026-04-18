# Agent 核心设计

## Agent 架构

基于 LangChain 的 ReAct (Reasoning + Acting) 模式：

```
┌──────────────────────────────────────────────────────┐
│                    User Input                        │
│               "介绍一下你的项目经验"                   │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                   Intent Classifier                   │
│           (意图识别: 闲聊/知识问答/任务)                 │
└──────────────────────┬───────────────────────────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
          ▼            ▼            ▼
     ┌─────────┐  ┌──────────┐  ┌─────────┐
     │ 闲聊    │  │ 知识问答  │  │ 任务执行 │
     │ (LLM)  │  │ (RAG+LLM)│  │ (Tools) │
     └─────────┘  └──────────┘  └─────────┘
          │            │            │
          └────────────┼────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│                  Response Output                      │
│                   (格式化回复)                         │
└──────────────────────────────────────────────────────┘
```

## 核心组件

### 1. Intent Classifier
基于规则 + LLM 的意图识别：
- **闲聊**: 打招呼、心情等
- **知识问答**: 简历内容、技术问题
- **任务执行**: 天气查询、计算等

### 2. Memory Manager
对话记忆管理：
```python
class MemoryManager:
    - conversation_buffer: 最近N轮对话
    - summary_memory: 对话摘要
    - entity_memory: 实体信息
```

### 3. Tool Manager
工具注册与调用：
- RAG 检索工具
- 搜索工具 (可选)
- 计算工具 (可选)

### 4. Prompt Manager
动态 Prompt 组装：
- 系统提示词模板
- Few-shot 示例
- 动态变量注入

## LangChain Agent 实现

### 使用 LangChain Expression Language (LCEL)

```python
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate

chain = (
    ChatPromptTemplate.from_messages([...])
    | llm
    | StrOutputParser()
)
```

### Tool Calling Agent

```python
from langchain.agents import create_openai_functions_agent

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

## 对话流程

```
用户: "你好" 
  → Intent: 闲聊
  → Memory: 更新对话历史
  → LLM: 生成问候回复
  → 返回: "你好！有什么可以帮你的吗？"

用户: "介绍一下你的项目经验"
  → Intent: 知识问答
  → Memory: 加载历史上下文
  → RAG: 检索相关项目描述
  → LLM: 组装RAG结果生成回答
  → Memory: 更新对话历史
  → 返回: 项目介绍

用户: "北京天气怎么样"
  → Intent: 任务执行
  → Tool: 调用天气API
  → LLM: 格式化天气信息
  → Memory: 更新对话历史
  → 返回: "北京今天晴，25度..."
```

## 状态管理

```python
class AgentState:
    conversation_id: str      # 会话ID
    user_id: str              # 用户标识
    history: List[Message]    # 对话历史
    context: Dict             # 额外上下文
    current_intent: str       # 当前意图
```

## 错误处理

1. **LLM 超时**: 重试3次，失败返回友好提示
2. **RAG 检索失败**: 回退到纯LLM回答
3. **微信发送失败**: 记录日志，异步重试
4. **API 配额不足**: 限流 + 队列

## 可扩展性

- **多 Agent 协作**: 复杂任务分解给多个 Agent
- **插件系统**: 动态加载工具插件
- **多模态**: 支持图片、语音输入
