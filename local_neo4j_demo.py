"""
连接本地 Neo4j Desktop 数据库的 Mem0 Graph Memory 示例
"""

from mem0 import Memory
from typing import Dict, Any

class LocalNeo4jMemory:
    """连接本地 Neo4j Desktop 的 Graph Memory 类"""
    
    def __init__(self, password: str = "your-password"):
        """
        初始化本地 Neo4j Graph Memory
        
        Args:
            password: Neo4j Desktop 中设置的密码
        """
        config = {
            "graph_store": {
                "provider": "neo4j",
                "config": {
                    "url": "bolt://localhost:7687",  # Neo4j Desktop 默认端口
                    "username": "neo4j",
                    "password": password,
                    "database": "neo4j"
                }
            }
        }
        try:
            self.memory = Memory.from_config(config_dict=config)
            print("✅ 成功连接到本地 Neo4j Desktop 数据库，并启用 LLM 自动关系抽取！")
        except Exception as e:
            print(f"❌ 连接 Neo4j 失败: {e}")
            print("\n💡 请确保:")
            print("1. Neo4j Desktop 已启动")
            print("2. 数据库已启动（绿色状态）")
            print("3. 密码正确")
            raise
    
    def add_memory(self, content: str, user_id: str, agent_id: str | None = None) -> None:
        """添加记忆到 Neo4j，自动抽取关系"""
        try:
            if agent_id:
                self.memory.add(content, user_id=user_id, agent_id=agent_id)
                print(f"✅ 已添加记忆 (用户: {user_id}, 代理: {agent_id}): {content}")
            else:
                self.memory.add(content, user_id=user_id)
                print(f"✅ 已添加记忆 (用户: {user_id}): {content}")
        except Exception as e:
            print(f"❌ 添加记忆失败: {e}")
    
    def search_memories(self, query: str, user_id: str, agent_id: str | None = None) -> Dict[str, Any]:
        """搜索记忆"""
        try:
            if agent_id:
                results = self.memory.search(query, user_id=user_id, agent_id=agent_id)
            else:
                results = self.memory.search(query, user_id=user_id)
            
            print(f"🔍 搜索: '{query}'")
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
        """获取所有记忆"""
        try:
            if agent_id:
                results = self.memory.get_all(user_id=user_id, agent_id=agent_id)
            else:
                results = self.memory.get_all(user_id=user_id)
            
            print(f"📚 用户 {user_id}{f' 的代理 {agent_id}' if agent_id else ''} 的所有记忆:")
            print(f"   总数: {len(results['results'])}")
            
            for i, entry in enumerate(results["results"], 1):
                print(f"   {i}. {entry['memory']}")
            
            return results
        except Exception as e:
            print(f"❌ 获取记忆失败: {e}")
            return {"results": []}


def demo_local_neo4j():
    """演示本地 Neo4j 用法"""
    print("🗄️ 本地 Neo4j Desktop Graph Memory 演示")
    print("=" * 60)
    
    # 请替换为您的 Neo4j Desktop 密码
    neo4j_password = input("请输入您的 Neo4j Desktop 密码: ").strip()
    
    if not neo4j_password:
        print("❌ 密码不能为空！")
        return
    
    try:
        # 初始化本地 Neo4j 连接
        memory = LocalNeo4jMemory(password=neo4j_password)
        
        user_id = "local_user"
        
        # 添加记忆到 Neo4j
        memories = [
            "Tom is a friend of Jerry",
            "Jerry likes cheese",
            "Tom chases Jerry",
            "Jerry lives in New York",
            "Tom hates dogs",
            "Spike is a dog",
            "Spike protects Jerry",
            "Tom is a cat",
            "Jerry is a mouse"
        ]
        
        print("\n📝 添加记忆到本地 Neo4j...")
        for memory_content in memories:
            memory.add_memory(memory_content, user_id=user_id)
        
        # 搜索记忆
        print("\n🔍 搜索记忆:")
        queries = [
            "Neo4j",
            "Python",
            "人工智能",
            "聊天机器人",
            "数据库"
        ]
        
        for query in queries:
            print(f"\n--- 查询: {query} ---")
            memory.search_memories(query, user_id=user_id)
        
        # 获取所有记忆
        print(f"\n📚 获取用户 {user_id} 的所有记忆:")
        memory.get_all_memories(user_id=user_id)
        
        print("\n🎉 演示完成！")
        print("💡 您可以在 Neo4j Desktop 中查看数据：")
        print("   1. 打开 Neo4j Desktop")
        print("   2. 点击数据库")
        print("   3. 点击 'Open with Neo4j Browser'")
        print("   4. 运行: MATCH (n) RETURN n")
        
    except Exception as e:
        print(f"❌ 演示失败: {e}")
        print("\n💡 请确保:")
        print("1. Neo4j Desktop 已启动")
        print("2. 数据库已启动（绿色状态）")
        print("3. 密码正确")


def check_neo4j_connection(password: str) -> bool:
    """检查 Neo4j 连接"""
    print("🔍 检查 Neo4j 连接...")
    
    try:
        from neo4j import GraphDatabase
        
        # 尝试连接
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", password))
        
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
        return False


def main():
    """主函数"""
    print("🎯 本地 Neo4j Desktop Graph Memory 示例")
    print("=" * 60)
    
    print("\n📋 使用前请确保:")
    print("1. Neo4j Desktop 已启动")
    print("2. 已创建并启动数据库")
    print("3. 记住数据库密码")
    
    # 获取密码
    password = input("\n请输入您的 Neo4j Desktop 密码: ").strip()
    
    if not password:
        print("❌ 密码不能为空！")
        return
    
    # 检查连接
    if check_neo4j_connection(password):
        demo_local_neo4j()
    else:
        print("\n📋 Neo4j Desktop 设置指南:")
        print("1. 打开 Neo4j Desktop")
        print("2. 创建新项目")
        print("3. 添加数据库 -> Create a Local Graph")
        print("4. 设置密码并启动数据库")
        print("5. 重新运行此脚本")


if __name__ == "__main__":
    main() 