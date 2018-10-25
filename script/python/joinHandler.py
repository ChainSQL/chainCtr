# coding=utf8

import json

from proto import request_pb2
import db

def handle_JoinRequest(request):
    assert request.type ==  request_pb2.Request.join, "miss type that is join"

    response = request_pb2.Response

    requestID = request.id
    response.id = requestID

    info = None
    if request.has_info():
        info = request.info()
        host = info.host
        print host, requestID
    
    return response

def test_success():
    r = request_pb2.Request
    r.type = request_pb2.Request.join
    r.id = 1000

    info = request_pb2.Info
    validator = request_pb2.Info.Validator()
    validator.public_key = 'xxxx'
    info.validator = validator
    r.info = info
    #r.info.validator.public_key = 'public key'
    #r.info.rpc.port = 5005
    #r.info.rpc.ip = '172.16.0.12'
    #r.info.rpc.admin = '127.0.0.1'

    #r.info.peer.port = 51235
    #r.info.peer.ip = '172.16.0.12'

    #r.info.ws.port = 6006
    #r.info.ws.ip = '172.16.0.12'
    #r.info.ws.admin = '127.0.0.1'

    print r.info.validator.public_key

if __name__ == '__main__':
    test_success()
    pass
