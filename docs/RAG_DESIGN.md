# RAG 检索增强生成设计

## 状态：规划中

RAG 功能尚未实现，以下是设计文档供参考。

---

## RAG 流程（规划）

```
用户问题 ──► Embedding ──► 向量检索 ──► Context组装 ──► LLM生成 ──► 回答
                 │              │
                 ▼              ▼
           text2vec模型      FAISS向量库
```

## 文档处理流程（规划）

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

## 规划中的核心组件

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

## RAG 实现后的对话流程

```
用户: "介绍一下你的项目经验"
  → Intent: 知识问答
  → RAG: 检索相关项目描述
  → LLM: 组装 RAG 结果生成回答
  → 返回: 项目介绍
```

## 实现步骤（待执行）

1. **文档处理**
   - 创建 `knowledge_base/` 目录
   - 添加简历、项目文档
   - 实现文档加载和分割

2. **向量数据库**
   - 选型：FAISS / ChromaDB / Milvus
   - 实现 embedding 和存储

3. **检索逻辑**
   - 实现相似度检索
   - 优化 Top-K 参数

4. **集成到 Agent**
   - 在 `get_ai_response_stream()` 中集成 RAG
   - 组装 context 到 prompt

## 评估指标

- **召回率**: 检索到的相关文档比例
- **精确率**: 检索结果中真正相关的比例
- **回答质量**: 生成回答的准确性、相关性

## 参考资料

- [LangChain RAG 教程](https://python.langchain.com/docs/tutorials/rag/)
- [FAISS 文档](https://github.com/facebookresearch/faiss)
- [text2vec 模型](https://huggingface.co/shibing624/text2vec-base-chinese)
