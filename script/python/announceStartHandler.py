# coding=utf8

import json

import request
import handler


class announceStartHandler(handler.handler):
    def __init__(self, request, announce = None):
        assert isinstance(announce, handler.announce), 'announce must be object of handler.announce'
        handler.handler.__init__(self, request, announce=announce)

    def __check__(self):
        if self.request.has_key('command') == False or self.request['command'] != 'announceStart':
            return False
        return True

    def process(self):
        res = None
        if self.__check__() == False:
            res = request.announceStartResponse(1000, self.id)
            res.setErrorMsg('check failure')
            return res

        #ips_fixed = self.request['info']['ips_fixed']
        #validators = self.request['info']['validators']

        # 启动 chainsqld 服务
        if self.announce != None:
            res = self.announce.emit(self.request)

        return res

class test_announce(handler.announce):
    def __init__(self, config):
        handler.announce.__init__(self)
        self.config = config

    def emit(self, req):
        ips_fixed = req['info']['ips_fixed']
        validators = req['info']['validators']

        ips_fixed = filter(lambda e: e != self.config['host'], ips_fixed)
        validators = filter(lambda e: e != self.config['public_key'], validators)

        print 'chainsql would be started with following params: '
        print ips_fixed
        print validators

        res = request.announceStartResponse(0, req['id'])
        res.started('success')
        return res

def test_announceStartHandler():
    announce = request.announceStartRequest(1000)
    announce.add_ips_fixed(['172.16.18.2 51235', '172.16.18.3 51235', '172.16.18.4 51235'])
    announce.add_validators(['pubkey1', 'pubkey2', 'pubkey3'])

    config = {}
    config['host'] = '172.16.18.2 51235'
    config['public_key'] = 'pubkey1'
    handler = announceStartHandler(json.dumps(announce.dumps()), test_announce(config))
    print handler.process().dumps()

if __name__ == '__main__':
    test_announceStartHandler()