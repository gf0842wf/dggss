# -*- coding: utf-8 -*-
import logging
import os
import sys

# 配置

HOME = os.path.dirname(__file__)

# 主服务器配置
MAIN_PORT = 16000
MAIN_TIMEOUT = 20
MAIN_RETRY_COUNT = 5

# 日志配置
LOG_LEVEL = logging.DEBUG
LOG_FILENAME = HOME + "/var/log/test.log"
LOG_FMT = "[%(asctime)s %(levelname)-7s %(module)s:%(funcName)s:%(lineno)s] %(message)s"
LOG_DATE_FMT = "%Y-%m-%d %X"
LOG_MAXBYTES = 20 * 1024 * 1024
LOG_BACKUPCOUNT = 10

# 其他配置
CONFIG_INTERVAL = 180 # 定时加载配置的时间间隔
CONFIG_MODULES = ["settings"] # 需要定时加载的模块

