from mem0 import Memory
from typing import Dict, Any

class GraphMemoryManager:
    """Graph Memory 管理器类"""
    
    def __init__(self, config: Dict[str, Any] | None = None):
        """
        初始化 Graph Memory
        
        Args:
            config: 配置字典，包含图数据库连接信息
        """
        if config is None:
            # 默认配置 - 使用 Neo4j
            config = {
                "graph_store": {
                    "provider": "neo4j",
                    "config": {
                        "url": "neo4j+s://xxx",  # 替换为你的 Neo4j 连接 URL
                        "username": "neo4j",
                        "password": "767632877Kk"        # 替换为你的密码
                    }
                }
            }
        
        self.memory = Memory.from_config(config_dict=config)
    
    def add_memory(self, content: str, user_id: str, agent_id: str | None = None) -> None:
        """
        添加记忆到图数据库
        
        Args:
            content: 记忆内容
            user_id: 用户ID
            agent_id: 代理ID（可选）
        """
        if agent_id:
            self.memory.add(content, user_id=user_id, agent_id=agent_id)
            print(f"✅ 已添加记忆 (用户: {user_id}, 代理: {agent_id}): {content}")
        else:
            self.memory.add(content, user_id=user_id)
            print(f"✅ 已添加记忆 (用户: {user_id}): {content}")
    
    def search_memories(self, query: str, user_id: str, agent_id: str | None = None, limit: int = 5) -> Dict[str, Any]:
        """
        搜索相关记忆
        
        Args:
            query: 搜索查询
            user_id: 用户ID
            agent_id: 代理ID（可选）
            limit: 返回结果数量限制
            
        Returns:
            搜索结果字典
        """
        if agent_id:
            results = self.memory.search(query, user_id=user_id, agent_id=agent_id)
        else:
            results = self.memory.search(query, user_id=user_id)
        
        print(f"🔍 搜索查询: '{query}' (用户: {user_id}{f', 代理: {agent_id}' if agent_id else ''})")
        
        if results["results"]:
            print("📋 相关记忆:")
            for i, entry in enumerate(results["results"][:limit], 1):
                print(f"  {i}. {entry['memory']}")
        else:
            print("⚠️ 没有找到相关记忆")
        
        return results
    
    def get_all_memories(self, user_id: str, agent_id: str | None = None) -> Dict[str, Any]:
        """
        获取用户的所有记忆
        
        Args:
            user_id: 用户ID
            agent_id: 代理ID（可选）
            
        Returns:
            所有记忆的字典
        """
        if agent_id:
            results = self.memory.get_all(user_id=user_id, agent_id=agent_id)
        else:
            results = self.memory.get_all(user_id=user_id)
        
        print(f"📚 用户 {user_id}{f' 的代理 {agent_id}' if agent_id else ''} 的所有记忆:")
        print(f"   总数: {len(results['results'])}")
        
        for i, entry in enumerate(results["results"], 1):
            print(f"   {i}. {entry['memory']}")
        
        return results
    
    def delete_all_memories(self, user_id: str, agent_id: str | None = None) -> None:
        """
        删除用户的所有记忆
        
        Args:
            user_id: 用户ID
            agent_id: 代理ID（可选）
        """
        if agent_id:
            self.memory.delete_all(user_id=user_id, agent_id=agent_id)
            print(f"🗑️ 已删除用户 {user_id} 的代理 {agent_id} 的所有记忆")
        else:
            self.memory.delete_all(user_id=user_id)
            print(f"🗑️ 已删除用户 {user_id} 的所有记忆")


def demo_basic_usage():
    """演示基本用法"""
    print("🚀 Mem0 Graph Memory 基本用法演示")
    print("=" * 50)
    
    # 初始化 Graph Memory（需要配置你的数据库连接）
    # memory_manager = GraphMemoryManager()
    
    # 为了演示，我们创建一个模拟的配置
    demo_config = {
        "graph_store": {
            "provider": "memgraph",  # 使用 Memgraph 作为示例
            "config": {
                "url": "bolt://localhost:7687",
                "username": "memgraph",
                "password": "demo_password",
            },
        },
    }
    
    memory_manager = GraphMemoryManager(demo_config)
    
    user_id = "alice123"
    
    # 添加记忆示例
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
    for memory in memories:
        memory_manager.add_memory(memory, user_id=user_id)
    
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
        memory_manager.search_memories(query, user_id=user_id)
    
    # 获取所有记忆
    print(f"\n📚 获取用户 {user_id} 的所有记忆:")
    memory_manager.get_all_memories(user_id=user_id)


def demo_multi_agent():
    """演示多代理用法"""
    print("\n🤖 Mem0 Graph Memory 多代理演示")
    print("=" * 50)
    
    # 初始化
    demo_config = {
        "graph_store": {
            "provider": "neo4j",
            "config": {
                "url": "neo4j+s://demo",
                "username": "neo4j",
                "password": "demo",
            },
        },
    }
    
    memory_manager = GraphMemoryManager(demo_config)
    user_id = "bob"
    
    # 为不同代理添加记忆
    print("📝 为不同代理添加记忆...")
    
    # 食物助手记忆
    memory_manager.add_memory("I prefer Italian cuisine", user_id=user_id, agent_id="food-assistant")
    memory_manager.add_memory("I love pizza and pasta", user_id=user_id, agent_id="food-assistant")
    memory_manager.add_memory("I don't like spicy food", user_id=user_id, agent_id="food-assistant")
    
    # 健康助手记忆
    memory_manager.add_memory("I'm allergic to peanuts", user_id=user_id, agent_id="health-assistant")
    memory_manager.add_memory("I have diabetes", user_id=user_id, agent_id="health-assistant")
    memory_manager.add_memory("I exercise 3 times a week", user_id=user_id, agent_id="health-assistant")
    
    # 共享记忆（所有代理都可以访问）
    memory_manager.add_memory("I live in Seattle", user_id=user_id)
    memory_manager.add_memory("I work as a software engineer", user_id=user_id)
    
    # 搜索特定代理的记忆
    print("\n🔍 搜索特定代理的记忆:")
    
    print("\n--- 食物助手查询 ---")
    memory_manager.search_memories("What food do I like?", user_id=user_id, agent_id="food-assistant")
    
    print("\n--- 健康助手查询 ---")
    memory_manager.search_memories("What are my allergies?", user_id=user_id, agent_id="health-assistant")
    
    print("\n--- 共享记忆查询 ---")
    memory_manager.search_memories("Where do I live?", user_id=user_id)  # 不指定 agent_id，搜索所有代理


def main():
    """主函数"""
    print("🎯 Mem0 Graph Memory 完整示例")
    print("=" * 60)
    
    try:
        # 基本用法演示
        demo_basic_usage()
        
        # 多代理演示
        demo_multi_agent()
        
        print("\n✅ 演示完成！")
        print("\n💡 提示:")
        print("1. 请确保已安装 mem0ai[graph]: pip install 'mem0ai[graph]'")
        print("2. 配置正确的图数据库连接信息")
        print("3. 支持的图数据库: Neo4j, Memgraph, Neptune Analytics")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        print("请检查配置和依赖是否正确安装")


if __name__ == "__main__":
    main() 