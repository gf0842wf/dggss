# -*- coding: utf-8 -*-

# 这里放TCP,UDP,WEB等handlers
# 基本协议格式如下:
# length + json({'type':'LOGIN', 'userid':'fk', 'password':'112358'})

from lib import log, TimeoutMixin, LoopingCall
from share import id2cli, cli2id
from gevent import Timeout
import json
import struct
import settings

MAX_SELNO = 10000

class TCPProtocol(object):
    def __init__(self, sock, addr):
        self.sock = sock
        self.addr = addr
        self.status = 0 # 0 - 未登录, 1 - 登陆, 2 - 退出
        self.userid = ""
        self.selno = 0
        self.media = 0 # 0 - 不是媒体, 1 - 是媒体文件
        # connection_made
    
    def encode(self, data):
        log.debug(data)
        jdata = json.dumps(data)
        return chr(len(jdata)) + jdata
    
    def send(self, data):
        self.sock.send(data)
    
    def data_received(self, ctx):
        if self.media == 1:
            data = ctx
            type_ = "MEDIA"
        else:
            data = json.loads(ctx)
            type_ = data.pop("type")
        handle = getattr(self, "handle_%s" % type_)
        if handle:
            resp = handle(data)
            if resp:
                self.message_received(resp)
        else:
            log.warning("unknown cmd")
    
    def message_received(self, resp):
        data = self.encode(resp)
        self.send(data)
        
    def handle_LOGIN(self, data):
        """登陆
        """
        userid = data["userid"]
        password = data["password"]
        # TODO: 验证
        # 验证成功 建立映射
        if True:
            self.status = 1
            self.userid = userid
            id2cli[userid] = self
            cli2id[self] = userid
            resp = {"type":"LOGIN", "result":0, "message":"login ok"}
        # 验证失败
        else:
            self.status = 0
            resp = {"type":"LOGIN", "result":1, "message":"login failed"}
        return resp
    
    def handle_NOP(self, data):
        """心跳
        '\x00\x00\x00\x0f{"type": "NOP"}'
        """
        resp = {"type":"NOP"}
        return resp
    
    def handle_MEDIASTART(self, data):
        """媒体发送准备
        - 把文件名发送给客户端
        @data: {"type":"MEDIASTART", "name":"jpg"}
        @return {{"type":"MEDIASTART", "name":"0.jpg"}}
        """
        self.media = 1
        self.media_name = "%d.%s" % (self.selno % MAX_SELNO, data["name"])
        self.store_name = "%s/var/media/%s" % (settings.HOME, self.media_name)
        self.selno += 1
        resp = {"type":"MEDIASTART", "name":self.media_name}
        return resp
    
    def handle_MEDIA(self, data):
        """媒体文件存档
        """
        def store():
            open(self.store_name, "wb").write(data)
        store()
        self.media = 0
    
    def handle_DEVUP(self, data):
        """通用消息上行(客户端发给服务器),
        - 如果含有媒体文件,要先发一个媒体准备消息
        - 媒体数据先上传,再上传本消息
        """
        message = data["message"]
        sub_type = data["sub_type"] # 0 - 文字, 1 - 文字 + 媒体文件
        if sub_type == 1:
            media_name = data["media_name"]
            store_name = "%s/%s" % (settings.HOME, media_name)
            # TODO: message消息入库, media文件路径(store_name)入库
        else:
            # TODO: message消息入库
            pass
#             gevent.spawn(write).join()
            
    def handle_BROADCAST(self, data):
        """广播消息
        - 如果消息含有媒体文件,同上,下同
        """
        message = data["message"]
        log.debug("broadcast:%s", message)
        for cli in id2cli.values():
            cli.send(message)
    
    def handle_C2C(self, data):
        """客户端发给客户端的消息
        """
        dst_id = data["dst"]
        dst_cli = id2cli.get(dst_id)
        message = data["message"]
        log.debug("c2c:%s", message)
        if dst_cli:
            dst_cli.send(message)
        else:
            # TODO: 对方不在线,存库
            pass
        
    def handle_C2CS(self, data):
        """群发,非广播
        """
        message = data["message"]
        userids = data["clients"]
        log.debug("c2cs:%s", message)
        clis = [id2cli.get(userid) for userid in userids]
        for cli in clis:
            cli.send(message)

def tcp_rloop(sock, addr):
    log.debug("%r connected", addr)
    protocol = TCPProtocol(sock, addr)
    timeout = TimeoutMixin(settings.MAIN_TIMEOUT)
    timeout.start_timeout()
    def loop():
        _buf = ""
        while True:
            try:
                _buf = sock.recv(4)
                if not _buf:
                    continue
                len_, = struct.unpack(">I", _buf[:4])
                _buf = _buf[4:]
                while True:
                    _buf += sock.recv(512)
                    if len(_buf) >= len_:
                        break
                ctx = _buf[:len_]
                _buf = _buf[len_:]
                timeout.reset_timeout()
                protocol.data_received(ctx)
            except Timeout:
                log.warning("%r disconnect timeout", addr)
                sock.close()
                break
#             except Exception as e:
#                 log.error("%r disconnect error:%s", *(addr, repr(e)))
#                 sock.close()
#                 break
    loop()