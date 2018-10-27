# coding=utf8

import sqlite3

import callStack
import node

"""
Nodes
| field  | type | desc |
| ------ | ---- | ---- |
| id         | int     | 自动增长                |
| host       | varchar | 主机名                  |
| public_key | varchar | public key              |
| validated  | bool    | 是否是验证节点          |
| retarts    | int     | 重启次数                |
| status     | int     | 运行状态。0 停止 1 运行 |

service
| field  | type | desc |
| ------ | ---- | ---- |
| id      | int  | 外键，指向 Nodes 表 id |
| port    |      |                        |
| ip      |      |                        |
| admin   |      |                        |
| potocol |      |                        |

blockchainstatus
| field  | type | desc |
| ------ | ---- | ---- |
| init   | int  |      |
| status |      |      |
"""

class connect:
    def __init__(self, path):
        try:
            self.conn = sqlite3.connect(path)
            c = self.conn.cursor()
            c.execute('create table if not EXISTS nodes(\
                            `id`	INTEGER PRIMARY KEY AUTOINCREMENT,\
                            `host`	TEXT, \
                            `public_key`	TEXT UNIQUE,\
                            `validated`	INTEGER, \
                            `restarts`	INTEGER,\
                            `status`	INTEGER)')

            c.execute('create table if not EXISTS service(\
                            `id`	INTEGER,\
                            `port`	INTEGER, \
                            `ip`	TEXT,\
                            `admin`	TEXT, \
                            `protocol`	TEXT,\
                            FOREIGN KEY (id) REFERENCES nodes (id) )')

            c.execute('create table if not EXISTS blockchainstatus(\
                            `init`	INTEGER ,\
                            `status`	INTEGER)')

            #values = ('chainSQL', 'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn', '1', 0, 0)
            #c.execute('insert into nodes (host,public_key,validated,restarts,status) values(?,?,?,?,?)', values)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e

    def nodes(self):
        return nodes(self)

    def chain(self, init = 4):
        return chainStatus(self, init)
    
    def close(self):
        self.conn.close()

class chainStatus:
    def __init__(self, conn, init = 4):
        self.__conn__ = conn

        if self.getStatus() == None:
            try:
                c = self.__conn__.conn.cursor()
                v = (init,)
                c.execute('insert into blockchainstatus values(?,0)', v)
                self.__conn__.conn.commit()
            except Exception as e:
                self.__conn__.conn.rollback()
                raise e

    def getStatus(self):
        c = self.__conn__.conn.cursor()
        c.execute('select init,status from blockchainstatus')
        row = c.fetchone()
        if row == None:
            return None
        return {'init': row[0], 'status': row[1]}

    def setStatus(self, status):
        try:
            c = self.__conn__.conn.cursor()
            newStatus = (status,)
            c.execute('update blockchainstatus set status=?', newStatus)
            self.__conn__.conn.commit()
        except Exception as e:
            self.__conn__.conn.rollback()
            raise e
    
    def setinit(self, init):
        try:
            c = self.__conn__.conn.cursor()
            newInit = (init,)
            c.execute('update blockchainstatus set init=?', newInit)
            self.__conn__.conn.commit()
        except Exception as e:
            self.__conn__.conn.rollback()
            raise e

class nodes:
    def __init__(self, conn):
        self.__conn__ = conn

    def append(self, node):
        nodeid = None
        try:
            c = self.__conn__.conn.cursor()
            public_key = (node.conf.validation_public_key,)
            c.execute('select id from nodes where public_key=?', public_key)
            result = c.fetchone()
            if result == None:
                values = (node.host, node.conf.validation_public_key,node.validated, 0, 0)
                c.execute('insert into nodes(host,public_key,validated,restarts,status) \
                            values(?,?,?,?,?)', values)
                
                nodeid = c.lastrowid

                rpc = node.conf.port_rpc_admin_local
                peer = node.conf.port_peer
                ws = node.conf.port_ws_admin_local
                services = [(nodeid, rpc.port, rpc.ip, rpc.admin, rpc.protocol),
                            (nodeid, peer.port, peer.ip, None, peer.protocol),
                            (nodeid, ws.port, ws.ip, ws.admin, ws.protocol)]

                c.executemany('insert into service values(?,?,?,?,?)', services)
            else:
                nodeid = self.update(node)

            self.__conn__.conn.commit()
        except Exception as e:
            self.__conn__.conn.rollback()
            raise e

        return nodeid

    '''
    描述:   根据 id 或是 public key 更新节点信息
            更新的信息包括 public key 和 rpc，peer 和 websocket 服务
    '''
    def update(self, node):
        node_id = None
        try:
            c = self.__conn__.conn.cursor()
            update = (node.conf.validation_public_key,node.id)
            c.execute('select id from nodes where public_key=? or id=?', update)
            result = c.fetchone()
            if result != None:
                values = (node.validated,node.restart,node.status,node.conf.validation_public_key)
                c.execute('update nodes set validated=?,restarts=?,status=? where public_key=?', values)

                node_id = result[0]
                rpc_service = node.conf.port_rpc_admin_local
                update_rpc = (rpc_service.port, rpc_service.ip, rpc_service.admin, node_id)
                c.execute("update service set port=?,ip=?,admin=? where protocol='rpc' and id=?", update_rpc)

                peer_service = node.conf.port_peer
                update_peer = (peer_service.port, peer_service.ip, node_id)
                c.execute("update service set port=?,ip=? where protocol='peer' and id=?", update_peer)

                ws_service = node.conf.port_ws_admin_local
                update_ws = (ws_service.port, ws_service.ip, ws_service.admin, node_id)
                c.execute("update service set port=?,ip=?,admin=? where protocol='ws' and id=?", update_ws)

            self.__conn__.conn.commit()
        except Exception as e:
            self.__conn__.conn.rollback()
            raise e
        return node_id 

    '''
    描述:   根据 id 或是 public key 获取节点信息
    参数：
        condition   如果类型为整数，说明是根据 node id 获取
                    如果类型为字符串，说是是根据 public key 获取
    '''
    def getNode(self, condition):
        select = None
        where = None
        oneNode = None
        c = self.__conn__.conn.cursor()
        if isinstance(condition, int):
            select = 'select id,host,public_key,validated,restarts,status from nodes where id=?'
            where = (condition,)
        elif isinstance(condition, str):
            select = 'select id,host,public_key,validated,restarts,status from nodes where public_key=?'
            where = (condition,)
        else:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

        c.execute(select, where)
        result = c.fetchone()
        if result != None:
            oneNode = node.node()
            oneNode.id = result[0] 
            oneNode.host = result[1]
            oneNode.conf.validation_public_key = result[2]
            oneNode.validated = result[3]
            oneNode.restart = result[4]
            oneNode.status = result[5]

            id=(oneNode.id,)
            for row in c.execute('select port,ip,admin,protocol from service where id=?', id):
                if row[3] == 'rpc':
                    oneNode.conf.port_rpc_admin_local.port = row[0]
                    oneNode.conf.port_rpc_admin_local.ip = row[1]
                    oneNode.conf.port_rpc_admin_local.admin = row[2]
                    oneNode.conf.port_rpc_admin_local.protocol = row[3]
                elif row[3] == 'peer':
                    oneNode.conf.port_peer.port = row[0]
                    oneNode.conf.port_peer.ip = row[1]
                    oneNode.conf.port_peer.protocol = row[3]
                elif row[3] == 'ws':
                    oneNode.conf.port_ws_admin_local.port = row[0]
                    oneNode.conf.port_ws_admin_local.ip = row[1]
                    oneNode.conf.port_ws_admin_local.admin = row[2]
                    oneNode.conf.port_ws_admin_local.protocol = row[3]
        return oneNode

    '''
    描述:   根据 id 或是 public key 更新节点信息, 
            更新的具体信息由 fields 指定
            {
                'host':chainsql,
                'restarts':0,
                'status':0
                'validator': {
                    'validation_public_key':'zn...'
                },
                'rpc': {
                    'port':5005,
                    'ip':'0.0.0.0',
                    'admin':'127.0.0.1'
                },
                'peer': {
                    'port':51235,
                    'ip':'0.0.0.0'
                },
                'ws': {
                    'port':6006,
                    'ip':'0.0.0.0',
                    'admin':'127.0.0.1'
                }
            }
            上面的 key 可以随意组合
    参数：
        condition   如果类型为整数，说明是根据 node id 获取
                    如果类型为字符串，说是是根据 public key 获取
    '''
    def setValues(self, fields, condition):
        where_key = '' 
        where_value = (condition,)
        if isinstance(condition, int):
            where_key = 'id'
        elif isinstance(condition, str):
            where_key = 'public_key'
        else:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

        c = self.__conn__.conn.cursor()
        select = 'select id from nodes where %s=?' % where_key
        c.execute(select, where_value)
        result = c.fetchone()
        if result == None:
            return False

        set_nodes_where = []
        set_nodes = '' 

        # update nodes
        update_nodes = None

        # update rpc
        update_rpc = None
        set_rpc_sevice_where = None

        # update peer
        update_peer = None
        set_peer_sevice_where = None

        # update websocket
        update_ws = None
        set_ws_sevice_where = None

        for key in fields:
            if key == 'rpc':
                update_rpc = "update service set port=?,ip=?,admin=? where id=? and protocol='rpc'"
                rpc = fields[key]
                port = 5005
                ip = '127.0.0.1'
                admin = '127.0.0.1'
                if rpc.has_key('port'):
                    port = rpc['port']
                if rpc.has_key('ip'):
                    ip = rpc['ip']
                if rpc.has_key('admin'):
                    admin = rpc['admin']
                set_rpc_sevice_where = (port, ip, admin, result[0])
            elif key == 'peer':
                update_peer = "update service set port=?,ip=? where id=? and protocol='peer'"
                peer = fields[key]
                port = 51235
                ip = '127.0.0.1'
                if peer.has_key('port'):
                    port = peer['port']
                if peer.has_key('ip'):
                    ip = peer['ip']
                set_peer_sevice_where = (port, ip, result[0])
            elif key == 'ws':
                update_ws = "update service set port=?,ip=?,admin=? where id=? and protocol='ws'"
                ws = fields[key]
                port = 5005
                ip = '127.0.0.1'
                admin = '127.0.0.1'
                if ws.has_key('port'):
                    port = ws['port']
                if ws.has_key('ip'):
                    ip = ws['ip']
                if ws.has_key('admin'):
                    admin = ws['admin']
                set_ws_sevice_where = (port, ip, admin, result[0])
            else:
                set_nodes = set_nodes + ('%s=?' % key)
                set_nodes_where.append(fields[key])
                set_nodes = set_nodes + ','

        if len(set_nodes) != 0:
            set_nodes = set_nodes.strip(',')
            set_nodes_where.append(condition)
            update_nodes = 'update nodes set %s where %s =?' % (set_nodes, where_key)

        #if len(set_nodes) == 0:
        #    return False

        try:
            if update_nodes != None:
                c.execute(update_nodes, tuple(set_nodes_where))

            if update_rpc != None:
                c.execute(update_rpc, set_rpc_sevice_where)

            if update_peer != None:
                c.execute(update_peer, set_peer_sevice_where)

            if update_ws != None:
                c.execute(update_ws, set_ws_sevice_where)

            self.__conn__.conn.commit()
        except Exception as e:
            self.__conn__.conn.rollback()
            raise e

        return True
        

def test_connect():
    try:
        conn = connect('G:\\develop\\config.db')
        nodes = conn.nodes()
        oneNode = node.node()
        oneNode.validated = True
        oneNode.host = '192.168.31.122'
        oneNode.conf.validation_public_key = 'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'
        oneNode.conf.port_rpc_admin_local.port = 5005
        oneNode.conf.port_rpc_admin_local.ip = '0.0.0.0'
        oneNode.conf.port_rpc_admin_local.admin = '127.0.0.1'
        nodes.append(oneNode)
        conn.close()
    except Exception as e:
        print 'An error: ' , e.message

def test_getNode():
    try:
        conn = connect('G:\\develop\\config.db')
        nodes = conn.nodes()
        oneNode = nodes.getNode(1)
        print oneNode
        conn.close()
    except Exception as e:
        print 'An error: ' , e.message

def test_setValues():
    try:
        conn = connect('G:\\develop\\config.db')
        nodes = conn.nodes()
        fields = {
            'host':'chainSQL',
            'validated':1,
            'restarts':3,
            'status': 1,
            'rpc': {
                'port':8008,
                'ip':'172.16.18.3',
                'admin': '127.0.0.1'
            },
            'peer': {
                'port':'61236',
                'ip':'172.16.18.3'
            }
        }
        nodes.setValues(fields, 1)
        conn.close()
    except Exception as e:
        print 'An error: ' , e.message

def test_chainstatus():
    try:
        conn = connect('G:\\develop\\config.db')
        chain = conn.chain()
        print chain.getStatus()

        chain.setinit(8)
        chain.setStatus(1)
        print chain.getStatus()
        
    except Exception as e:
        print 'An error: ', e.message

if __name__ == '__main__':
    test_connect()
    test_getNode()
    test_setValues()
    test_chainstatus()
