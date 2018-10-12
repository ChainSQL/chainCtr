# coding=utf8

import os
import socket
import asyncore
import SocketServer


class Echo(asyncore.dispatcher_with_send):
    def handle_close(self):
        self.close()
    def handle_read(self):
        print self.recv(8192)

class ServerHandler:
    def __init__(self):
        pass

    def dispatch(self, newClient):
        socket, addr = newClient
        Echo(socket)

class TCPServer(asyncore.dispatcher):

    def __init__(self, host, handler = ServerHandler()):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(host)
        self.listen(5)
        self.handler = handler

    def handle_accept(self):
        newClient = self.accept()
        if newClient is not None:
            sock, addr = newClient
            self.handler.dispatch(newClient)

    def run_forever(self):
        asyncore.loop()



if __name__ == '__main__':
    server = TCPServer(('0.0.0.0', 7670))
    print 'listen on 7670'
    server.run_forever()


