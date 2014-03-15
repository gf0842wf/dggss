# -*- coding: utf-8 -*-
# 压力测试

import gevent 
from gevent.pool import Pool
from gevent import socket

NOP = '\x00\x00\x00\x0f{"type": "NOP"}'
COUNT = 3000
HOST = "127.0.0.1"
PORT = 16000
    
def handler(sock, idx):
    while True:
        sock.send(NOP)
        gevent.sleep(5)
        nop = sock.recv(16)
        print idx, nop
        

def client(host, port, idx):
    s = socket.socket()
    s.connect((host, port))
    handler(s, idx)

pool = Pool(COUNT)

for i in xrange(COUNT):
    pool.spawn(client, HOST, PORT, i)

pool.join()
