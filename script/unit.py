# coding=utf8

import os
import json
import time

def stop_chainsqled():
    #os.popen("ps -ef|grep chainsqld|grep -v grep|awk '{cmd=\"kill -9 \"$2;system(cmd)}'").read()
    try:
        while(True):
            output = os.popen('./chainsqld stop').read()
            jdata = json.loads(output)
            if 'error' in jdata:
                return True
            else:
                time.sleep(1)
    except:
        return False

def execute_chainsqld():
    os.popen('./chainsqld > /dev/null &').read()
    count = 1
    while(chainsqld_started() == False):
        if (++count) > 5:
            break
        time.sleep(1)


def chainsqld_started():
    try:
        output = os.popen('./chainsqld server_info').read()
        jdata = json.loads(output)
        if (jdata['result']['status']) == 'success':
            return True
        else:
            return False
    except:
        return False

def chainsqld_is_running():
    try:
        output = os.popen('./chainsqld server_info').read()
        jdata = json.loads(output)
        if (jdata['result']['complete_ledgers']) != 'empty':
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
        output = os.popen('./chainsqld validation_create').read()
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
