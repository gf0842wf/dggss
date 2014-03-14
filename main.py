# -*- coding: utf-8 -*-

# 主循环

from gevent.server import StreamServer
from lib import log
from dggs.server import tcp_rloop
import settings
import sys
import gevent

def load_config():
    """定时重新加载配置文件
    """
    for module in settings.CONFIG_MODULES:
        try:
            module = sys.modules[module]
        except:
            continue
        reload(module)
        log.debug(u"加载配置文件")
        
        
if __name__ == "__main__":
    port = settings.MAIN_PORT
    if sys.platform == "linux2":
        import signal
        gevent.signal(signal.SIGQUIT, gevent.killall)
        log.error("sigquit, kill all")
    server = StreamServer(("0.0.0.0", port), tcp_rloop, spawn=5000)
    log.debug("start server port:%d", port)
    server.serve_forever()


