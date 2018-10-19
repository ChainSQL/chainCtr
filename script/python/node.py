# coding=utf8

from chainsqlCfg import chainsqlCfg

class node:
    def __init__(self, id = None):
        self.id = None
        self.host = None
        self.conf = chainsqlCfg()
        # 0 停止状态
        # 1 运行状态
        self.status = 0

        # 重启次数
        self.restart = 0

# "host" "version" "peers" "uptime" "completes" "quorum" "status"
class watch_info:
    def __init__(self):
        self.id = None
        self.host = None
        self.version = None
        self.peers = 0
        self.uptime = 0
        self.completes = "empty"
        self.quorum = 0
        self.status = None

if __name__ == '__main__':
    pass