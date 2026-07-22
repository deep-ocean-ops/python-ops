# disk_check.py Day2 subprocess磁盘使用率巡检告警
import subprocess
import os

# 1. 配置常量
WARN_THRESHOLD = 80  # 磁盘告警阈值80%
REPORT_FILE = os.path.join(os.getcwd(), "disk_report.txt")  # 报表文件路径

# 2. ANSI终端颜色定义
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

def get_disk_info():
    """执行df -h命令，清洗输出，返回磁盘列表"""
    # 执行df -h命令，捕获输出，超时5秒
    cmd_result = subprocess.run(
        ["df", "-h"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        timeout=5
    )
    # 命令执行失败直接抛出错误
    if cmd_result.returncode != 0:
        raise Exception(f"命令执行失败：{cmd_result.stderr.strip()}")
    
    disk_list = []
    lines = cmd_result.stdout.splitlines()
    # 跳过第一行表头 Filesystem Size Used Avail Use% Mounted on
    for line in lines[1:]:
        data = line.split()
        fs = data[0]       # 磁盘分区
        used_rate = data[4]# 使用率 12%
        mount = data[5]    # 挂载点
        # 去掉百分号转数字
        rate_num = int(used_rate.replace("%", ""))
        disk_list.append({
            "fs": fs,
            "rate": rate_num,
            "mount": mount
        })
    return disk_list

def check_warning(disk_list):
    """遍历磁盘，终端打印告警，同时组装报表文本"""
    report_content = "===== 磁盘巡检报表 =====\n"
    report_content += f"告警阈值：{WARN_THRESHOLD}%\n\n"

    print("===== 磁盘巡检结果 =====")
    for disk in disk_list:
        fs = disk["fs"]
        rate = disk["rate"]
        mount = disk["mount"]
        line_text = f"分区：{fs:12} 挂载点：{mount:15} 使用率：{rate}%"
        
        # 判断是否超阈值
        if rate >= WARN_THRESHOLD:
            print(f"{RED}[告警]{RESET} " + line_text)
            report_content += f"【告警】{line_text}\n"
        else:
            print(f"{GREEN}[正常]{RESET} " + line_text)
            report_content += f"【正常】{line_text}\n"
    return report_content

def write_report(content):
    """把巡检报表写入txt文件"""
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\n巡检报表已保存至：{REPORT_FILE}")

if __name__ == "__main__":
    try:
        disk_data = get_disk_info()
        report_txt = check_warning(disk_data)
        write_report(report_txt)
    except Exception as e:
        print(f"{RED}巡检异常：{e}{RESET}")
