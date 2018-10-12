# coding=utf8

import os
import json
import time
import socket

def stop_chainsqld():
    #os.popen("ps -ef|grep chainsqld|grep -v grep|awk '{cmd=\"kill -9 \"$2;system(cmd)}'").read()
    try:
        while(True):
            output = os.popen('./chainsqld stop 2>/dev/null').read()
            jdata = json.loads(output)
            if 'error' in jdata:
                return True
            else:
                time.sleep(1)
    except:
        return False

def execute_chainsqld():
    #os.popen('./chainsqld > /dev/null &').read()
    os.popen('./chainsqld 2>&1  &')
    count = 1
    while(chainsqld_started() == False):
        if (++count) > 5:
            break
        time.sleep(1)


def chainsqld_started():
    try:
        output = os.popen('./chainsqld server_info 2>/dev/null').read()
        jdata = json.loads(output)
        if (jdata['result']['status']) == 'success':
            return True
        else:
            return False
    except:
        return False

def chainsqld_is_running():
    try:
        output = os.popen('./chainsqld server_info 2>/dev/null').read()
        jdata = json.loads(output)
        if (jdata['result']['info']['complete_ledgers']) != 'empty':
            return True
        else:
            return False
    except:
        return False

def chainsqld_server_info():
    try:
        output = os.popen('./chainsqld server_info').read()
        jdata = json.loads(output)
        return jdata
    except:
        return None

def generate_one_seed():
    try:
        output = os.popen('./chainsqld validation_create 2>/dev/null').read()
        return output
    except:
        return None

def generate_seeds(n):
    print n
    result = []
    execute_chainsqld()
    for i in range(n):
        seed = generate_one_seed()
        result.append(seed)

    return result

def node_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip
