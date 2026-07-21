# ssh_batch.py 批量服务器磁盘巡检
import paramiko
# 导入同目录工具函数
from host_list import get_host_list

# 方式1：标准写法（新手推荐，方便调试）
# 调用函数，读取配置文件，生成结构化主机列表
host_info_list = get_host_list()

# 循环遍历所有服务器，批量执行命令
for host in host_info_list:
    print(f"\n>>>>>>>>>> 正在连接服务器 {host['ip']} <<<<<<<<<<")
    # 创建SSH客户端对象
    ssh = paramiko.SSHClient()
    # 自动信任主机密钥
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 登录服务器（精准传入ip/用户名/密码，不会混淆）
    ssh.connect(
        hostname=host["ip"],
        username=host["username"],
        password=host["password"],
        timeout=5
    )
    # 执行磁盘查询命令
    stdin, stdout, stderr = ssh.exec_command("df -h")
    # 输出结果解码打印
    print("服务器磁盘信息：")
    print(stdout.read().decode())
    # 关闭连接
    ssh.close()

# 方式2：精简写法（省略中间变量，直接遍历函数返回值）
# for host in get_host_list():
#     执行SSH逻辑

