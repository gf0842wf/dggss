# -*- coding: utf-8 -*-

# 共享对象

from weakref import WeakValueDictionary, WeakKeyDictionary
from lib import named_any

# 所有 userid:client
id2cli = WeakValueDictionary()
# 所有 client:userid
cli2id = WeakKeyDictionary

tcp_handle = named_any("dggs.handlers.tcp_handler")

__all__ = ["tcp_handle", "id2cli", "cli2id"]