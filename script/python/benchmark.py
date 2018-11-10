# coding=utf8

import sys
import json

import db
import request
import handler
import joinHandler
import startHandler

class Node:
    def __init__(self, id=None):
        self.id = id

    def join(self, host, protocol, validator = None):
        '''
        protocol is:
        {
            rpc: {
                port: 5005,
                ip: '172.16.18.2',
                admin: '127.0.0.1'
            },
            peer: {
                port: 51235,
                ip: '172.16.18.2',
                admin: '127.0.0.1'
            },
            ws: {
                port: 6006,
                ip: '127.0.0.1',
                admin: '127.0.0.1'
            }
        }

        validator is :
            {'validation_public_key':'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'}
        '''
        validated = False
        if validator != None:
            validated = True
        req = request.joinRequest('172.16.18.2', validated)
        req.addPeer(protocol['peer'])
        req.addRPC(protocol['rpc'])
        req.addWebsocket(protocol['ws'])
        if validator != None:
            req.addValidator(validator)
        return req.dumps()

    def start(self):
       req = request.startRequest(self.id, 10000)
       return req.dumps()

    def announce(self, announceMent):
        #print announceMent
        print 'chainsqld would be started.'
        print '  ', announceMent['info']['ips_fixed']
        print '  ', announceMent['info']['validators']

    def handler_response(self, res):
        error_code = res['error_code']
        if error_code == 0:
            print 'join master successfully. nodeid is %d' % res['result']['nodeid']
        else:
            print 'join master unsuccessfully. [%d]' % error_code

class test_announce(handler.announce):
    def __init__(self, db, nodes):
        handler.announce.__init__(self)
        self.__db__ = db
        self.__nodes__ = nodes

    def emit(self, req):
        nodes = []
        self.__db__.nodes().getValidators(nodes)

        announce = request.announceStartRequest(req['id'] + 1)
        ips_fixed = []
        validators = []

        for n in nodes:
            ips_fixed.append('%s %d' % (n['peer_ip'], n['peer_port']))
            validators.append(n['public_key'])

        announce.add_ips_fixed(ips_fixed)
        announce.add_validators(validators)

        for _, n in self.__nodes__.iteritems():
            n.announce(announce.dumps())

        #jprint 'Announce other nodes to start chainsqld: '
        #print announce.dumps()

class master:
    def __init__(self):
        self.database = db.connect('G:\\develop\\master.db')
        self.nodes = {}

    def join(self, joinReq):
        #assert isinstance(joinReq, request.joinRequest), 'type of joinReq should be joinRequest'
        
        h = joinHandler.joinHandler(json.dumps(joinReq), self.database)
        res = h.process()

        node_id = res['result']['nodeid']
        newNode = Node(id=node_id)
        self.nodes[node_id] = newNode
        newNode.handler_response(res)
        #print res

    def start(self, startReq):
        # 在处理 start 指令的时候会通知其他的节点启动 chainsqld
        h = startHandler.startHandler(json.dumps(startReq), self.database, test_announce(self.database, self.nodes))
        res = h.process()
        error_code = res['error_code']
        if error_code == 0:
            print 'start instruction has been emited.'
        else:
            print 'start failure.'
            print res

test_nodes = [
    {
        'host': '172.16.18.2',
        'protocol': {
            'rpc': {
                'port':5005,
                'ip': '172.16.18.2',
                'admin': '127.0.0.1'
            },
            'peer': {
                'port':51235,
                'ip': '172.16.18.2'
            },
            'ws': {
                'port':6006,
                'ip': '172.16.18.2',
                'admin': '127.0.0.1'
            }
        },
        'validator' : {
            'validation_public_key':'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'
        }
    },
    {
        'host': '172.16.18.3',
        'protocol': {
            'rpc': {
                'port':5005,
                'ip': '172.16.18.3',
                'admin': '127.0.0.1'
            },
            'peer': {
                'port':51235,
                'ip': '172.16.18.3'
            },
            'ws': {
                'port':6006,
                'ip': '172.16.18.3',
                'admin': '127.0.0.1'
            }
        },
        'validator' : {
            'validation_public_key':'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVm'
        }
    }
]

if __name__ == '__main__':
    Master = master()
    
    clients = []
    for n in test_nodes:
        newNode = Node()
        clients.append(newNode)
        req = newNode.join(n['host'], n['protocol'], n['validator'])
        Master.join(req)

    startReq = clients[0].start()
    Master.start(startReq)


    
