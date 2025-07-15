"""
演示如何用 mem0 的 Graph Memory 向本地 Neo4j 添加记忆并进行查询，密码用环境变量 NEO4J_PASSWORD。
"""

from mem0 import Memory
import os

# 从环境变量获取 Neo4j 密码
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD")
if not NEO4J_PASSWORD:
    raise ValueError("请先设置环境变量 NEO4J_PASSWORD！")

# 配置本地 Neo4j 连接
config = {
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "bolt://localhost:7687",
            "username": "neo4j",
            "password": NEO4J_PASSWORD,
            "database": "neo4j"
        }
    }
}

# 初始化 Graph Memory
memory = Memory.from_config(config_dict=config)

# 官网例子的记忆内容
memories = [
    "If it doesn't rain today, Bob will go to the park. I'm not sure if he will take an umbrella or not, but he went there yesterday as well.",
    "Alice loves reading books about science fiction. She has a collection of over 100 books.",
    "Bob and Alice are good friends. They often meet at the coffee shop on weekends.",
    "The weather forecast says it will rain tomorrow. Bob usually stays home when it rains.",
]

user_id = "alice123"

# 添加记忆到 Neo4j
print("📝 正在添加记忆到 Neo4j...")
for content in memories:
    memory.add(content, user_id=user_id)
    print(f"✅ 已添加记忆: {content}")

print("\n" + "="*50)
print("🔍 开始查询记忆...")

# 查询示例
queries = [
    "What do we know about Bob?",
    "Tell me about Alice's interests",
    "What happens when it rains?",
    "Where do Bob and Alice meet?",
    "What is the weather forecast?"
]

# 执行查询
for query in queries:
    print(f"\n❓ 查询: {query}")
    try:
        # 使用 memory.search 进行查询
        results = memory.search(query, user_id=user_id)
        
        # 显示向量存储的查询结果
        if results["results"]:
            print("📋 相关记忆 (向量存储):")
            for i, entry in enumerate(results["results"], 1):
                print(f"  {i}. {entry['memory']}")
        else:
            print("❌ 未找到相关记忆")
        
        # 显示图数据库的关系查询结果
        if "relations" in results and results["relations"]:
            print("🔗 实体关系 (图数据库):")
            for i, relation in enumerate(results["relations"], 1):
                print(f"  {i}. {relation['source']} --{relation['relationship']}--> {relation['destination']}")
        else:
            print("🔗 未找到相关实体关系")
            
    except Exception as e:
        print(f"❌ 查询出错: {e}")

print("\n" + "="*50)
print("🎉 查询完成！") 
