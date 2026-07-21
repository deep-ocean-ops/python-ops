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
