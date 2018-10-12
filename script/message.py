# coding=utf8
import json

def joinRequest(hostid, config):
    request = """
    {
        "cmd":"join",
        "node": {
            "validate":true,
            "hostid":"%s"
        },
        "conf":%s
    }
    """
    request = request % (hostid, config)
    return request

def startRequest(hostid):
    request = """
    {
        "cmd":"start",
        "node": {
            "validate":true,
            "hostid":"%s"
        }
    }
    """
    return request % hostid

def deployRequest(ips, public_keys):
    request = {}
    request['cmd'] = 'deploy'
    request['conf'] = {}
    request['conf']['ips_fixed'] = ips
    request['conf']['validators'] = public_keys
    return json.dumps(request)


def success(cmd):
    response = """
    {
        "status":"success",
        "result": {
            "cmd":"%s"
        }
    }
    """
    return response % cmd

def failure(error):
    response = """
    {
        "status":"failure",
        "result": {
            "error": "%s"
        }
    }
    """
    return response % error
