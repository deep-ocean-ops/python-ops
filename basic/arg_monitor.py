# arg_monitor.py Day9 sys.argv 命令行传参动态筛选服务器
import sys
import os
from alert_func import send_alert

# 支持的合法环境列表
ALLOW_ENV = ["dev", "test", "prod"]

def check_argv():
    """校验命令行传入参数合法性"""
    # sys.argv[0] = 脚本文件名，真实参数从下标1开始
    # 要求必须传入2个外部参数：文件路径 + 环境
    if len(sys.argv) != 3:
        send_alert("参数数量错误！正确使用方式：python3 arg_monitor.py hosts.txt prod", level="error")
        send_alert(f"示例：python3 arg_monitor.py hosts.txt prod | 可选环境：{ALLOW_ENV}", level="info")
        sys.exit(1)  # 异常退出程序，返回非0状态码

    file_path = sys.argv[1]
    env_input = sys.argv[2]

    # 校验文件是否存在
    if not os.path.exists(file_path):
        send_alert(f"清单文件不存在：{file_path}", level="error")
        sys.exit(1)

    # 校验环境参数是否合法
    if env_input not in ALLOW_ENV:
        send_alert(f"环境参数非法！仅支持 {ALLOW_ENV}", level="error")
        sys.exit(1)
    
    return file_path, env_input

def load_host_file(file_path):
    """读取主机清单，构建嵌套字典分组（复用Day8结构）"""
    server_group = {
        "prod": [],
        "test": [],
        "dev": []
    }
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # 跳过空行、注释行
                if not line or line.startswith("#"):
                    continue
                # 文件格式：ip,user,room,biz,env
                ip, user, room, biz, env = line.split(",")
                host_info = {
                    "ip": ip,
                    "user": user,
                    "room": room,
                    "biz": biz
                }
                server_group[env].append(host_info)
    except Exception as e:
        send_alert(f"读取主机文件失败：{str(e)}", level="error")
        sys.exit(1)
    return server_group

def filter_target_env(group_data, target_env):
    """根据传入环境筛选主机"""
    target_hosts = group_data[target_env]
    send_alert(f"成功筛选【{target_env}】环境，共 {len(target_hosts)} 台主机", level="success")
    print("-" * 60)
    for host in target_hosts:
        print(f"IP:{host['ip']:12} 账号:{host['user']:6} 机房:{host['room']:8} 业务:{host['biz']}")
    print("-" * 60)
    return target_hosts

def export_env_report(host_list, env):
    """导出当前筛选环境的主机清单"""
    report_name = f"{env}_server_report.txt"
    report_path = os.path.join(os.getcwd(), report_name)
    try:
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"===== {env} 环境主机清单 =====\n")
            f.write(f"主机总数：{len(host_list)}\n\n")
            for host in host_list:
                f.write(f"{host['ip']} | {host['user']} | {host['room']} | {host['biz']}\n")
        send_alert(f"报表已导出：{report_path}", level="info")
    except PermissionError as e:
        send_alert(f"报表写入权限不足：{str(e)}", level="error")

if __name__ == "__main__":
    # 1. 校验命令行参数
    host_file, target_env = check_argv()
    # 2. 读取主机清单构建分组
    server_groups = load_host_file(host_file)
    # 3. 筛选目标环境主机并打印
    env_hosts = filter_target_env(server_groups, target_env)
    # 4. 导出对应环境报表
    export_env_report(env_hosts, target_env)
