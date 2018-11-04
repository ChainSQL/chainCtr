# coding=utf8

import json

import request
import handler
import node
import db


class startHandler(handler.handler):
    def __init__(self, request, db, announce):
        assert isinstance(announce, handler.announce), 'announce must be object of handler.announce'
        handler.handler.__init__(self, request, db=db, announce=announce)
        self.fromNode = None

    def process(self):
        res = None
        if self.__check__() == False:
            res = request.startResponse(1000, self.id)
            res.setErrorMsg('check failure')
            return res

        if self.request.has_key('info') and self.request['info'].has_key('nodeid'):
            self.fromNode = self.request['info']['nodeid']

        # 通知其他节点启动 chainsqld
        self.announce.emit(self.request)
        
        res = request.startResponse(0, self.id)

        return res

    def __check__(self):
        if self.request.has_key('command') == False or self.request['command'] != 'start':
            return False
        return True

class test_announce(handler.announce):
    def __init__(self, db):
        handler.announce.__init__(self)
        self.__db__ = db

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

        print 'Announce other nodes to start chainsqld: '
        print announce.dumps()

def test_startHandler():
    start = request.startRequest(id = 10000)
    start.setNodeID(1)

    database = db.connect('G:\\develop\\config.db')
    handler = startHandler(json.dumps(start.dumps()), database, test_announce(database))
    handler.process()

if __name__ == '__main__':
    test_startHandler()
    pass
