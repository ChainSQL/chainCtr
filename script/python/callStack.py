# coding=utf8

import inspect

def currentCallFrame():
    callerframerecord = inspect.stack()[1]  # 0 represents this line
    # 1 represents line at caller
    frame = callerframerecord[0]
    info = inspect.getframeinfo(frame)
    #print info.filename  # __FILE__ -> Test.py
    #print info.function  # __FUNCTION__ -> Main
    #print info.lineno  # __LINE__ -> 13
    return info.filename, info.function, info.lineno