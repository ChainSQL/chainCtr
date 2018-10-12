# coding=utf8
import os

chainsql_cfg = 'chainsqld.cfg'
validators_cfg = 'validators.txt'

def get_line_number(key, file_path):
    grep = 'grep -n "' + key + '" ' + file_path
    line_num = os.popen(grep).read()
    if not line_num:
        return -1;
    else:
        vector = line_num.split(':')
        return int(vector[0])

def set_host(protocol, host):
    protocol = '\[%s\]' % protocol
    number = get_line_number(protocol, chainsql_cfg)
    vector = host.split(':')
    port = int(vector[1])
    ip = vector[0]

    if number != -1:
        # set port
        number += 1
        cmd = 'sed -i "%d c port = %s" %s' %(number, vector[1], chainsql_cfg)
        os.system(cmd)
        # set ip
        number += 1
        cmd = 'sed -i "%d c ip = %s" %s' %(number, vector[0], chainsql_cfg)
        os.system(cmd)

def set_admin_ip(protocol, ip):
    protocol = '\[%s\]' % protocol
    number = get_line_number(protocol, chainsql_cfg)
    if number != -1:
        number += 3
        cmd = 'sed -i "%d c admin = %s" %s' %(number, ip, chainsql_cfg)
        os.system(cmd)


def set_rpc_host(host='127.0.0.1:5005'):
    set_host('port_rpc_admin_local', host);

def set_peer_host(host='127.0.0.1:51235'):
    set_host('port_peer', host);

def set_ws_host(host='127.0.0.1:6006'):
    set_host('port_ws_admin_local', host);

def set_rpc_admin_ip(ip = '127.0.0.1'):
    set_admin_ip('port_rpc_admin_local', ip)

def set_ws_admin_ip(ip = '127.0.0.1'):
    set_admin_ip('port_ws_admin_local', ip)

def set_validation_public_key(key):
    number = get_line_number('\[validation_public_key\]', chainsql_cfg)
    if number == -1:
        os.system('sed -i "$ a \n" ' + chainsql_cfg)
        os.system('sed -i "$ a \[validation_public_key\]" ' + chainsql_cfg)
        os.system('sed -i "$ a ' + key + ' " ' + chainsql_cfg)
    else:
        number += 1
        cmd = 'sed -i "%d c %s" %s' %(number, key, chainsql_cfg)
        os.system(cmd)

def set_validation_seed(seed):
    number = get_line_number('\[validation_seed\]', chainsql_cfg)
    if number == -1:
        os.system('sed -i "$ a \n" ' + chainsql_cfg)
        os.system('sed -i "$ a \[validation_seed\]" ' + chainsql_cfg)
        os.system('sed -i "$ a ' + seed + ' " ' + chainsql_cfg)
    else:
        number += 1
        cmd = 'sed -i "%d c %s" %s' %(number, seed, chainsql_cfg)
        os.system(cmd)

def append_validators(validators):
    for v in validators:
        append_validator(v)
        #os.system('sed -i "$ a ' + v + ' " ' + validators_cfg)

def append_validator(validator):
    os.system('sed -i "$ a ' + validator + ' " ' + validators_cfg)

def append_ips_fixed(ips):
    number = get_line_number('\[ips_fixed\]', chainsql_cfg)
    if number == -1:
        os.system('sed -i "$ a \n" ' + chainsql_cfg)
        os.system('sed -i "$ a \[ips_fixed\]" ' + chainsql_cfg)
        for ip in ips:
            os.system('sed -i "$ a ' + ip + ' " ' + chainsql_cfg)
    else:
        number += 1
        for ip in ips:
            cmd = 'sed -i "%d i %s" %s' %(number, ip, chainsql_cfg)
            os.system(cmd)
            number += 1

def append_ip_fixed(ip):
    number = get_line_number('\[ips_fixed\]', chainsql_cfg)
    if number == -1:
        os.system('sed -i "$ a \n" ' + chainsql_cfg)
        os.system('sed -i "$ a \[ips_fixed\]" ' + chainsql_cfg)
        os.system('sed -i "$ a ' + ip + ' " ' + chainsql_cfg)
    else:
        number += 1
        cmd = 'sed -i "%d i %s" %s' %(number, ip, chainsql_cfg)
        os.system(cmd)


def set_mysql(entry):
    def subcmd(value):
        index = get_line_number(value, chainsql_cfg)
        if index == -1:
            return 'i'
        else:
            return 'c'

    index = get_line_number('\[sync_db\]', chainsql_cfg)
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    passwd = '3.16'
    db = 'chainsqld'
    charset = 'utf8'
    if index != -1:
        # replace type
        index += 1
        cmd = 'sed -i "%d c type=mysql" %s' %(index, chainsql_cfg)
        os.system(cmd)
        # set host
        index += 1
        if entry.has_key('host'):
            host = entry['host']
        cmd = 'sed -i "%d %s host=%s" %s' %(index, subcmd('host='), host, chainsql_cfg)
        os.system(cmd)
        # set port
        index += 1
        if entry.has_key('port'):
            port = entry['port']
        cmd = 'sed -i "%d %s port=%d" %s' %(index, subcmd('port='), port, chainsql_cfg)
        os.system(cmd)
        # set user
        index += 1
        if entry.has_key('user'):
            user = entry['user']
        cmd = 'sed -i "%d %s user=%s" %s' %(index, subcmd('user='), user, chainsql_cfg)
        os.system(cmd)
        # set pwd
        index += 1
        if entry.has_key('passwd'):
            passwd = entry['passwd']
        cmd = 'sed -i "%d %s pass=%s" %s' %(index, subcmd('pass=') ,passwd, chainsql_cfg)
        os.system(cmd)
        # set db
        index += 1
        if entry.has_key('db'):
            db = entry['db']
        cmd = 'sed -i "%d %s db=%s" %s' %(index, subcmd('db='), db, chainsql_cfg)
        os.system(cmd)
        # set charset
        index += 1
        if entry.has_key('charset'):
            charset = entry['charset']
        cmd = 'sed -i "%d %s charset=%s" %s' %(index, subcmd('charset='), charset, chainsql_cfg)
        os.system(cmd)

