# 快速启动指南

## 5分钟快速上手

### 步骤1: 配置环境

1. 复制环境变量模板：
```bash
cp .env.example .env
```

2. 编辑 `.env` 文件，填入您的OpenAI API密钥：
```env
OPENAI_API_KEY=sk-your-api-key-here
```

### 步骤2: 安装依赖

使用uv（推荐）：
```bash
uv sync
```

或使用pip：
```bash
pip install -r requirements.txt
```

### 步骤3: 运行系统

直接运行（构建知识库并演示）：
```bash
python main.py
```

### 步骤4: 开始使用

**命令行查询：**
```bash
python main.py query "什么是人工智能？"
```

**交互模式：**
```bash
python main.py interactive
```

## 常用命令

```bash
# 构建知识库
python main.py build

# 查询问题
python main.py query "你的问题"

# 交互问答
python main.py interactive

# 运行示例代码
python example_usage.py
```

## 添加自己的文档

1. 将文档放入 `docs/` 目录
2. 支持的格式：PDF, TXT, MD
3. 重新构建知识库：
```bash
python main.py build
```

## 自定义配置

编辑 `.env` 文件调整参数：

```env
# 文本分割设置
CHUNK_SIZE=1000        # 每个文本块的大小
CHUNK_OVERLAP=200      # 文本块之间的重叠

# 检索设置
TOP_K=5                # 每次检索返回的文档数量

# 模型设置
OPENAI_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-ada-002
```

## 故障排除

### 问题：ModuleNotFoundError

解决：确保已安装所有依赖
```bash
pip install -r requirements.txt
```

### 问题：OpenAI API错误

解决：检查 `.env` 文件中的API密钥是否正确

### 问题：知识库为空

解决：确保 `docs/` 目录中有文档，然后运行：
```bash
python main.py build
```

## 下一步

- 阅读 [README.md](README.md) 了解详细功能
- 查看 [example_usage.py](example_usage.py) 学习编程接口
- 探索 `app/` 目录下的模块源码

祝您使用愉快！🎉
