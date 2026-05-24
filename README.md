# 基于LangChain的知识库RAG系统

这是一个使用LangChain框架构建的检索增强生成（RAG）知识库系统，支持文档加载、向量化存储和智能问答功能。

## 项目特点

- 📚 **多格式文档支持**：支持PDF、TXT、MD等格式的文档
- 🔍 **智能检索**：基于向量相似度的文档检索
- 💬 **自然语言问答**：使用OpenAI大模型进行智能回答
- 💾 **持久化存储**：使用Chroma向量数据库存储知识
- ⚙️ **灵活配置**：通过环境变量轻松配置系统参数

## 项目结构

```
zgl-rag/
├── app/                    # 应用模块
│   ├── __init__.py
│   ├── document_loader.py  # 文档加载器
│   ├── vector_store.py     # 向量存储管理
│   └── rag_engine.py       # RAG引擎
├── config/                 # 配置模块
│   ├── __init__.py
│   └── settings.py         # 配置管理
├── data/                   # 数据存储目录
│   └── chroma_db/          # Chroma向量数据库
├── docs/                   # 文档目录
│   └── sample_ai_intro.md  # 示例文档
├── .env.example            # 环境变量示例
├── .gitignore
├── main.py                 # 主程序入口
├── pyproject.toml          # 项目依赖配置
└── README.md               # 项目说明
```

## 快速开始

### 1. 环境要求

- Python >= 3.14
- OpenAI API密钥

### 2. 安装依赖

```bash
# 使用uv安装（推荐）
uv sync

# 或使用pip
pip install -e .
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并填写配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置您的OpenAI API密钥：

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-ada-002
```

### 4. 添加文档

将您的文档（PDF、TXT、MD格式）放入 `docs/` 目录中。

### 5. 运行系统

#### 方式一：构建知识库并演示查询

```bash
python main.py
```

#### 方式二：仅构建知识库

```bash
python main.py build
```

#### 方式三：查询知识库

```bash
python main.py query "你的问题"
```

例如：
```bash
python main.py query "什么是人工智能？"
```

#### 方式四：交互式问答模式

```bash
python main.py interactive
```

然后可以连续提问，输入 `quit` 或 `exit` 退出。

## 使用说明

### 基本工作流程

1. **准备文档**：将文档放入 `docs/` 目录
2. **构建知识库**：运行 `python main.py build`
3. **查询知识**：使用query命令或交互模式进行问答

### 自定义配置

在 `.env` 文件中可以调整以下参数：

- `CHUNK_SIZE`：文本块大小（默认1000）
- `CHUNK_OVERLAP`：文本块重叠（默认200）
- `TOP_K`：检索返回的文档数量（默认5）
- `COLLECTION_NAME`：向量数据库集合名称
- `CHROMA_DB_PATH`：向量数据库存储路径

## 核心组件

### DocumentLoader（文档加载器）

负责加载和预处理各种格式的文档：
- PDF文档加载
- 文本文件加载
- Markdown文件加载
- 文档内容清理

### VectorStore（向量存储）

管理文档的向量化和存储：
- 文本分割
- 向量嵌入
- Chroma数据库操作
- 检索器创建

### RAGEngine（RAG引擎）

实现检索增强生成的核心逻辑：
- 文档检索
- 提示词工程
- LLM问答生成
- 来源追踪

## 技术栈

- **LangChain**: AI应用开发框架
- **LangChain-OpenAI**: OpenAI集成
- **Chroma**: 向量数据库
- **PyPDF**: PDF文档处理
- **Python-dotenv**: 环境变量管理

## 常见问题

### Q: 如何添加更多文档格式支持？

A: 在 `app/document_loader.py` 中添加相应的loader即可，LangChain社区提供了丰富的文档加载器。

### Q: 可以使用其他向量数据库吗？

A: 可以，LangChain支持多种向量数据库（如FAISS、Pinecone、Milvus等），修改 `app/vector_store.py` 中的实现即可。

### Q: 如何提高回答质量？

A: 可以尝试：
- 优化文档质量和结构
- 调整CHUNK_SIZE和CHUNK_OVERLAP参数
- 使用更强大的LLM模型
- 优化提示词模板

## 开发计划

- [ ] 支持更多文档格式（Word、Excel等）
- [ ] 添加Web界面
- [ ] 支持多轮对话
- [ ] 添加文档管理功能
- [ ] 支持本地部署的LLM模型

## 许可证

MIT License

## 贡献

欢迎提交Issue和Pull Request！
