# Mem0 Graph Memory 示例项目

基于 [mem0 Graph Memory 官方文档](https://docs.mem0.ai/open-source/graph_memory/overview) 的完整示例代码。

## 📁 文件说明

- `main.py` - 原始的聊天机器人代码（已修复类型错误）
- `graph_memory_example.py` - 完整的 Graph Memory 示例（包含多代理支持）
- `simple_graph_memory_demo.py` - 简化的 Graph Memory 演示（推荐新手使用）
- `config_examples.py` - 不同图数据库的配置示例

## 🚀 快速开始

### 1. 安装依赖

```bash
# 基础安装
pip install mem0ai

# 如果需要图数据库支持
pip install 'mem0ai[graph]'
```

### 2. 运行简化演示

```bash
python simple_graph_memory_demo.py
```

### 3. 查看配置示例

```bash
python config_examples.py
```

## 🔧 支持的图数据库

### 1. Neo4j
```python
config = {
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": "neo4j+s://your-instance.com:7687",
            "username": "neo4j",
            "password": "your-password"
        }
    }
}
```

### 2. Memgraph
```python
config = {
    "graph_store": {
        "provider": "memgraph",
        "config": {
            "url": "bolt://localhost:7687",
            "username": "memgraph",
            "password": "your-password"
        }
    }
}
```

### 3. Neptune Analytics
```python
config = {
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
```

### 4. 内存存储（测试用）
```python
config = {
    "graph_store": {
        "provider": "memory"
    }
}
```

## 💡 核心功能

### 基本操作
```python
from mem0 import Memory

# 初始化
memory = Memory.from_config(config_dict=config)

# 添加记忆
memory.add("用户喜欢徒步旅行", user_id="user123")

# 搜索记忆
results = memory.search("徒步", user_id="user123")

# 获取所有记忆
all_memories = memory.get_all(user_id="user123")
```

### 多代理支持
```python
# 为特定代理添加记忆
memory.add("用户偏好意大利菜", user_id="user123", agent_id="food-assistant")

# 搜索特定代理的记忆
results = memory.search("食物偏好", user_id="user123", agent_id="food-assistant")
```

## 🎯 使用场景

1. **聊天机器人记忆** - 记住用户偏好和历史对话
2. **多代理系统** - 不同代理维护各自的记忆
3. **知识图谱** - 构建和查询实体关系
4. **个性化推荐** - 基于用户历史行为推荐

## ⚠️ 注意事项

1. **生产环境**：建议使用图数据库而不是内存存储
2. **API 密钥**：确保正确配置数据库连接信息
3. **数据安全**：敏感信息请使用安全的数据库连接
4. **性能优化**：大量数据时考虑索引和查询优化

## 🔗 相关链接

- [Mem0 官方文档](https://docs.mem0.ai/)
- [Graph Memory 概述](https://docs.mem0.ai/open-source/graph_memory/overview)
- [LangGraph 集成](https://docs.mem0.ai/integrations/langgraph)

## 📝 许可证

本项目仅用于学习和演示目的。请参考 Mem0 的官方许可证。 