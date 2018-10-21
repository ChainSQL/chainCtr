# coding=utf8

import json

import callStack

class request:
    def __init__(self):
        self.req = {}

    def addKV(self, k, v):
        if isinstance(v, request):
            self.req[k] = v.req
        else:
            self.req[k] = v
        return self

    def newNode(self, name):
        new = request()
        self.req[name] = new.req
        return new

    def asString(self):
        return json.dumps(self.req)

class Reponse(request):
    def __init__(self, command, status = 'success', id = None):
        if command == None:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

        request.__init__(self)
        self._result = self.newNode('result')
        self._result.addKV('command', command)
        self._result.addKV('status', status)

        if id != None and isinstance(id, int):
            self._result.addKV('id', id)

    def addKV(self, k, v):
        self._result.addKV(k, v)
        return self

class joinRequest(request):
    def __init__(self, id = None):
        request.__init__(self)

        self.addKV('command', 'join')
        if id != None and isinstance(id, int):
            self.addKV('id', id)

        self._info = self.newNode('info')
    
    # validator = {'validation_public_key':'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'}
    def addValidator(self, validator):
        if validator.has_key('validation_public_key'):
            self._info.addKV('validator', validator)
        else:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

    def addRPC(self, rpc):
        if rpc.has_key('port') and rpc.has_key('ip'):
            self._info.addKV('rpc', rpc)
        else:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

    def addPeer(self, peer):
        if peer.has_key('port') and peer.has_key('ip'):
            self._info.addKV('peer', peer)
        else:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

    def addWebsocket(self, ws):
        if ws.has_key('port') and ws.has_key('ip'):
            self._info.addKV('websocket', ws)
        else:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

class joinResponse(Reponse):
    def __init__(self, status, id):
        Reponse.__init__(self, 'join', status, id)

class startRequest(request):
    def __init__(self, id = None):
        request.__init__(self)
        self.addKV('command', 'start')
        if id != None and isinstance(id, int):
            self.addKV('id', id)

class startResponse(Reponse):
    def __init__(self, status, id):
        Reponse.__init__(self, 'start', status, id)

    def _add_list_value(self, key, values):
        if isinstance(values, list):
            self.addKV(key, values)
        else:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

    def add_ips_fixed(self, ips):
        self._add_list_value('ips_fixed', ips)

    def add_validators(self, validators):
        self._add_list_value('validators', validators)

class stopRequest(request):
    def __init__(self, id = None):
        request.__init__(self)
        self.addKV('command', 'stop')
        if id != None and isinstance(id, int):
            self.addKV('id', id)
        self._info = self.newNode('info')
    
    def whose(self, who = None):
        # 如果 who 等于 ALL, 会停止所以的节点
        # 否则停止指定的节点
        if who != None:
            self._info.addKV('who', who)

class stopResponse(Reponse):
    def __init__(self, status, id):
        Reponse.__init__(self, 'stop', status, id)

# 列出所以节点
class listRequest(request):
    def __init__(self, id = None):
        request.__init__(self)
        self.addKV('command', 'list')

class listResponse(Reponse):
    def __init__(self, status, id):
        Reponse.__init__(self, 'list', status, id)

    def addNodes(self, nodes):
        if isinstance(nodes, list):
            self.addKV('nodes', nodes)
        else:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

class watchRequest(request):
    def __init__(self):
        request.__init__(self)
        self.addKV('command', 'watch')

class watchResponse(Reponse):
    def __init__(self, status, id):
        Reponse.__init__(self, 'watch', status, id)

    def addNodes(self, nodes):
        if isinstance(nodes, list):
            self.addKV('nodes', nodes)
        else:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

if __name__ == '__main__':
    try:
        join = joinRequest(1000)
        join.addValidator({'validation_public_key':'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'})
        join.addRPC({'port':5005, 'ip':'0.0.0.0', 'admin':'127.0.0.1'})
        join.addPeer({'port':51235, 'ip':'0.0.0.0'})
        join.addWebsocket({'port':6006, 'ip':'0.0.0.0', 'admin':'127.0.0.1'})

        print join.asString()

        joinRes = joinResponse('success', 1000)
        print joinRes.asString()

        startRes = startResponse('success', 1000)
        startRes.add_ips_fixed(['172.16.18.2 51235', '172.16.18.3 51235'])
        startRes.add_validators(['n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'])
        print startRes.asString()

        stopRes = stopResponse('success', 1000)
        print stopRes.asString()

        nodeRes = listResponse('success', 1000)
        nodeRes.addNodes([{'id':0, 'port':5005, 'ip':'172.16.18.2'}, {'id':1, 'port':5005, 'ip':'172.16.18.3'}])
        print nodeRes.asString()

    except Exception as e:
        print  'An error: %s' % e.message
