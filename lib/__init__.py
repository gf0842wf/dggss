# -*- coding: utf-8 -*-
import logging
import settings
import gevent
from logging.handlers import RotatingFileHandler
from gevent import Timeout
from functools import partial


def named_any(name):
    """ 参照from twisted.python.reflect import namedAny
    @param name: The name of the object to return.
    @return: the Python object identified by 'name'.
    """
    names = name.split(".")
    if " " in names:
        raise ValueError("name has space character!")
    
    for i in xrange(len(names)):
        try:
            return __import__(".".join(names[i:]))
        except:
            continue
        
        raise ValueError("can't import!")
    
def _log():  
    log = logging.getLogger("main")
    log.setLevel(settings.LOG_LEVEL)
    handler = RotatingFileHandler(settings.LOG_FILENAME, maxBytes=settings.LOG_MAXBYTES, backupCount=settings.LOG_BACKUPCOUNT)
    formatter = logging.Formatter(settings.LOG_FMT, settings.LOG_DATE_FMT)
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log

log = _log()

class TimeoutMixin(object):
    """超时
    """
    def __init__(self, secs=None, exception=None, ref=True, priority=-1):
        self.secs = secs
        self.timeout = Timeout(secs)
        
    def stop_timeout(self):
        self.timeout.cancel()
        
    def reset_timeout(self):
        self.timeout.cancel()
        self.timeout = Timeout(self.secs, False)
        self.timeout.start()
        
    def start_timeout(self):
        self.timeout.start()

class LoopingCall(object):
    """定时调用
    """
    def __init__(self, f, *a, **kw):
        self.loop = gevent.get_hub().loop
        self.f = f
        self.a = a
        self.kw = kw
    
    def start(self, secs):
        self.timer = self.loop.timer(0.0, secs)
        func = partial(self.f, *self.a, **self.kw)
        self.timer.start(func)
        self.loop.run()
    
    def stop(self):
        self.timer.stop()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    
__all__ = ["named_any", "log", "TimeoutMixin", "LoopingCall"]