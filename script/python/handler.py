# coding=utf8

import request
import db

import json

class handler:
    def __init__(self, request):
        self.request = json.loads(request)
        self.command = self.request['command']
        self.id = None 
        if self.request.has_key('id'):
            self.id = self.request['id']

    def process(self):
        return None

    def __check__(self):
        return False