# -*- coding: utf-8 -*-
import socket
import json
import struct

sock = socket.socket()
sock.connect(("127.0.0.1", 16000))

# 图片发送测试
# 第一幅
msg_mediastart = json.dumps({"type":"MEDIASTART", "name":"jpg"})
data_mediastart = struct.pack(">I", len(msg_mediastart)) + msg_mediastart
sock.send(data_mediastart)
msg_media = open("test.jpg", "rb").read()
print len(msg_media)
data_media = struct.pack(">I", len(msg_media)) + msg_media

print sock.send(data_media)
print sock.recv(1024)

  

sock.close()
