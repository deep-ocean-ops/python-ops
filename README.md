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
