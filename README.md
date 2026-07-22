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

## 仓库推送规范
# 同步推送到Gitee master分支
git push gitee master
# 同步推送到GitHub main分支（本地master映射远程main）
git push github master:main

### ✅ Day2 subprocess磁盘巡检告警
#### 实现功能
1. 使用subprocess.run调用df -h获取服务器磁盘信息
2. 内置超时保护、命令异常捕获
3. 阈值80%，超阈值终端红色告警，正常绿色输出
4. 自动生成格式化巡检报表 disk_report.txt
#### 新增文件
- basic/disk_check.py
