"""
真正使用 Neo4j 的 Mem0 Graph Memory 示例
"""

from mem0 import Memory
from typing import Dict, Any

class Neo4jGraphMemory:
    """使用 Neo4j 的 Graph Memory 类"""
    
    def __init__(self, neo4j_url: str = "bolt://localhost:7687", 
                 username: str = "neo4j", password: str = "password"):
        """
        初始化 Neo4j Graph Memory
        
        Args:
            neo4j_url: Neo4j 连接地址
            username: 用户名
            password: 密码
        """
        config = {
            "graph_store": {
                "provider": "neo4j",
                "config": {
                    "url": neo4j_url,
                    "username": username,
                    "password": password,
                    "database": "neo4j"  # 数据库名称
                }
            }
        }
        
        try:
            self.memory = Memory.from_config(config_dict=config)
            print(f"✅ 成功连接到 Neo4j: {neo4j_url}")
        except Exception as e:
            print(f"❌ 连接 Neo4j 失败: {e}")
            print("请确保 Neo4j 正在运行且连接信息正确")
            raise
    
    def add_memory(self, content: str, user_id: str, agent_id: str | None = None) -> None:
        """添加记忆到 Neo4j"""
        try:
            if agent_id:
                self.memory.add(content, user_id=user_id, agent_id=agent_id)
                print(f"✅ 已添加记忆到 Neo4j (用户: {user_id}, 代理: {agent_id}): {content}")
            else:
                self.memory.add(content, user_id=user_id)
                print(f"✅ 已添加记忆到 Neo4j (用户: {user_id}): {content}")
        except Exception as e:
            print(f"❌ 添加记忆失败: {e}")
    
    def search_memories(self, query: str, user_id: str, agent_id: str | None = None) -> Dict[str, Any]:
        """从 Neo4j 搜索记忆"""
        try:
            if agent_id:
                results = self.memory.search(query, user_id=user_id, agent_id=agent_id)
            else:
                results = self.memory.search(query, user_id=user_id)
            
            print(f"🔍 从 Neo4j 搜索: '{query}'")
            if results["results"]:
                print("📋 相关记忆:")
                for i, entry in enumerate(results["results"], 1):
                    print(f"  {i}. {entry['memory']}")
            else:
                print("⚠️ 没有找到相关记忆")
            
            return results
        except Exception as e:
            print(f"❌ 搜索记忆失败: {e}")
            return {"results": []}
    
    def get_all_memories(self, user_id: str, agent_id: str | None = None) -> Dict[str, Any]:
        """从 Neo4j 获取所有记忆"""
        try:
            if agent_id:
                results = self.memory.get_all(user_id=user_id, agent_id=agent_id)
            else:
                results = self.memory.get_all(user_id=user_id)
            
            print(f"📚 从 Neo4j 获取用户 {user_id}{f' 的代理 {agent_id}' if agent_id else ''} 的所有记忆:")
            print(f"   总数: {len(results['results'])}")
            
            for i, entry in enumerate(results["results"], 1):
                print(f"   {i}. {entry['memory']}")
            
            return results
        except Exception as e:
            print(f"❌ 获取记忆失败: {e}")
            return {"results": []}


def demo_neo4j_usage():
    """演示 Neo4j 用法"""
    print("🗄️ Neo4j Graph Memory 演示")
    print("=" * 50)
    
    try:
        # 初始化 Neo4j 连接
        # 注意：需要先启动 Neo4j 数据库
        memory = Neo4jGraphMemory(
            neo4j_url="bolt://localhost:7687",
            username="neo4j", 
            password="password"  # 替换为你的密码
        )
        
        user_id = "neo4j_user"
        
        # 添加记忆到 Neo4j
        memories = [
            "用户喜欢使用 Neo4j 数据库",
            "用户正在学习图数据库技术",
            "用户的项目需要持久化存储",
            "用户对 GraphQL 感兴趣"
        ]
        
        print("\n📝 添加记忆到 Neo4j...")
        for memory_content in memories:
            memory.add_memory(memory_content, user_id=user_id)
        
        # 搜索记忆
        print("\n🔍 从 Neo4j 搜索记忆:")
        queries = [
            "数据库",
            "图数据库",
            "持久化",
            "GraphQL"
        ]
        
        for query in queries:
            print(f"\n--- 查询: {query} ---")
            memory.search_memories(query, user_id=user_id)
        
        # 获取所有记忆
        print(f"\n📚 从 Neo4j 获取用户 {user_id} 的所有记忆:")
        memory.get_all_memories(user_id=user_id)
        
    except Exception as e:
        print(f"❌ Neo4j 演示失败: {e}")
        print("\n💡 请确保:")
        print("1. Neo4j 数据库正在运行")
        print("2. 连接信息正确")
        print("3. 已安装 mem0ai[graph]: pip install 'mem0ai[graph]'")


def check_neo4j_connection():
    """检查 Neo4j 连接"""
    print("🔍 检查 Neo4j 连接...")
    
    try:
        from neo4j import GraphDatabase
        
        # 尝试连接
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "password"))
        
        with driver.session() as session:
            result = session.run("RETURN 1 as test")
            record = result.single()
            if record and record["test"] == 1:
                print("✅ Neo4j 连接成功！")
                return True
            else:
                print("❌ Neo4j 连接测试失败")
                return False
                
    except Exception as e:
        print(f"❌ 无法连接到 Neo4j: {e}")
        print("\n💡 请启动 Neo4j:")
        print("docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest")
        return False


def main():
    """主函数"""
    print("🎯 Neo4j Graph Memory 完整示例")
    print("=" * 60)
    
    # 检查 Neo4j 连接
    if check_neo4j_connection():
        demo_neo4j_usage()
    else:
        print("\n📋 Neo4j 设置指南:")
        print("1. 安装 Docker")
        print("2. 运行: docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest")
        print("3. 访问 http://localhost:7474 设置密码")
        print("4. 安装依赖: pip install 'mem0ai[graph]'")
        print("5. 重新运行此脚本")


if __name__ == "__main__":
    main() 