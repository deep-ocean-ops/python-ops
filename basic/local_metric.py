# local_metric.py Day3 psutil采集CPU/内存/磁盘 + JSON读写
import psutil
import json
import os
from datetime import datetime

# 配置文件路径
JSON_FILE = os.path.join(os.getcwd(), "metric.json")

def get_system_metric():
    """采集本机CPU、内存、磁盘指标，返回结构化字典"""
    # 1. CPU采集
    cpu_percent = psutil.cpu_percent(interval=1)  # 1秒采样CPU使用率
    cpu_core = psutil.cpu_count(logical=True)     # 逻辑核心数

    # 2. 内存采集
    mem = psutil.virtual_memory()
    mem_total = round(mem.total / 1024 / 1024 / 1024, 2)    # 总内存GB
    mem_used = round(mem.used / 1024 / 1024 / 1024, 2)      # 已用内存GB
    mem_percent = mem.percent

    # 3. 磁盘采集（只过滤物理挂载盘，跳过tmp临时分区）
    disk_list = []
    disk_partitions = psutil.disk_partitions()
    for part in disk_partitions:
        # 过滤临时文件系统
        if "tmpfs" in part.fstype or "loop" in part.fstype:
            continue
        disk_usage = psutil.disk_usage(part.mountpoint)
        disk_info = {
            "mount": part.mountpoint,
            "total_gb": round(disk_usage.total / 1024 / 1024 / 1024, 2),
            "used_gb": round(disk_usage.used / 1024 / 1024 / 1024, 2),
            "use_percent": disk_usage.percent
        }
        disk_list.append(disk_info)

    # 整合所有指标，增加采集时间戳
    metric_data = {
        "collect_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu": {
            "logic_core": cpu_core,
            "usage_percent": cpu_percent
        },
        "memory": {
            "total_gb": mem_total,
            "used_gb": mem_used,
            "usage_percent": mem_percent
        },
        "disk": disk_list
    }
    return metric_data

def save_to_json(data):
    """将采集到的监控数据写入metric.json持久化"""
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        # indent=2 格式化json，方便人阅读
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"监控数据已写入文件：{JSON_FILE}")

def load_json_report():
    """读取metric.json文件，格式化打印监控报表"""
    if not os.path.exists(JSON_FILE):
        print("错误：metric.json监控文件不存在，请先执行采集！")
        return

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        metric = json.load(f)

    # 格式化打印报表
    print("=" * 50)
    print(f"【服务器资源监控报表】采集时间：{metric['collect_time']}")
    print("=" * 50)
    print(f"CPU信息：逻辑核心数 {metric['cpu']['logic_core']} | 当前使用率 {metric['cpu']['usage_percent']}%")
    print("-" * 50)
    print(f"内存信息：总内存 {metric['memory']['total_gb']}GB | 已用 {metric['memory']['used_gb']}GB | 使用率 {metric['memory']['usage_percent']}%")
    print("-" * 50)
    print("磁盘分区使用详情：")
    for disk in metric["disk"]:
        print(f"挂载点：{disk['mount']:12} 总容量：{disk['total_gb']:5}GB 已用：{disk['used_gb']:5}GB 使用率：{disk['use_percent']}%")
    print("=" * 50)

if __name__ == "__main__":
    # 1. 采集系统指标
    metric_info = get_system_metric()
    # 2. 保存到JSON文件
    save_to_json(metric_info)
    # 3. 读取JSON并打印完整报表
    load_json_report()
