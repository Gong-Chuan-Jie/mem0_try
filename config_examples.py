"""
Mem0 Graph Memory 配置示例
基于 https://docs.mem0.ai/open-source/graph_memory/overview
"""

from mem0 import Memory

# 配置示例 1: Neo4j
neo4j_config = {
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "bolt://localhost:7687",
            "username": "neo4j",
            "password": "your-password",
            "database": "neo4j"  # 可选，默认是 neo4j
        }
    }
}

# 配置示例 2: Memgraph
memgraph_config = {
    "graph_store": {
        "provider": "memgraph",
        "config": {
            "url": "bolt://localhost:7687",
            "username": "memgraph",
            "password": "your-password",
        }
    }
}

# 配置示例 3: Neptune Analytics
neptune_config = {
    "graph_store": {
        "provider": "neptune",
        "config": {
            "url": "your-neptune-endpoint.amazonaws.com",
            "port": 8182,
            "region": "us-east-1",
            "access_key": "your-access-key",
            "secret_key": "your-secret-key"
        }
    }
}

# 配置示例 4: 内存存储（用于测试）
memory_config = {
    "graph_store": {
        "provider": "memory"
    }
}

def create_memory_with_config(config: dict, config_name: str):
    """使用指定配置创建 Memory 实例"""
    try:
        memory = Memory.from_config(config_dict=config)
        print(f"✅ 成功创建 {config_name} 配置的 Memory 实例")
        return memory
    except Exception as e:
        print(f"❌ 创建 {config_name} 配置失败: {e}")
        return None

def demo_configs():
    """演示不同配置"""
    print("🔧 Mem0 Graph Memory 配置示例")
    print("=" * 50)
    
    # 使用内存配置（最安全，用于演示）
    print("\n📝 使用内存配置...")
    memory = create_memory_with_config(memory_config, "内存存储")
    
    if memory:
        # 测试基本功能
        user_id = "test_user"
        
        # 添加记忆
        memory.add("这是一个测试记忆", user_id=user_id)
        
        # 搜索记忆
        results = memory.search("测试", user_id=user_id)
        print(f"搜索结果: {results}")
        
        # 获取所有记忆
        all_memories = memory.get_all(user_id=user_id)
        print(f"所有记忆: {all_memories}")

def show_config_instructions():
    """显示配置说明"""
    print("\n📋 配置说明:")
    print("=" * 50)
    
    print("\n1. Neo4j 配置:")
    print("   - 需要 Neo4j 数据库实例")
    print("   - 支持 Neo4j 4.x 和 5.x")
    print("   - 安装: pip install neo4j")
    
    print("\n2. Memgraph 配置:")
    print("   - 需要 Memgraph 数据库实例")
    print("   - 开源图数据库")
    print("   - 安装: pip install memgraph")
    
    print("\n3. Neptune Analytics 配置:")
    print("   - 需要 AWS Neptune 实例")
    print("   - 托管图数据库服务")
    print("   - 安装: pip install boto3")
    
    print("\n4. 内存配置:")
    print("   - 仅用于测试和开发")
    print("   - 数据不会持久化")
    print("   - 无需额外安装")

if __name__ == "__main__":
    demo_configs()
    show_config_instructions() 