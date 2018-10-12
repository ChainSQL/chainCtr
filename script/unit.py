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
    result = []
    execute_chainsqld()
    for i in range(n):
        seed = generate_one_seed()
        result.append(seed)

    return result

def has_mysql():
    version = os.popen('mysql --version 2>/dev/null|awk \'{print $1}\'').read()
    if version == 'mysql':
        return True
    else:
        return False

def mysql_started(mysql):
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    pwd = None
    db = 'chainsql'
    if mysql.has_key('host'):
        host = mysql['host']
    if mysql.has_key('port'):
        port = mysql['port']
    if mysql.has_key('user'):
        user = mysql['user']
    if mysql.has_key('pwd'):
        pwd = mysql['port']
    if mysql.has_key('db'):
        db = mysql['db']

    mysql = 'mysql -u%s -h%s -P%s  -e \'select 1\' -p' %(user, host, port)
    version = os.popen(mysql).read()
    if len(version) == 0:
        print version
        return False
    else:
       return True

def node_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip
