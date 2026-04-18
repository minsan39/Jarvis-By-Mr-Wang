# My WeChat Agent

基于智谱AI + LangChain + RAG 的微信智能助手，用于技术能力展示。

## 技术栈

- **LLM**: 智谱AI (GLM-4)
- **框架**: LangChain
- **RAG**: 向量检索 + 知识库问答
- **微信**: wxauto / itchat
- **向量数据库**: FAISS

## 项目结构

```
my_agent/
├── src/                    # 源代码
│   ├── agent/              # 核心智能体
│   ├── config/             # 配置管理
│   ├── memory/             # 对话记忆
│   ├── prompts/            # 提示词模板
│   ├── rag/                # RAG 实现
│   └── wechat/             # 微信接入
├── config/                 # 配置文件
├── knowledge_base/         # 知识库文档
├── tests/                  # 单元测试
├── docs/                   # 技术文档
└── data/                   # 运行时数据
```

## 核心模块

### 1. Agent (`src/agent/`)
核心智能体编排，控制对话流程和工具调用。

### 2. RAG (`src/rag/`)
- 文档加载与分割
- 向量嵌入与存储
- 语义检索

### 3. Memory (`src/memory/`)
- 对话历史管理
- 窗口记忆 / 摘要记忆

### 4. WeChat (`src/wechat/`)
微信消息接收与回复。

### 5. Config (`src/config/`)
统一配置管理，支持 .env 环境变量。

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入你的 API Key
```

### 3. 运行

```bash
python -m src.wechat.bot
```

## 技术亮点

- **RAG**: 基于私有知识库的精准问答
- **记忆**: ConversationBufferMemory + 摘要记忆
- **流式输出**: 支持打字机效果
- **异步**: 异步消息处理，高并发

## License

MIT
