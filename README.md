# Jarvis By Mr Wang

基于智谱AI + LangChain + RAG 的智能助手，支持知识库问答和工具调用。

## 技术栈

- **LLM**: 智谱AI (GLM-4 / GLM-4-Flash)
- **框架**: LangChain + LangGraph
- **RAG**: 向量检索 + 知识库问答
- **Embedding**: Ollama (mxbai-embed-large)
- **向量数据库**: Chroma
- **前端**: Streamlit
- **会话管理**: 本地 JSON 存储

## 项目结构

```
my_agent/
├── src/
│   ├── agent/           # Agent 核心，包含工具定义
│   ├── rag/             # RAG 实现
│   │   ├── chain.py         # RAG 链
│   │   ├── chunker.py       # 文本分块
│   │   ├── embeddings.py    # 向量嵌入
│   │   ├── loader.py        # 文档加载
│   │   ├── vectorstore.py   # 向量存储
│   │   └── config.py        # 配置
│   ├── session/         # 会话管理
│   └── wechat/          # 微信/企业微信接入
├── main.py              # Streamlit Web 界面
├── knowledge_base/       # 知识库文档
├── vector_db/           # 向量数据库
├── data/                # 会话数据
└── docs/                # 技术文档
```

## 核心功能

### 1. RAG 知识库问答
- 支持上传 TXT/PDF/DOCX 文档
- 自动分块、向量化和存储
- 基于语义检索的精准回答

### 2. Agent 工具调用
- 天气查询
- 文件读写
- 目录浏览
- 知识库检索

### 3. 会话管理
- 多会话支持
- 历史记录保存
- 会话切换与删除

### 4. Web 界面
- Streamlit 实现
- 文档上传
- 实时流式输出

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
ZHIPUAI_API_KEY=your_api_key
ZHIPUAI_MODEL=glm-4-flash
ZHIPUAI_TEMPERATURE=0.7
```

### 3. 启动

```bash
streamlit run main.py
```

访问 http://localhost:8501

## Docker 部署

```bash
docker-compose up -d
```

## 技术亮点

- **RAG + Agent 混合**: 先检索知识库，检索不到再用 Agent 工具
- **流式输出**: 支持打字机效果
- **智能路由**: 根据问题类型自动选择回答方式
- **会话隔离**: 每个会话独立存储

## License

MIT
