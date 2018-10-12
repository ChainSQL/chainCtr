# coding=utf8

import os
import sys
import signal
import socket
import asyncore
import time
import json
import threading

import message

#import net.service as service
from net.service import *

clients = {}
ips_fixed = []
validation_public_keys = []
deploy_normal_network = False

class client(asyncore.dispatcher_with_send):
    __host = None
    __buffer = ''
    def handle_close(self):
        if self.__host is not None:
            if self.__host in clients:
                del clients[self.__host]
        self.close()
        print 'close %s ' % self.__host

    def handle_read(self):
        global ips_fixed
        global validation_public_keys
        global deploy_normal_network
        data = self.recv(8192)
        try:
            jdata = json.loads(data)
            if jdata['cmd'] == 'join':

                if jdata.has_key('conf') \
                    and jdata['conf'].has_key('port_peer') \
                    and jdata['conf']['port_peer'].has_key('port'):
                    ips_fixed.append('%s:%d' %(self.__host.split(':')[0], jdata['conf']['port_peer']['port']))

                if jdata.has_key('conf') \
                    and jdata['conf'].has_key('validation') \
                    and jdata['conf']['validation'].has_key('validation_public_key'):
                    validation_public_keys.append(jdata['conf']['validation']['validation_public_key'])

                self.send(message.success('join'))

            elif jdata['cmd'] == 'start':
                del clients[self.__host]
                deploy_normal_network = True
                self.send(message.success('start'))
        except ValueError as e:
            print 'Handle read data failure. %s' % e
            print data
            self.send(message.failure(e))
        except keyError as e:
            print 'Handle read data failure. %s' % e
            print data
            self.send(message.failure(e))

    def set_host(self, host):
        self.__host = host

    def sendmsg(self, msg):
        self.send(msg)

class initNormalNetWorkHandler:
    def __init__(self):
        pass

    def dispatch(self, newClient):
        socket, addr = newClient
        print 'A new client come from %s' % repr(addr)
        c = client(socket)
        key = '%s:%d' % (addr[0], addr[1])
        c.set_host(key)
        clients[key] = c


def handler_signal(signum, frame):
    if signum == signal.SIGINT:
        sys.exit(0)

class worker(threading.Thread):

    def __init__(self, name = 'worker_thread'):
        self._stopevent = threading.Event()
        self._sleepperiod = 0.1
        threading.Thread.__init__(self, name = name)

    def run(self):
        global ips_fixed
        global validation_public_keys
        global deploy_normal_network
        while not self._stopevent.isSet():
            if deploy_normal_network == True:
                for key, client in clients.iteritems():
                    ip = key.split(':')[0]
                    ips = filter(lambda e: e.find(ip) == -1, ips_fixed)
                    deployCmd = message.deployRequest(ips, validation_public_keys)
                    client.sendmsg(deployCmd)
                deploy_normal_network = False
            self._stopevent.wait(self._sleepperiod)

        print '%s ends' % self.getName()


    def join(self, timeout = None):
        self._stopevent.set()
        threading.Thread.join(self, timeout)

def init_normal_network(listen_tcp_port = 7670):
    signal.signal(signal.SIGINT, handler_signal)
    server = TCPServer(('0.0.0.0', listen_tcp_port), initNormalNetWorkHandler())
    w = worker()
    w.start()

    print 'listen on %d' % listen_tcp_port

    server.run_forever()
    w.join()



def test():
    init_normal_network()

if __name__ == '__main__':
    test()
