# Dynamic Config

基于Redis Cluster的动态配置管理系统，采用主动拉取(Pull)+推送(Push)双模式更新策略，内置LRU本地缓存。

## 核心特性
- **双模式更新**：主动拉取(过期/缓存未命中) + 推送订阅(实时变更)
- **高效缓存**：LRU本地缓存，支持容量和过期时间配置
- **集群支持**：原生支持Redis Cluster分布式部署
- **高可用**：订阅模式自动重连机制

## 架构设计

## Installation
```bash
pip install dynamic-config
```

## 快速开始
### 客户端
```python
from dynamic_config import DynamicConfigClient

# 初始化客户端
client = DynamicConfigClient(
    cluster_nodes=[{'host': 'redis', 'port': 6301, 'name': 'paas.dc.node1.dzqd.cn:6301'},],
    password='pwd',
    cache_capacity=1000,      # LRU缓存容量
    cache_expire=300,         # 缓存过期时间(秒)
    enable_subscription=True  # 启用订阅接受推送
)

# 读写配置
client.set("timeout", 30)     # 写入配置
timeout = client.get("timeout")  # 读取配置
```

### 管理接口
```python
from dynamic_config import DynamicConfigManager

config_manager = DynamicConfigManager(
    cluster_nodes=[{'host': 'redis', 'port': 6301, 'name': 'paas.dc.node1.dzqd.cn:6301'}],
    password='pwd',
    socket_timeout=10,
    socket_connect_timeout=30,
)

config_manager.create_config("test_key3", "test_value")
config_manager.update_config("test_key3", "updated_value")
config_manager.delete_config("test_key3")

```


## 配置

### Client配置参数
| 参数名 | 类型 | 默认值 | 说明                                                                                              |
|--------|------|--------|-------------------------------------------------------------------------------------------------|
| `cluster_nodes` | List[str] | 必填 | Redis Cluster节点列表 (如 `=[{'host': 'redis', 'port': 6301, 'name': 'paas.dc.node1.dzqd.cn:6301'}]`) |
| `password` | str | None | Redis访问密码                                                                                       |
| `cache_capacity` | int | 1000 | LRU缓存最大容量，0表示不启用本地缓存                                                                            |
| `cache_expire` | int | 300 | 缓存过期时间(秒)                                                                                       |
| `socket_timeout` | int | 10 | Redis操作超时时间(秒)                                                                                  |
| `socket_connect_timeout` | int | 30 | Redis连接超时时间(秒)                                                                                  |
| `enable_subscription` | bool | False | 启用订阅，接收push消息                                                                                   |
| `subscription_reconnection_interval` | int | 5 | 订阅断开后重连间隔(秒)                                                                                    |
| `channel` | str | "global" | 配置变更通知频道前缀                                                                                      |

### 使用建议
1. 高频读、低频写：
   1. 增大cache_expire减少Redis访问；
   2. 关闭订阅或增加订阅断开重连时间间隔，避免长链接占用或频繁建立连接。
2. 低频读、对配置更新时效敏感：关闭cache，每次读取都从Redis获取。
3. 配置立即生效：重启服务（不建议使用接受push消息的订阅模式，仅在服务不支持重启更新配置的情况下使用）。