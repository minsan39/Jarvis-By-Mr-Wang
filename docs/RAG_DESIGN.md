# RAG 检索增强生成设计

## RAG 流程

```
用户问题 ──► Embedding ──► 向量检索 ──► Context组装 ──► LLM生成 ──► 回答
                 │              │
                 ▼              ▼
           text2vec模型      FAISS向量库
```

## 文档处理流程

```
knowledge_base/
    ├── resume.pdf       ──► PDF Loader ──► Text Splitter ──► chunks
    ├── projects.md      ──► Text Loader  ──► Text Splitter ──► chunks
    └── skills.txt       ──► Text Loader  ──► Text Splitter ──► chunks
                                                              │
                                                              ▼
                                                        向量数据库
                                                         (FAISS)
```

## 核心组件

### 1. Document Loader
支持多种文档格式：
- PDF: `PyPDFLoader`
- Markdown/TXT: `TextLoader`
- DOCX: `Docx2txtLoader`

### 2. Text Splitter
分块策略：
- **chunk_size**: 500 字符
- **chunk_overlap**: 50 字符
- **separator**: 句号、换行符、段落边界

### 3. Embedding
使用 `text2vec-base-chinese` 模型：
- 维度: 768
- 特点: 中文语义理解优秀

### 4. Vector Store
FAISS 向量数据库：
- Index类型: `IndexFlatIP` (余弦相似度)
- 持久化: 本地磁盘存储

### 5. Retriever
检索策略：
- **相似度检索**: Top-K 最相关文档
- **混合检索**: 关键词 + 语义 (可选)
- **重排序**: MMR (可选)

## 检索增强策略

### 基础RAG
```python
# 1. 检索相关文档
docs = retriever.get_relevant_documents(query)

# 2. 组装Prompt
prompt = f"基于以下上下文回答：\n{context}\n\n问题：{query}"

# 3. LLM生成
response = llm.invoke(prompt)
```

### 带历史记忆的RAG
```python
# 1. 获取对话历史
history = memory.load_memory_variables(inputs)

# 2. 整合历史 + 当前问题
enhanced_query = f"历史对话：{history}\n当前问题：{query}"

# 3. 检索 + 生成
```

## 知识库内容建议

用于面试的简历知识库：
- 简历全文 (PDF)
- 项目经历详细描述
- 技术栈深入理解
- 常见面试题答案

## 性能优化

1. **向量库预加载**: 启动时加载向量库，避免首次查询延迟
2. **批量嵌入**: 文档处理时批量嵌入，减少API调用
3. **缓存**: 热门问题结果缓存
4. **异步**: 检索和生成可并行

## 评估指标

- **召回率**: 检索到的相关文档比例
- **精确率**: 检索结果中真正相关的比例
- **回答质量**: 生成回答的准确性、相关性
