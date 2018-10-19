# coding=utf8

class port:
    def __init__(self, port = 0, protocol = None):
        self.port = port 
        self.ip = '0.0.0.0'
        self.admin = '127.0.0.1'
        self.protocol = protocol 

class node_db:
    def __init__(self):
        self.type = 'RocksDB'
        self.path = './db'
        self.open_files = 2000
        self.filter_bits = 12
        self.cache_mb = 256
        self.file_size_mb = 8
        self.file_size_mult = 2
        self.online_delete = 2000
        self.advisory_delete = 0


class sync_db:
    def __init__(self, type):
        if type == 'mysql':
            self.type = 'mysql'
            self.host = 'localhost'
            self.port = 3306
            self.user = 'root'
            self.passwd = 'root'
            self.db = 'chainsql'
            self.first_storage = 0
            self.unix_socket = None
            self.ssl_ca = None
            self.ssl_cert = None
            self.ssl_key = None
            self.local_infile = None
            self.charset = 'utf8'
        elif type == 'sqlite':
            self.type = 'sqlite'
            self.host = None
            self.port = None
            self.user = None
            self.passwd = None
            self.db = None
            self.first_storage = None
            self.unix_socket = None
            self.ssl_ca = None
            self.ssl_cert = None
            self.ssl_key = None
            self.local_infile = None
            self.charset = None
        else:
            raise Exception("Type Error in sync_db")

class sync_tables:
    def __init__(self):
        self._tables  = []
        
    def addOneTable(self, table):
        if isinstance(table, tuple) == False:
            raise Exception("Type Error in addOneTable")
        else:
            self._tables.append(table)


class chainsqlCfg:
    def __init__(self):
        self.port_rpc_admin_local = port(5005, 'rpc')
        self.port_peer = port(51235, 'peer')
        self.port_ws_admin_local = port(6006, 'ws')
        self.node_size = 'medium'
        self.node_db = node_db()
        self.ledger_history = 'full'
        self.database_path = './db'
        self.debug_logfile = './debug.log'
        self.ips_fix = []
        self.validators = []
        self.validation_public_key = ''
        self.validation_seed = ''
        self.validation_quorum = 1
        self.ssl_verify = 1
        self.auto_sync = 1
        self.sync_db = sync_db('sqlite')
        self.sync_tables = sync_tables()

class blockchain_status:
    def __init__(self):
        # 初始链需要的最少节点数
        self.init_nodes = 4
        # 0 初始状态
        # 1 初始链的节点已经启动
        # 2 初始链节点已经运行成功
        self.status = 0


if __name__ == '__main__':
    try:
        db = sync_db('xx')
        syncs = sync_tables()
        syncs.addOneTable('name')
    except Exception as e:
        print e.message
    pass
