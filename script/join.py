# coding=utf8

import os
import sys
import signal
import socket
import asyncore
import time
import json

from net.client import *
import unit
import config
import message

class setting:

    def __init__(self):
        self.__sets = {}

        self.__add('port_rpc_admin_local', {
            'port':5005,
            'ip':'0.0.0.0',
            'admin':'0.0.0.0'
        })

        self.__add('port_peer', {
            'port':5125,
            'ip':'0.0.0.0'
        })

        self.__add('port_ws_admin_local', {
            'port':6006,
            'ip':'0.0.0.0'
        })

    def __add(self, key, value):
        self.__sets[key] = value
        return self.__sets

    def add_validation(self, seed):
        validation = {}
        validation['validation_public_key'] = seed['result']['validation_public_key']
        validation['validation_seed'] = seed['result']['validation_seed']
        self.__add('validation', validation)
        return self.__sets['validation']

    def dumps(self):
        return json.dumps(self.__sets)

def handler_signal(signum, frame):
    if signum == signal.SIGINT:
        sys.exit(0)

def deploy_local_chainsqld():
    pwd = os.getcwd()
    if(os.path.exists('/var/local/peersafe')):
        os.system('rm -rf /var/local/peersafe')

    # copy chainsql and config
    path = '/var/local/peersafe/chainsqld'
    mkdir = 'mkdir -p %s' % path
    os.system(mkdir)

    cp_chainsqld = 'cp %s/bin/chainsqld %s/' % (pwd, path)
    #print cp_chainsqld
    os.system(cp_chainsqld)

    cp_cfg = 'cp %s/config/chainsqld.cfg %s/' % (pwd, path)
    #print cp_cfg
    os.system(cp_cfg)

    cp_validators = 'cp %s/config/validators.txt %s/' % (pwd, path)
    #print cp_validators
    os.system(cp_validators)


def TCPClientHandler(source, data):
    def handle_response(jdata):
        if jdata['status'] == 'success' and jdata['result']['cmd'] == 'join':
            print 'joined to %s:%d successfully.' % (source[0], source[1])

    def handle_command(jdata):
        pwd = os.getcwd()
        if jdata['cmd'] == 'deploy':
            if unit.chainsqld_is_running() == False:
                ips_fixed = jdata['conf']['ips_fixed']
                validators = jdata['conf']['validators']

                path = '/var/local/peersafe/chainsqld'
                os.chdir(path)
                for ip in ips_fixed:
                    config.append_ip_fixed(ip)
                config.append_validators(validators)

                print 'chainsqld is starting'
                unit.execute_chainsqld()
                while unit.chainsqld_is_running() == False:
                    time.sleep(1)
                print 'chainsqld has started completely.'
        elif jdata['cmd'] == 'stop':
            if unit.chainsqld_is_running() == True:
                path = '/var/local/peersafe/chainsqld'
                os.chdir(path)
                print 'chainsqld is stopping'
                unit.stop_chainsqld()
                print 'chainsqld has stopped completely.'

        os.chdir(pwd)

    try:
        jdata = json.loads(data)
        if jdata.has_key('status'):
            handle_response(jdata)
        elif jdata.has_key('cmd'):
            handle_command(jdata)

    except ValueError as e:
        print e
        sys.exit(1)
    except keyError as e:
        print e
        sys.exit(1)

def join(host):
    pwd = os.getcwd()
    signal.signal(signal.SIGINT, handler_signal)
    path = '/var/local/peersafe/chainsqld'
    defaultCfg = setting()
    if os.path.exists(path) == False:
        os.chdir('%s/bin' % pwd)
        config.set_rpc_host('127.0.0.1:5005')
        unit.execute_chainsqld()
        seed = json.loads(unit.generate_one_seed())
        unit.stop_chainsqld()
        os.chdir(pwd)
        deploy_local_chainsqld()
        # set default configuration
        os.chdir(path)
        config.set_rpc_host('0.0.0.0:5005')
        config.set_peer_host('0.0.0.0:5125')
        config.set_ws_host('0.0.0.0:6006')
        config.set_validation_public_key(seed['result']['validation_public_key'])
        config.set_validation_seed(seed['result']['validation_seed'])

        defaultCfg.add_validation(seed)

    os.chdir(pwd)
    os.system('echo %s:%d > master' % (host[0], host[1]))
    client = TCPClient(host, TCPClientHandler)
    request = message.joinRequest('chainSQL', defaultCfg.dumps())
    client.sendmsg(request)
    client.loop()


def start():
    try:
        host = os.popen('cat master').read().split(':')
        request = message.startRequest('chainSQL')
        send(host[0], int(host[1]), request)
    except IndexError as e:
        print 'please join network firstly.'

def stop():
    try:
        host = os.popen('cat master').read().split(':')
        request = message.stopRequest()
        send(host[0], int(host[1]), request)
    except IndexError as e:
        print 'please join network firstly.'

if __name__ == '__main__':
    sets = setting()

    seed = {}
    seed['result'] = {}
    seed['result']['validation_public_key'] = 'pnFb5pCgU6fK2RQKcoeGZ63MgGvf2et4ZC1fCjDRaedN33uadyb'
    seed['result']['validation_seed'] = 'xcE5y2x74oTd5k6SU3VJSQ8oYPgko'
    sets.add_validation(seed)

    print json.loads(sets.dumps())











