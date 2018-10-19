# coding=utf8

"""
Nodes
| id         | int     | 自动增长                |
| ---------- | ------- | ----------------------- |
| host       | varchar | 主机名                  |
| public_key | varchar | public key              |
| validated  | bool    | 是否是验证节点          |
| retarts    | int     | 重启次数                |
| status     | int     | 运行状态。0 停止 1 运行 |

service
| id      | int  | 外键，指向 Nodes 表 id |
| ------- | ---- | ---------------------- |
| port    |      |                        |
| ip      |      |                        |
| admin   |      |                        |
| potocol |      |                        |

blockchainstatus
| init   | int  |      |
| ------ | ---- | ---- |
| status |      |      |
"""