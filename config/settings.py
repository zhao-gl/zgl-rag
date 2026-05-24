"""
配置管理模块
负责加载和管理应用程序的配置参数
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 项目根目录
ROOT_DIR = Path(__file__).parent.parent

# OpenAI配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")

# 向量数据库配置
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", str(ROOT_DIR / "data" / "chroma_db"))
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "knowledge_base")

# 文档处理配置
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# 检索配置
TOP_K = int(os.getenv("TOP_K", "5"))

# 文档目录
DOCS_DIR = ROOT_DIR / "docs"
