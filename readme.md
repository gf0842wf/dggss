## gevent tcp服务器模板 ## 
- dggs: dummy gevent game server

### 代码结构 ###
- 主循环 `main`
- 主要逻辑   `dggs/handler & server`
- 配置文件和日志 `settings & lib/__init__`
- 测试 `test`

### 部署监控 ###
- 部署 使用 supervisor
- 监控 使用 monit

### 数据备份 ###

### TODO ###
- 采用mongodb作为主数据库