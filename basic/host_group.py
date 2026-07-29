# host_group.py Day8 字典嵌套/列表推导式/filter 服务器分组管理
from alert_func import send_alert
import os

# 1. 嵌套字典：多环境服务器分组数据源（生产/测试/开发）
server_group = {
    "prod": [
        {"ip": "10.0.1.10", "user": "root", "room": "A机房", "biz": "订单服务"},
        {"ip": "10.0.1.11", "user": "root", "room": "A机房", "biz": "支付服务"},
        {"ip": "10.0.1.12", "user": "ops", "room": "B机房", "biz": "监控服务"},
    ],
    "test": [
        {"ip": "10.0.2.20", "user": "test", "room": "测试机房", "biz": "预发布验证"},
        {"ip": "10.0.2.21", "user": "test", "room": "测试机房", "biz": "接口测试"},
    ],
    "dev": [
        {"ip": "10.0.3.30", "user": "dev", "room": "开发机房", "biz": "本地调试"},
    ]
}

PROD_REPORT = os.path.join(os.getcwd(), "prod_server_list.txt")

def filter_prod_by_list_comprehension(group_data):
    """方式1：列表推导式筛选生产环境主机（运维最常用）"""
    prod_hosts = [host for env, host_list in group_data.items() if env == "prod" for host in host_list]
    return prod_hosts

def filter_prod_by_filter_func(group_data):
    """方式2：filter高阶函数筛选生产环境主机"""
    all_env_items = filter(lambda x: x[0] == "prod", group_data.items())
    prod_hosts = []
    for env_name, host_list in all_env_items:
        prod_hosts.extend(host_list)
    return prod_hosts

def print_all_group_report(group_data):
    """打印全环境分组总报表"""
    send_alert("===== 全服务器分组总报表 =====", level="info")
    for env, host_list in group_data.items():
        send_alert(f"\n【环境：{env} 共{len(host_list)}台主机】", level="info")
        for host in host_list:
            print(f"IP:{host['ip']:12} 账号:{host['user']:6} 机房:{host['room']:8} 业务:{host['biz']}")

def export_prod_report(prod_hosts):
    """导出生产主机清单到文本文件"""
    try:
        with open(PROD_REPORT, "w", encoding="utf-8") as f:
            f.write("===== 生产环境服务器清单 =====\n")
            f.write(f"总计机器数量：{len(prod_hosts)}\n\n")
            for host in prod_hosts:
                line = f"IP:{host['ip']} | 登录账号:{host['user']} | 机房:{host['room']} | 业务:{host['biz']}\n"
                f.write(line)
        send_alert(f"生产服务器清单已导出至 {PROD_REPORT}", level="success")
    except PermissionError as e:
        send_alert(f"导出文件权限不足：{str(e)}", level="error")

if __name__ == "__main__":
    # 1. 打印全部分组
    print_all_group_report(server_group)

    # 2. 两种方式筛选生产主机（效果完全一致）
    prod_list1 = filter_prod_by_list_comprehension(server_group)
    prod_list2 = filter_prod_by_filter_func(server_group)

    send_alert(f"\n列表推导式筛选生产主机数量：{len(prod_list1)}", level="info")
    send_alert(f"filter函数筛选生产主机数量：{len(prod_list2)}", level="info")

    # 3. 打印生产环境单独报表
    send_alert("\n===== 生产环境主机明细 =====", level="warn")
    for host in prod_list1:
        print(f"生产IP:{host['ip']:12} 业务:{host['biz']}")

    # 4. 导出生产主机清单文件
    export_prod_report(prod_list1)
