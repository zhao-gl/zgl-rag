"""
使用示例 - 演示如何以编程方式使用RAG系统
"""
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from app.document_loader import DocumentLoader
from app.vector_store import VectorStore
from app.rag_engine import RAGEngine
import config.settings as settings


def example_basic_usage():
    """基本使用示例"""
    print("=" * 60)
    print("示例1: 基本使用流程")
    print("=" * 60)
    
    # 1. 加载文档
    print("\n[1] 加载文档...")
    loader = DocumentLoader(settings.DOCS_DIR)
    documents = loader.load_directory()
    print(f"加载了 {len(documents)} 个文档")
    
    # 2. 清理文档
    print("\n[2] 清理文档...")
    documents = loader.clean_documents(documents)
    print(f"清理后剩余 {len(documents)} 个文档")
    
    # 3. 创建向量存储
    print("\n[3] 创建向量存储...")
    vector_store = VectorStore()
    split_docs = vector_store.split_documents(documents)
    print(f"分割为 {len(split_docs)} 个文本块")
    
    # 4. 构建知识库
    print("\n[4] 构建知识库...")
    vector_store.create_store(split_docs, recreate=True)
    
    # 5. 查询
    print("\n[5] 查询知识库...")
    retriever = vector_store.get_retriever()
    engine = RAGEngine(retriever)
    
    question = "什么是人工智能？"
    result = engine.query(question)
    
    print(f"\n问题: {question}")
    print(f"回答: {result['answer']}")
    

def example_query_with_sources():
    """带来源的查询示例"""
    print("\n" + "=" * 60)
    print("示例2: 带来源信息的查询")
    print("=" * 60)
    
    # 假设知识库已构建
    vector_store = VectorStore()
    try:
        vector_store.load_store()
        
        retriever = vector_store.get_retriever()
        engine = RAGEngine(retriever)
        
        question = "人工智能有哪些应用领域？"
        result = engine.query_with_sources(question)
        
        print(f"\n问题: {question}")
        print(f"\n回答:\n{result['answer']}")
        
        print(f"\n参考来源 ({len(result['sources'])} 个):")
        for i, source in enumerate(result['sources'], 1):
            print(f"\n  [{i}] {source['content'][:150]}...")
            if 'source' in source['metadata']:
                print(f"      文件: {Path(source['metadata']['source']).name}")
    
    except Exception as e:
        print(f"请先构建知识库: python main.py build")
        print(f"错误: {e}")


def example_custom_configuration():
    """自定义配置示例"""
    print("\n" + "=" * 60)
    print("示例3: 自定义配置")
    print("=" * 60)
    
    # 使用自定义配置的向量存储
    custom_vector_store = VectorStore(
        collection_name="custom_collection",
        persist_directory="./data/custom_chroma_db"
    )
    
    print("\n创建了自定义配置的向量存储:")
    print(f"  - 集合名称: {custom_vector_store.collection_name}")
    print(f"  - 存储路径: {custom_vector_store.persist_directory}")
    print(f"  - 文本块大小: {settings.CHUNK_SIZE}")
    print(f"  - 文本块重叠: {settings.CHUNK_OVERLAP}")
    print(f"  - 检索数量: {settings.TOP_K}")


def example_add_new_documents():
    """添加新文档示例"""
    print("\n" + "=" * 60)
    print("示例4: 向现有知识库添加新文档")
    print("=" * 60)
    
    # 加载单个文档
    loader = DocumentLoader()
    
    # 假设有一个新文档
    new_doc_path = Path(settings.DOCS_DIR) / "sample_ai_intro.md"
    if new_doc_path.exists():
        documents = loader.load_text(new_doc_path)
        documents = loader.clean_documents(documents)
        
        print(f"\n加载了新文档: {new_doc_path.name}")
        print(f"文档数量: {len(documents)}")
        
        # 添加到现有向量存储
        vector_store = VectorStore()
        try:
            vector_store.load_store()
            split_docs = vector_store.split_documents(documents)
            vector_store.create_store(split_docs, recreate=False)
            print("文档已成功添加到知识库!")
        except Exception as e:
            print(f"请先构建知识库: {e}")


def main():
    """运行所有示例"""
    print("\n欢迎使用LangChain RAG系统 - 使用示例\n")
    
    # 运行示例
    example_basic_usage()
    example_query_with_sources()
    example_custom_configuration()
    example_add_new_documents()
    
    print("\n" + "=" * 60)
    print("示例运行完成!")
    print("=" * 60)
    print("\n提示:")
    print("  - 查看 README.md 了解更多使用方法")
    print("  - 运行 'python main.py interactive' 进入交互模式")
    print("  - 在 .env 文件中自定义配置参数")


if __name__ == "__main__":
    main()
