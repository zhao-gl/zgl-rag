"""
向量存储模块
负责文本分割、向量化和存储到向量数据库
"""
from typing import List, Optional
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import config.settings as settings


class VectorStore:
    """向量存储管理类"""

    def __init__(
        self,
        collection_name: str = None,
        persist_directory: str = None
    ):
        """
        初始化向量存储
        
        Args:
            collection_name: 集合名称
            persist_directory: 持久化目录
        """
        self.collection_name = collection_name or settings.COLLECTION_NAME
        self.persist_directory = persist_directory or settings.CHROMA_DB_PATH
        
        # 初始化嵌入模型
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.OPENAI_BASE_URL
        )
        
        # 初始化文本分割器
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )
        
        # 初始化向量数据库
        self.db = None

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        分割文档
        
        Args:
            documents: 原始文档列表
            
        Returns:
            分割后的文档列表
        """
        return self.text_splitter.split_documents(documents)

    def create_store(
        self,
        documents: List[Document],
        recreate: bool = False
    ) -> Chroma:
        """
        创建向量存储
        
        Args:
            documents: 文档列表
            recreate: 是否重新创建（删除旧数据）
            
        Returns:
            Chroma向量数据库实例
        """
        if recreate:
            print(f"重新创建向量数据库: {self.collection_name}")
            self.db = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                persist_directory=self.persist_directory,
            )
        else:
            print(f"添加到现有向量数据库: {self.collection_name}")
            self.db = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
            )
            self.db.add_documents(documents)
        
        # Chroma 会自动持久化，无需手动调用 persist()
        print(f"已处理 {len(documents)} 个文档块")
        
        return self.db

    def load_store(self) -> Chroma:
        """
        加载已有的向量存储
        
        Returns:
            Chroma向量数据库实例
        """
        if self.db is None:
            self.db = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.persist_directory,
            )
        
        return self.db

    def get_retriever(self, k: int = None):
        """
        获取检索器
        
        Args:
            k: 返回的结果数量
            
        Returns:
            检索器对象
        """
        if self.db is None:
            self.load_store()
        
        k = k or settings.TOP_K
        return self.db.as_retriever(search_kwargs={"k": k})

    def clear_store(self):
        """清空向量存储"""
        if self.db:
            self.db.delete_collection()
            self.db = None
            print("向量数据库已清空")
