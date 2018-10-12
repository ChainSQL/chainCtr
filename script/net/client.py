# coding=utf8

import os
import sys
import socket
import asyncore

def send(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()


class TCPClient(asyncore.dispatcher):

    def __init__(self, host, handler = None):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = host
        self.buffer = ''
        self.connect(host)
        self.handler = handler

    def handle_connect(self):
        #print 'connected %s:%d' % (self.address[0], self.address[1])
        pass

    def handle_close(self):
        print 'close to %s:%d' % (self.address[0], self.address[1])
        self.close()

    def handle_read(self):
        data = self.recv(8192)
        if self.handler == None:
            print 'from ', self.address
            print data
        else:
            self.handler(self.address, data)

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def sendmsg(self, data):
        self.buffer = data

    def loop(self):
        asyncore.loop()


if __name__ == '__main__':
    ip = sys.argv[1]
    port = int(sys.argv[2])
    message = None
    if sys.argv[3] == '-m':
        message = sys.argv[4]
    elif sys.argv[3] == '-f':
        with open(sys.argv[4]) as f:
            message = f.read()

    client = TCPClient((ip,port))
    client.sendmsg(message)
    client.loop()

