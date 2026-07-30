# python-ops 运维自动化脚本库
## 目录说明
- basic：Python基础运维脚本（文件IO、yaml/json、正则、子进程）
- lib：封装好的工具库（SSH、资源采集、命令行、Excel导出）
- project：完整成品项目——多线程批量服务器巡检工具
- shell-ops：工程化可复用Shell脚本（awk/sed/定时任务/日志模板）

## 环境依赖
```bash
yum install python3 python3-pip -y
pip3 install pyyaml paramiko psutil click openpyxl
```

## 学习进度
### ✅ Day1 文件IO + os模块 + 批量SSH实战
#### 实现功能
1. basic/hosts.txt：统一存放服务器IP、账号、密码，支持#注释、空行排版
2. basic/host_list.py：封装get_host_list()读取函数，自动过滤无效行，返回结构化主机字典列表
3. basic/ssh_batch.py：导入读取函数，循环批量ssh登录服务器执行磁盘df -h巡检
#### 本次新增文件
- basic/hosts.txt
- basic/host_list.py
- basic/ssh_batch.py


### ✅ Day2 subprocess磁盘巡检告警
#### 实现功能
1. 使用subprocess.run调用df -h获取服务器磁盘信息
2. 内置超时保护、命令异常捕获
3. 阈值80%，超阈值终端红色告警，正常绿色输出
4. 自动生成格式化巡检报表 disk_report.txt
#### 新增文件
- basic/disk_check.py

### ✅ Day3 psutil本地资源采集 + JSON持久化存储
#### 实现功能
1. psutil库无shell调用采集CPU、内存、磁盘全量指标
2. 自动过滤tmpfs临时磁盘分区，只保留物理磁盘
3. json.dump 将监控数据序列化存入 metric.json 持久化
4. json.load 读取本地监控文件，格式化打印资源报表
5. 自动换算内存/磁盘GB单位，增加采集时间戳
#### 新增文件
- basic/local_metric.py
- basic/metric.json（程序自动生成，无需手动创建）

### ✅ Day4 re正则 日志错误过滤与统计
#### 实现功能
1. 内置re正则模块读取日志，匹配 error/fail/500 错误关键字
2. 自动过滤空行，统计全部错误日志总行数
3. 正则分组提取错误类型，字典统计每种错误出现频次
4. 按频次倒序输出Top10高频错误排行
5. 完整打印所有原始错误日志，便于问题排查
#### 新增文件
- basic/log_analysis.py
- basic/app.log（测试日志文件）

### ✅ Day5 PyYAML 读写批量生成K8s Namespace资源
#### 实现功能
1. PyYAML模块safe_load读取配置ns_list.yaml，统一管理多环境命名空间
2. 内置K8s v1标准Namespace模板，批量生成独立资源yaml
3. 自动创建输出目录，每个namespace单独生成清单文件
4. safe_dump输出标准格式化K8s yaml，字段顺序符合集群规范，直接kubectl apply部署
#### 新增文件
- basic/k8s_ns_create.py
- basic/ns_list.yaml

### ✅ Day6 统一告警工具函数封装
#### 实现功能
1. 封装通用send_alert告警函数，支持4种等级：info/success/warn/error
2. 终端分级彩色输出，自动记录告警日志到alert_record.log
3. 支持默认参数控制是否持久化日志，灵活调试
4. 全局统一颜色常量，所有历史脚本可导入复用，消除重复打印代码
5. 统一告警入口，后续扩展邮件/钉钉告警仅修改本文件即可
#### 新增文件
- basic/alert_func.py

### ✅ Day7 try-except 异常处理 脚本容错加固
#### 实现功能
1. 改造Day2磁盘巡检脚本，全链路多层try-except异常捕获
2. 精准捕获：命令超时、权限不足、文件读写失败、数据格式解析错误
3. 自定义业务异常：磁盘命令异常、磁盘数据解析异常，区分故障类型
4. 错误信息单独持久化到 error.log，和普通业务日志隔离
5. 顶层全局异常兜底，防止脚本直接崩溃退出
6. 复用Day6统一告警函数，异常终端红色提示
#### 新增文件
- basic/safe_monitor.py

### ✅ Day8 列表/字典高阶：服务器分组管理
#### 实现功能
1. 嵌套字典存储多环境服务器分组（dev/test/prod），单台主机存储IP/账号/机房/业务标签
2. 两种筛选方案：列表推导式、filter高阶函数过滤生产环境主机
3. 打印全环境分组报表 + 单独生产环境明细报表
4. 自动导出生产服务器清单 prod_server_list.txt
5. 复用Day6统一告警函数输出分级提示，增加文件写入异常捕获
#### 新增文件
- basic/host_group.py
#### 自动生成（gitignore忽略）
- basic/prod_server_list.txt

### ✅ Day9 sys.argv 命令行传参：脚本动态入参
#### 实现功能
1. 使用sys.argv接收命令行双参数：主机清单文件 + 目标环境
2. 多层参数校验：参数数量、文件存在性、环境合法性拦截错误
3. 读取hosts.txt构建多环境服务器分组，根据传入环境动态筛选
4. 打印目标环境主机明细，自动生成对应环境独立报表
5. 复用Day6告警工具，异常友好提示，错误状态码退出
#### 使用示例
python3 arg_monitor.py hosts.txt prod
python3 arg_monitor.py hosts.txt test
#### 新增文件
- basic/arg_monitor.py
- basic/hosts.txt
#### 自动生成（gitignore忽略）
- basic/dev_server_report.txt / test_server_report.txt / prod_server_report.txt

### ✅ Day10 循环进阶：批量生成测试日志文件
#### 实现功能
1. for + range 循环批量生成指定行数模拟业务日志
2. 70%正常日志 / 30%错误日志，包含error、500、fail关键字
3. 随机生成时间戳、耗时、任务ID，贴近真实应用日志格式
4. 支持命令行传参自定义日志条数，默认生成100行
5. 附带while循环示例，对比两种循环使用场景
6. 产出app_sim.log，作为日志分析脚本标准测试数据源
#### 使用示例
python3 gen_log.py       # 默认100行
python3 gen_log.py 200   # 自定义200行日志
#### 新增文件
- basic/gen_log.py
#### gitignore忽略文件
- basic/app_sim.log
