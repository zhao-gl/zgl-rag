"""
RAG引擎模块
实现检索增强生成的核心逻辑
"""
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain
import config.settings as settings


class RAGEngine:
    """RAG引擎类"""

    def __init__(self, retriever):
        """
        初始化RAG引擎
        
        Args:
            retriever: 文档检索器
        """
        self.retriever = retriever
        
        # 初始化LLM
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.OPENAI_BASE_URL,
            temperature=0.7
        )
        
        # 创建问答链
        self.qa_chain = self._create_qa_chain()

    def _create_qa_chain(self):
        """
        创建问答链
        
        Returns:
            检索问答链
        """
        # 定义提示词模板
        prompt_template = """
        你是一个智能助手，基于提供的上下文信息来回答用户问题。

        上下文信息：
        {context}

        用户问题：{input}

        请基于上述上下文信息回答问题。如果上下文中没有相关信息，请明确说明"根据现有知识库，我无法回答这个问题"。
        
        回答：
        """
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        
        # 创建文档处理链
        stuff_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=prompt
        )
        
        # 创建检索链
        retrieval_chain = create_retrieval_chain(
            retriever=self.retriever,
            combine_docs_chain=stuff_chain
        )
        
        return retrieval_chain

    def query(self, question: str) -> dict:
        """
        查询知识库
        
        Args:
            question: 用户问题
            
        Returns:
            包含答案和上下文的字典
        """
        result = self.qa_chain.invoke({"input": question})
        
        return {
            "answer": result["answer"],
            "context": result["context"],
            "question": question
        }

    def query_with_sources(self, question: str) -> dict:
        """
        查询知识库并返回来源信息
        
        Args:
            question: 用户问题
            
        Returns:
            包含答案、上下文和来源的字典
        """
        result = self.query(question)
        
        # 提取来源信息
        sources = []
        for doc in result["context"]:
            source_info = {
                "content": doc.page_content[:200] + "...",
                "metadata": doc.metadata
            }
            sources.append(source_info)
        
        result["sources"] = sources
        
        return result
