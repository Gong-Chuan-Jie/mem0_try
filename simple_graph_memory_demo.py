"""
Mem0 Graph Memory 简化演示
基于 https://docs.mem0.ai/open-source/graph_memory/overview
"""

from mem0 import Memory
from typing import Dict, Any

class SimpleGraphMemory:
    """简化的 Graph Memory 类"""
    
    def __init__(self):
        """初始化 Graph Memory"""
        # 使用默认配置（内存存储）
        self.memory = Memory()
    
    def add_memory(self, content: str, user_id: str) -> None:
        """添加记忆"""
        self.memory.add(content, user_id=user_id)
        print(f"✅ 已添加记忆: {content}")
    
    def search_memories(self, query: str, user_id: str) -> Dict[str, Any]:
        """搜索记忆"""
        results = self.memory.search(query, user_id=user_id)
        
        print(f"🔍 搜索: '{query}'")
        if results["results"]:
            print("📋 相关记忆:")
            for i, entry in enumerate(results["results"], 1):
                print(f"  {i}. {entry['memory']}")
        else:
            print("⚠️ 没有找到相关记忆")
        
        return results
    
    def get_all_memories(self, user_id: str) -> Dict[str, Any]:
        """获取所有记忆"""
        results = self.memory.get_all(user_id=user_id)
        
        print(f"📚 用户 {user_id} 的所有记忆:")
        print(f"   总数: {len(results['results'])}")
        
        for i, entry in enumerate(results["results"], 1):
            print(f"   {i}. {entry['memory']}")
        
        return results


def demo_basic_usage():
    """基本用法演示"""
    print("🚀 Mem0 Graph Memory 基本用法演示")
    print("=" * 50)
    
    # 初始化
    memory = SimpleGraphMemory()
    user_id = "alice123"
    
    # 添加记忆（来自文档示例）
    memories = [
        "I like going to hikes",
        "I love to play badminton", 
        "I hate playing badminton",
        "My friend name is john and john has a dog named tommy",
        "My name is Alice",
        "John loves to hike and Harry loves to hike as well",
        "My friend peter is the spiderman"
    ]
    
    print("\n📝 添加记忆...")
    for memory_content in memories:
        memory.add_memory(memory_content, user_id=user_id)
    
    # 搜索记忆示例
    print("\n🔍 搜索记忆示例:")
    queries = [
        "What is my name?",
        "Who is spiderman?",
        "What activities do I like?",
        "Tell me about my friends"
    ]
    
    for query in queries:
        print(f"\n--- 查询: {query} ---")
        memory.search_memories(query, user_id=user_id)
    
    # 获取所有记忆
    print(f"\n📚 获取用户 {user_id} 的所有记忆:")
    memory.get_all_memories(user_id=user_id)


def demo_conversation_memory():
    """对话记忆演示"""
    print("\n💬 对话记忆演示")
    print("=" * 50)
    
    memory = SimpleGraphMemory()
    user_id = "bob"
    
    # 模拟对话记忆
    conversations = [
        "User: What's the weather like today? Assistant: It's sunny and 25°C",
        "User: I need help with Python. Assistant: I'd be happy to help with Python programming",
        "User: How do I install packages? Assistant: Use pip install package_name",
        "User: What's your favorite color? Assistant: I don't have preferences, but I can help you choose",
        "User: Tell me a joke. Assistant: Why don't scientists trust atoms? Because they make up everything!"
    ]
    
    print("📝 添加对话记忆...")
    for conv in conversations:
        memory.add_memory(conv, user_id=user_id)
    
    # 搜索相关对话
    print("\n🔍 搜索相关对话:")
    search_queries = [
        "weather",
        "Python programming",
        "jokes",
        "package installation"
    ]
    
    for query in search_queries:
        print(f"\n--- 查询: {query} ---")
        memory.search_memories(query, user_id=user_id)


def main():
    """主函数"""
    print("🎯 Mem0 Graph Memory 简化演示")
    print("=" * 60)
    
    try:
        # 基本用法演示
        demo_basic_usage()
        
        # 对话记忆演示
        demo_conversation_memory()
        
        print("\n✅ 演示完成！")
        print("\n💡 提示:")
        print("1. 这个示例使用内存存储，适合学习和测试")
        print("2. 生产环境建议使用图数据库: Neo4j, Memgraph, Neptune")
        print("3. 安装图数据库支持: pip install 'mem0ai[graph]'")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("请确保已安装 mem0ai: pip install mem0ai")


if __name__ == "__main__":
    main() 