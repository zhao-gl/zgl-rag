"""
基于LangChain的知识库RAG系统主入口
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from app.document_loader import DocumentLoader
from app.vector_store import VectorStore
from app.rag_engine import RAGEngine
import config.settings as settings


def build_knowledge_base():
    """构建知识库"""
    print("=" * 50)
    print("开始构建知识库...")
    print("=" * 50)
    
    # 1. 加载文档
    print("\n步骤1: 加载文档...")
    loader = DocumentLoader(settings.DOCS_DIR)
    documents = loader.load_directory()
    
    if not documents:
        print("警告: 未找到任何文档")
        return None
    
    print(f"成功加载 {len(documents)} 个文档")
    
    # 2. 清理文档
    print("\n步骤2: 清理文档...")
    documents = loader.clean_documents(documents)
    print(f"清理后剩余 {len(documents)} 个文档")
    
    # 3. 创建向量存储
    print("\n步骤3: 创建向量存储...")
    vector_store = VectorStore()
    split_docs = vector_store.split_documents(documents)
    print(f"文档分割为 {len(split_docs)} 个块")
    
    # 4. 构建向量数据库
    print("\n步骤4: 构建向量数据库...")
    vector_store.create_store(split_docs, recreate=True)
    
    print("\n" + "=" * 50)
    print("知识库构建完成!")
    print("=" * 50)
    
    return vector_store


def query_knowledge_base(question: str):
    """
    查询知识库
    
    Args:
        question: 用户问题
    """
    print("\n" + "=" * 50)
    print(f"问题: {question}")
    print("=" * 50)
    
    # 加载向量存储
    vector_store = VectorStore()
    retriever = vector_store.get_retriever()
    
    # 创建RAG引擎
    engine = RAGEngine(retriever)
    
    # 查询并显示结果
    result = engine.query_with_sources(question)
    
    print("\n回答:")
    print(result["answer"])
    
    print("\n参考来源:")
    for i, source in enumerate(result["sources"], 1):
        print(f"\n来源 {i}:")
        print(f"内容: {source['content']}")
        if 'source' in source['metadata']:
            print(f"文件: {source['metadata']['source']}")
    
    return result


def interactive_mode():
    """交互式问答模式"""
    print("\n进入交互式问答模式 (输入 'quit' 或 'exit' 退出)")
    
    # 初始化RAG引擎
    vector_store = VectorStore()
    retriever = vector_store.get_retriever()
    engine = RAGEngine(retriever)
    
    while True:
        try:
            question = input("\n请输入您的问题: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("再见!")
                break
            
            if not question:
                continue
            
            result = engine.query(question)
            print("\n回答:")
            print(result["answer"])
            
        except KeyboardInterrupt:
            print("\n再见!")
            break
        except Exception as e:
            print(f"发生错误: {e}")


def main():
    """主函数"""
    print("欢迎使用基于LangChain的知识库RAG系统!")
    
    # 检查是否提供了命令行参数
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "build":
            # 构建知识库
            build_knowledge_base()
        
        elif command == "query" and len(sys.argv) > 2:
            # 查询知识库
            question = " ".join(sys.argv[2:])
            query_knowledge_base(question)
        
        elif command == "interactive":
            # 先构建知识库（如果不存在）
            try:
                vector_store = VectorStore()
                vector_store.load_store()
            except Exception:
                print("知识库不存在，正在构建...")
                build_knowledge_base()
            
            # 进入交互模式
            interactive_mode()
        
        else:
            print("用法:")
            print("  python main.py build              - 构建知识库")
            print("  python main.py query <问题>       - 查询知识库")
            print("  python main.py interactive        - 交互式问答")
    else:
        # 默认流程：构建知识库并演示查询
        vector_store = build_knowledge_base()
        
        if vector_store:
            # 演示查询
            demo_questions = [
                "什么是人工智能?",
                "请总结一下文档的主要内容",
            ]
            
            for question in demo_questions:
                query_knowledge_base(question)
                print("\n" + "-" * 50)


if __name__ == "__main__":
    main()
