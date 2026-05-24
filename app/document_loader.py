"""
文档加载模块
负责加载和预处理各种格式的文档
"""
from pathlib import Path
from typing import List
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    DirectoryLoader,
)
from langchain_core.documents import Document


class DocumentLoader:
    """文档加载器类"""

    def __init__(self, docs_dir: str = "./docs"):
        """
        初始化文档加载器
        
        Args:
            docs_dir: 文档目录路径
        """
        self.docs_dir = Path(docs_dir)

    def load_pdf(self, file_path: str) -> List[Document]:
        """
        加载PDF文件
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            文档列表
        """
        loader = PyPDFLoader(str(file_path))
        return loader.load()

    def load_text(self, file_path: str) -> List[Document]:
        """
        加载文本文件
        
        Args:
            file_path: 文本文件路径
            
        Returns:
            文档列表
        """
        loader = TextLoader(str(file_path), encoding='utf-8')
        return loader.load()

    def load_directory(self) -> List[Document]:
        """
        加载目录下所有支持的文档
        
        Returns:
            文档列表
        """
        documents = []
        
        # 遍历文档目录
        for file_path in self.docs_dir.rglob("*"):
            if file_path.is_file():
                try:
                    if file_path.suffix.lower() == '.pdf':
                        docs = self.load_pdf(file_path)
                        documents.extend(docs)
                    elif file_path.suffix.lower() in ['.txt', '.md']:
                        docs = self.load_text(file_path)
                        documents.extend(docs)
                except Exception as e:
                    print(f"加载文件 {file_path} 失败: {e}")
        
        return documents

    @staticmethod
    def clean_documents(documents: List[Document]) -> List[Document]:
        """
        清理文档内容
        
        Args:
            documents: 原始文档列表
            
        Returns:
            清理后的文档列表
        """
        cleaned_docs = []
        for doc in documents:
            # 去除多余空白字符
            content = ' '.join(doc.page_content.split())
            if content:  # 只保留非空内容
                doc.page_content = content
                cleaned_docs.append(doc)
        
        return cleaned_docs
