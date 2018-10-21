# coding=utf8

import request
import json

class handler:
    def __init__(self, request):
        self.request = json.loads(request.asString())

class joinHandler(handler):
    def __init__(self, request):
        handler.__init__(self, request)


    def __getService(self, serviceName):
        port = None
        ip = None
        admin = None

        if self.request.has_key('info'):
            info = self.request['info']
            if info.has_key(serviceName):
                service = info[serviceName]
                if service.has_key('port'):
                    port = service['port']

                if service.has_key('ip'):
                    ip = service['ip']

                if service.has_key('admin'):
                    admin = service['admin']

        return port, ip, admin

    def getRPC(self):
       return self.__getService('rpc')

    def getPeer(self):
       return self.__getService('peer')   

    def getWebsocket(self):
       return self.__getService('websocket')

    def getPublicKey(self):
        public_key = None
        if self.request.has_key('info'):
            info = self.request['info']
            if info.has_key('validator'):
                validator = info['validator']
                if validator.has_key('validation_public_key'):
                    public_key = validator['validation_public_key']

        return public_key


def test_handleJoinRequest():
    try:
        join = request.joinRequest(1000)
        join.addValidator({'validation_public_key':'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'})
        join.addRPC({'port':5005, 'ip':'0.0.0.0', 'admin':'127.0.0.1'})
        join.addPeer({'port':51235, 'ip':'0.0.0.0'})
        join.addWebsocket({'port':6006, 'ip':'0.0.0.0', 'admin':'127.0.0.1'})

        h = joinHandler(join)
        port, ip, admin = h.getRPC()
        assert port == 5005, 'port expect equal 5005, real equal %d' % port
        assert ip == '0.0.0.0', 'ip expect equal 0.0.0.0, real equal %s' % ip
        assert admin == '127.0.0.1', 'ip expect equal 127.0.0.1, real equal %s' % ip

        port, ip, admin = h.getPeer()
        assert port == 51235, 'port expect equal 51235, real equal %d' % port
        assert ip == '0.0.0.0', 'ip expect equal 0.0.0.0, real equal %s' % ip
        assert admin == None, 'ip expect equal None, real equal %s' % ip

        port, ip, admin = h.getWebsocket()
        assert port == 6006, 'port expect equal 6006, real equal %d' % port
        assert ip == '0.0.0.0', 'ip expect equal 0.0.0.0, real equal %s' % ip
        assert admin == '127.0.0.1', 'ip expect equal 127.0.0.1, real equal %s' % ip

        public_key = h.getPublicKey()
        expect = 'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'
        assert public_key == expect, 'port expect equal %s, real equal %s' % (expect, public_key) 

        print 'test_handleJoinRequest success'
    except Exception as e:
        print 'test_handleJoinRequest failure --> %s' % e.message

if __name__ == '__main__':
    test_handleJoinRequest()
