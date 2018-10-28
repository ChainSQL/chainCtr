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
        return res

    def __check__(self):
        if self.request.has_key('command') == False or self.request['command'] != 'start':
            return False
        return True

def test_startHandler():
    class test:
        def __init__(self):
            pass
        
        def __del__(self):
            print 'del'

        def run(self):
            pass

    t = test()
    print t

if __name__ == '__main__':
    test_startHandler()
    pass