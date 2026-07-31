# MonitorClass.py Day11 面向对象封装监控类
import psutil
from alert_func import send_alert

class Monitor:
    def __init__(self, mem_threshold=80, disk_threshold=80):
        """
        构造函数：实例创建时自动执行
        :param mem_threshold: 内存告警阈值 默认80%
        :param disk_threshold: 磁盘告警阈值 默认80%
        """
        # 实例属性，每个实例独立拥有
        self.mem_threshold = mem_threshold
        self.disk_threshold = disk_threshold

    def get_memory_info(self):
        """实例方法：采集内存信息"""
        mem = psutil.virtual_memory()
        data = {
            "total": round(mem.total / 1024 / 1024 / 1024, 2),
            "used": round(mem.used / 1024 / 1024 / 1024, 2),
            "percent": mem.percent
        }
        # 阈值判断告警
        if data["percent"] >= self.mem_threshold:
            send_alert(f"内存使用率过高！当前：{data['percent']}%", level="error")
        else:
            send_alert(f"内存正常，使用率：{data['percent']}%", level="info")
        return data

    def get_disk_info(self):
        """实例方法：采集磁盘分区信息"""
        disk_result = []
        partitions = psutil.disk_partitions()
        for part in partitions:
            # 跳过只读、虚拟分区
            if "/dev" not in part.device:
                continue
            usage = psutil.disk_usage(part.mountpoint)
            info = {
                "mount": part.mountpoint,
                "total_gb": round(usage.total / 1024**3, 2),
                "used_gb": round(usage.used / 1024**3, 2),
                "percent": usage.percent
            }
            disk_result.append(info)
            # 磁盘告警判断
            if info["percent"] >= self.disk_threshold:
                send_alert(f"分区{info['mount']}磁盘使用率告警 {info['percent']}%", level="error")
        return disk_result

    def run_all_check(self):
        """统一入口：一键执行全部监控采集"""
        send_alert("===== 开始执行整机监控巡检 =====", level="info")
        mem_data = self.get_memory_info()
        disk_data = self.get_disk_info()
        return {"memory": mem_data, "disk": disk_data}


if __name__ == "__main__":
    # 1. 创建监控类实例，自定义阈值
    monitor = Monitor(mem_threshold=75, disk_threshold=85)
    # 2. 调用统一巡检方法
    result = monitor.run_all_check()

    # 打印原始采集数据
    print("\n====采集原始数据=====")
    print(result)

    # 演示：新建另一个实例，使用不同阈值，体现面向对象优势
    send_alert("\n===== 创建第二套监控实例（测试环境阈值） =====", level="info")
    test_monitor = Monitor(mem_threshold=90, disk_threshold=90)
    test_monitor.get_memory_info()
