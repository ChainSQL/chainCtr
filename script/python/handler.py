# coding=utf8

import request
import db

import json

class announce:
    '''
    在处理一些请求的时候需要将相关的请求或是信息转发至
    其他的节点上
    '''
    def __init__(self):
        pass

    def emit(self, request):
        pass    

class handler:
    def __init__(self, request, db = None, announce = None):
        self.request = json.loads(request)
        self.db = db
        self.announce = announce
        self.command = self.request['command']
        self.id = None 
        if self.request.has_key('id'):
            self.id = self.request['id']

    def process(self):
        return None

    def __check__(self):
        return False