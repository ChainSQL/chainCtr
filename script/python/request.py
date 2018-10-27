# coding=utf8

import json

import callStack

class jdata:
    def __init__(self):
        self.__object__ = {}

    def has_key(self, key):
        return self.__object__.has_key(key)

    def __getitem__(self, key):
        return self.__object__[key]

    def __setitem__(self, key, value):
        self.__object__[key] = value
        return self

    def newObject(self, name):
        new = jdata()
        self.__object__[name] = new
        return new

    def add(self, key, value):
        self.__object__[key] = value
        return self

    def append(self, key, value):
        if self.__object__.has_key(key) == False:
            self.__object__[key] = []
        self.__object__[key].append(value)
        return self

    '''
    描述： 将 jdata 对象转换成 json 格式
    '''
    def dumps(self):
        for key, value in self.__object__.iteritems():
            if isinstance(value, jdata):
                  self.__object__[key] = value.dumps()

        return json.loads(json.dumps(self.__object__))


class request:
    def __init__(self, command, id = None):
        self.__jdata__ = jdata()
        self.__jdata__['command'] = command
        if id != None:
            self.__jdata__['id'] = id 

    def __getitem__(self, key):
        return self.__jdata__[key]

    def __setitem__(self, key, value):
        self.__jdata__[key] = value
        return self
        
    def __info__(self):
        info = None
        if self.__jdata__.has_key('info') == False:
            info = self.__jdata__.newObject('info')
        else:
            info = self.__jdata__['info']
        return info

    def setNodeID(self, nodeid):
        info = self.__info__()
        info['nodeid'] = nodeid

    def dumps(self):
        return self.__jdata__.dumps()

class response:
    '''
    {
        'error_code': 0,
        'id': 10000,
        'result': {
            'command': 'cmd' # 某个指令的响应
            'error_msg': 'reason of failure'  # 失败原因
        }
    }
    '''
    def __init__(self, error_code = 0, id = None):
        self.__jdata__ = jdata()
        self.__jdata__['error_code'] = error_code
        if id != None:
            self.__jdata__['id'] = id

    def __result__(self):
        result = None
        if self.__jdata__.has_key('result') == False:
            result = self.__jdata__.newObject('result')
        else:
            result = self.__jdata__['result']
        return result
    
    def __command__(self,command):
        result = self.__result__()
        result['command'] = command

    def setErrorMsg(self, errorMsg):
        result = self.__result__()
        result['error_msg'] = errorMsg

    def dumps(self):
        return self.__jdata__.dumps()

class joinRequest(request):
    '''
    {
        'command': 'join',
        'id': 1000,
        'info': {
            'host': '172.16.18.2', # 本机 ip 地址
            'validated': true, # 是否是验证节点
            'validator': {
                'validation_public_key': 'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'
            },
            'rpc': {
                'port': 5005,
                'ip': '127.0.0.1',
                'admin': '127.0.0.1'
            },
            'peer': {
                'port': 51235,
                'ip': '127.0.0.1',
                'admin': '127.0.0.1'
            },
            'ws': {
                'port': 6006,
                'ip': '127.0.0.1',
                'admin': '127.0.0.1'
            }
        }
    }
    '''
    def __init__(self, host = '127.0.0.1', validated = True,id = None):
        request.__init__(self, 'join', id)
        info = self.__info__()
        info['host'] = host
        info['validated'] = validated

    # validator = {'validation_public_key':'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'}
    def addValidator(self, validator):
        if isinstance(validator, object) == False:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

        info = self.__info__() 
        vd = None
        if info.has_key('validator') == False:
            vd = info.newObject('validator')
        else:
            vd = info['validator']

        for key, value in validator.iteritems():
            vd[key] = value


    def addRPC(self, rpc):
        if isinstance(rpc, object) == False:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

        info = self.__info__() 
        vd = None
        if info.has_key('rpc') == False:
            vd = info.newObject('rpc')
        else:
            vd = info['prc']

        for key, value in rpc.iteritems():
            vd[key] = value

    def addPeer(self, peer):
        if isinstance(peer, object) == False:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

        info = self.__info__() 
        vd = None
        if info.has_key('peer') == False:
            vd = info.newObject('peer')
        else:
            vd = info['peer']

        for key, value in peer.iteritems():
            vd[key] = value

    def addWebsocket(self, ws):
        if isinstance(ws, object) == False:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

        info = self.__info__() 
        vd = None
        if info.has_key('ws') == False:
            vd = info.newObject('ws')
        else:
            vd = info['ws']

        for key, value in ws.iteritems():
            vd[key] = value

class joinResponse(response):
    '''
    {
        'error_code': 0,
        'id': 10000,
        'result': {
            'command': 'join', # 表示 join 指令的响应
            'nodeid': 0,
        }
    }
    '''
    def __init__(self, error_code, id):
        response.__init__(self, error_code, id)
        self.__command__('join')

    def setNodeID(self, nodeid):
        result = self.__result__()
        result['nodeid'] = nodeid

    #def setErrorMsg(self, errorMsg):
    #    result = self.__result__()
    #    result['error_msg'] = errorMsg

    def dumps(self):
        return self.__jdata__.dumps()

class startRequest(request):
    '''
    {
        'command': 'start',
        'id': 10000,
        'info': {
            'nodeid': 0 # 代表谁发起的请求
        }
    }
    '''
    def __init__(self, nodeid = None, id = None):
        request.__init__(self, 'start', id)
        if nodeid != None:
            info = self.__info__()
            info['nodeid'] = nodeid

class startResponse(response):
    '''
    {
        'error_code': 0,
        'id': 10000,
        'result': {
            'ips_fixed': ['172.16.18.2 51235', '172.16.18.3 51235'],
            'validators': ['xxx1', 'xxx2']
        }
    }
    '''
    def __init__(self, error_code, id):
        response.__init__(self, error_code, id)
        self.__command__('start')

    def add_ips_fixed(self, ips):
        result = self.__result__()
        for ip in ips:
            result.append('ips_fixed', ip)

    def add_validators(self, validators):
        result = self.__result__()
        for v in validators:
            result.append('validators', v)

class stopRequest(request):
    '''
    {
        'command': 'stop',
        'id': 10000,
        'info': {
            'whose': 0 # 值为 nodeid，表示要挺某个节点，如果值为 all 表示停止全部节点
        }
    }
    '''
    def __init__(self, id = None):
        request.__init__(self, 'stop', id)
        pass
    
    def whose(self, whoes = None):
        # 如果 who 等于 ALL, 会停止所以的节点
        # 否则停止指定的节点
        if whoes != None:
            info = self.__info__()
            info['whose'] =  whoes

class stopResponse(response):
    '''
    {
        'error_code': 0,
        'id': 10000,
    }
    '''
    def __init__(self, error_code, id):
        response.__init__(self, error_code, id)
        self.__command__('stop')

# 列出所以节点
class listRequest(request):
    '''
    {
        'command': 'list',
        'id': 10000,
        'info': {
            'nodeid': 0 # 谁发起的请求
        }
    }
    '''
    def __init__(self, id = None):
        request.__init__(self, 'list', id)


class listResponse(response):
    '''
    {
        'error_code': 0,
        'id': 10000,
        'result': {
            'nodes':[
                {
                    'id':0, 
                    'host':'172.16.18.2',
                    'rpc':5005,
                    'ws':6006,
                    'peer':51235,
                    'pubkey': 'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'
                }
            ]
        }
    }
    '''
    def __init__(self, error_code, id):
        response.__init__(self, error_code, id)
        self.__command__('list')

    def addNodes(self, nodes):
        result = self.__result__()
        for n in nodes:
            result.append('nodes', n)

class watchRequest(request):
    '''
    {
        'command': 'list',
        'id': 10000,
        'info': {
            'nodeid': 0 # 谁发起的请求
        }
    }
    '''
    def __init__(self, id = None):
        request.__init__(self, 'watch', id)

class watchResponse(response):
    '''
    {
        'error_code': 0,
        'id': 10000,
        'result': {
            'nodes':[
                {
                    'id':0, 
                    'version': '1.0',
                    'peers': '2',
                    'uptime': '10000',
                    'completes': 'true',
                    'quorum': 2,
                    'status': 'success'
                }
            ]
        }
    }
    '''
    def __init__(self, error_code, id):
        response.__init__(error_code, id)
        self.__command__('watch')

    def addNodes(self, nodes):
        result = self.__result__()
        for n in nodes:
            result.append('nodes', n)

class nodeInfo(request):
    '''
    {
        'command': 'nodeinfo',
        'id': 10000,
        'info': {
            'nodeid': 1,
            'version': '1.0',
            'peers': '2',
            'uptime': '10000',
            'completes': 'true',
            'quorum': 2,
            'status': 'success'
        }
    }
    '''
    def __init__(self, id = None):
        request.__init__(self, 'nodeinfo', id)

    '''
    参数 info 为：
    {
        'nodeid': 1,
        'version': '1.0',
        'peers': '2',
        'uptime': '10000',
        'completes': 'true',
        'quorum': 2,
        'status': 'success'
    }
    '''
    def addInfo(self, info):
        if info.has_key('nodeid') == False or info.has_key('version') == False \
            or info.has_key('peers') == False or info.has_key('uptime') == False \
            or info.has_key('completes') == False or info.has_key('quorum') == False \
            or info.has_key('status') == False:
            file, function, line = callStack.currentCallFrame()
            raise Exception('%s: Type Error in %s:%d' % (file, function, line))

        infoObject = self.__info__()
        for key,value in info.iteritems():
            infoObject[key] = value

def test_jdata():
    join = jdata()
    join.add('cmd', 'join')
    join.add('id', 1000)

    info = join.newObject('info')
    info.append('ips_fixed', '172.16.18.2 5005')
    info.append('ips_fixed', '172.16.18.3 5005')
    info.append('validators', 'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn')
    info.append('validators', 'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn')

    info.newObject('validator') \
    .add('public', 'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn') \
    .add('seed', 'ssssssss')

    req = join.dumps()
    assert req['cmd'] == 'join', 'cmd expect equal join, real equal %s' % req['cmd'] 
    assert req['id'] == 1000, 'cmd expect equal 1000, real equal %d' % req['id'] 
    assert req['info']['validator']['seed'] == 'ssssssss', 'seed was wrong'
    assert len(req['info']['ips_fixed']) == 2, 'numbers is wrong in ips_fixed'

def test_request():
    req = request('join', 1000)
    req['info'] = {}
    req['info']['nodeid'] = 0
    req['info']['rpc'] = {}
    req['info']['rpc']['port'] = 5005
    #print req.dumps()
    

def test_joinRequest():
    req = joinRequest(host='192.168.31.22', validated=True,id=10000)
    validator = {'validation_public_key':'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'}
    req.addValidator(validator)
    req.addRPC({'port':5005, 'ip':'0.0.0.0', 'admin':'127.0.0.1'})
    req.addPeer({'port':51235, 'ip':'0.0.0.0'})
    req.addWebsocket({'port':6006, 'ip':'0.0.0.0', 'admin':'127.0.0.1'})

    r = req.dumps()
    assert r['id'] == 10000, "id was wrong"
    assert r['command'] == 'join', "command was wrong"
    assert r['info'] != None , "info was wrong"
    assert r['info']['host'] == '192.168.31.22', "host was wrong"
    assert r['info']['validated'] == True, "validated was wrong"
    assert r['info']['rpc'] != None , "rpc was wrong"
    assert r['info']['rpc']['port'] == 5005, "rpc's port was wrong"
    assert r['info']['peer']['port'] == 51235, "peer's port was wrong"
    assert r['info']['ws']['port'] == 6006, "peer's port was wrong"

    def res_success():
        res = joinResponse(0, 1000)
        res.setNodeID(0)
        q = res.dumps()
        assert q['error_code'] == 0, "error_code was wrong"
        assert q['id'] == 1000, "id was wrong"
        assert q['result'] != None, 'result was wrong'
        assert q['result']['nodeid'] == 0, "nodeid was wrong"
        assert q['result']['command'] == 'join', "response's command was wrong"

    def res_failure():
        res = joinResponse(1, 1000)
        res.setErrorMsg('failure')
        q = res.dumps()
        assert q['error_code'] == 1, "error_code was wrong"
        assert q['id'] == 1000, "id was wrong"
        assert q['result'] != None, 'result was wrong'
        assert q['result']['command'] == 'join', "response's command was wrong"
        assert q['result']['error_msg'] == 'failure', 'error_msg was wrong'

    res_success()
    res_failure()

def test_startRequest():
    req = startRequest(10, 1000)
    r = req.dumps()
    assert r['id'] == 1000, "id was wrong"
    assert r['command'] == 'start', "command was wrong"
    assert r['info'] != None, "info was wrong"
    assert r['info']['nodeid'] == 10, "nodeid was wrong"

    def res_success():
        res = startResponse(0, 1000)
        res.add_ips_fixed(['172.16.18.2 51235', '172.16.18.3 51235'])
        res.add_validators(['111', '222'])

        q = res.dumps()
        assert q['error_code'] == 0, "error_code was wrong"
        assert q['id'] == 1000, "id was wrong"
        assert q['result'] != None, 'result was wrong'
        assert q['result']['command'] == 'start', "response's command was wrong"
        assert len(q['result']['ips_fixed']) == 2, 'ips_fixed was wrong'
        assert len(q['result']['validators']) == 2, 'validators was wrong'
        pass

    res_success()

def test_listRequest():
    res = listResponse(0, 10000)
    nodes = [
        {
            'id':0, 
            'host':'172.16.18.2',
            'rpc':5005,
            'ws':6006,
            'peer':51235,
            'pubkey': 'n9Jq6dyM2jbxspDu92qbiz4pq7zg8umnVCmNmEDGGyyJv9XchvVn'           
        }
    ]
    res.addNodes(nodes)

    q = res.dumps()
    assert q['error_code'] == 0, "error_code was wrong"
    assert q['id'] == 10000, "id was wrong"
    assert q['result'] != None, 'result was wrong'
    assert q['result']['command'] == 'list', "response's command was wrong"
    assert len(q['result']['nodes']) == 1, 'nodes was wrong'

def test_nodeInfo():
    req = nodeInfo(1000)
    info = {
        'nodeid': 1,
        'version': '1.0',
        'peers': '2',
        'uptime': '10000',
        'completes': 'true',
        'quorum': 2,
        'status': 'success'
    }
    req.addInfo(info)

    r = req.dumps()

    assert r['id'] == 1000, "id was wrong"
    assert r['command'] == 'nodeinfo', "command was wrong"
    assert r['info'] != None, "info was wrong"
    assert r['info']['nodeid'] == 1, "nodeid was wrong"

if __name__ == '__main__':
    try:
        test_request()
        test_jdata()
        test_joinRequest()
        test_startRequest()
        test_listRequest()
        test_nodeInfo()
    except Exception as e:
        print  'An error: %s' % e.message
