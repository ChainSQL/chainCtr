# coding=utf8

import json

import request
import handler
import node
import db

class joinHandler(handler.handler):
    def __init__(self, request, db):
        handler.handler.__init__(self, request, db=db, announce=None)

    def __check__(self):
        if self.request.has_key('command') == False or self.request['command'] != 'join' \
            or self.request.has_key('info') == False or self.request['info'] == None \
            or self.request['info'].has_key('host') == False or self.request['info']['host'] == None \
            or self.request['info'].has_key('validator') == False or self.request['info']['validator'] == None \
            or self.request['info']['validator'].has_key('validation_public_key') == False \
            or self.request['info']['validator']['validation_public_key'] == None:
            return False

        return True

    def process(self):
        res = None 
        
        if self.__check__() == False:
            res = request.joinResponse(1000, self.id)
            res.setErrorMsg('check failure')
            return res

        n = node.node()
        n.host = self.request['info']['host']
        n.restart = 0
        n.status = 0
        n.validated = self.request['info']['validated']
        n.conf.validation_public_key = self.request['info']['validator']['validation_public_key']

        if self.request['info'].has_key('rpc'):
            n.conf.port_rpc_admin_local.port = self.request['info']['rpc']['port']
            n.conf.port_rpc_admin_local.ip = self.request['info']['rpc']['ip']
            n.conf.port_rpc_admin_local.admin = self.request['info']['rpc']['admin']
        
        if self.request['info'].has_key('peer'):
            n.conf.port_peer.port = self.request['info']['peer']['port']
            n.conf.port_peer.ip = self.request['info']['peer']['ip']

        if self.request['info'].has_key('ws'):
            n.conf.port_ws_admin_local.port = self.request['info']['ws']['port']
            n.conf.port_ws_admin_local.ip = self.request['info']['ws']['ip']
            n.conf.port_ws_admin_local.admin = self.request['info']['ws']['admin']

        node_id = self.db.nodes().append(n)

        res = request.joinResponse(0, self.id)
        res.setNodeID(node_id)

        return res

def test_handleJoinRequest():
    def failure():
        database = db.connect('G:\\develop\\config.db')
        req = request.joinRequest(host='192.168.31.22', validated=True, id=10000)
        #validator = {'validation_public_key':'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'}
        #req.addValidator(validator)
        req.addRPC({'port':5005, 'ip':'192.168.31.22', 'admin':'127.0.0.1'})
        req.addPeer({'port':51235, 'ip':'192.168.31.22'})
        req.addWebsocket({'port':6006, 'ip':'192.168.31.22', 'admin':'127.0.0.1'})

        handler = joinHandler(json.dumps(req.dumps()), database)
        res = handler.process()
        r = res.dumps()
        assert r['error_code'] == 1000, "error code was wrong"
        assert r['id'] == 10000, "id was wrong"
        assert r['result'] != None, "result was wrong"
        assert r['result']['error_msg'] == 'check failure', "error msg was wrong"

    def success():
        database = db.connect('G:\\develop\\config.db')
        req = request.joinRequest(host='192.168.31.22', id=10000, validated=True)
        validator = {'validation_public_key':'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'}
        req.addValidator(validator)
        req.addRPC({'port':5005, 'ip':'192.168.31.22', 'admin':'127.0.0.1'})
        req.addPeer({'port':51235, 'ip':'192.168.31.22'})
        req.addWebsocket({'port':6006, 'ip':'192.168.31.22', 'admin':'127.0.0.1'})

        handler = joinHandler(json.dumps(req.dumps()), database)
        res = handler.process()
        r = res.dumps()
        assert r['error_code'] == 0, "error code was wrong"
        assert r['id'] == 10000, "id was wrong"
        assert r['result'] != None, "result was wrong"
        assert r['result']['nodeid'] == 1, "nodeid was wrong"


    failure()
    success()

if __name__ == '__main__':
    test_handleJoinRequest()
    pass
