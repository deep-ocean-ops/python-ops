# safe_monitor.py Day7 try-except磁盘巡检全异常捕获 改造Day2脚本
import subprocess
import os
from alert_func import send_alert

# 常量配置
WARN_THRESHOLD = 80
REPORT_FILE = os.path.join(os.getcwd(), "disk_report.txt")
ERROR_LOG = os.path.join(os.getcwd(), "error.log")  # 单独异常日志文件

# ===================== 自定义业务异常 =====================
class DiskCommandError(Exception):
    """自定义异常：df磁盘命令执行失败"""
    pass

class DiskParseError(Exception):
    """自定义异常：磁盘输出解析、数值转换失败"""
    pass

# ===================== 异常日志写入工具 =====================
def write_error_log(exc_msg):
    """将异常信息单独写入error.log，时间戳记录"""
    from datetime import datetime
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{time_now}] ERROR: {exc_msg}\n"
    with open(ERROR_LOG, "a", encoding="utf-8") as f:
        f.write(log_line)

# ===================== 磁盘采集函数（全流程异常捕获） =====================
def get_disk_info():
    try:
        # 1. 执行df -h，捕获命令超时、权限、执行失败
        cmd_result = subprocess.run(
            ["df", "-h"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=3
        )
        # 命令返回码非0，抛出自定义异常
        if cmd_result.returncode != 0:
            raise DiskCommandError(f"df命令执行失败，stderr：{cmd_result.stderr.strip()}")
        
        disk_list = []
        lines = cmd_result.stdout.splitlines()
        # 跳过表头，逐行解析
        for line in lines[1:]:
            line_strip = line.strip()
            if not line_strip:
                continue
            data = line_strip.split()
            # 字段不足时触发解析异常
            if len(data) < 6:
                raise DiskParseError(f"磁盘行数据格式异常：{line_strip}")
            
            fs = data[0]
            used_rate_str = data[4]
            mount = data[5]
            # 去除百分号转数字，捕获非数字报错
            try:
                rate_num = int(used_rate_str.replace("%", ""))
            except ValueError:
                raise DiskParseError(f"使用率无法转为数字，原始值：{used_rate_str}")
            
            disk_list.append({
                "fs": fs,
                "rate": rate_num,
                "mount": mount
            })
        return disk_list

    # 分层捕获指定异常，精准区分问题
    except subprocess.TimeoutExpired as e:
        err_msg = f"磁盘命令执行超时：{str(e)}"
        send_alert(err_msg, level="error")
        write_error_log(err_msg)
        return None
    except PermissionError as e:
        err_msg = f"权限不足，无法读取磁盘分区：{str(e)}"
        send_alert(err_msg, level="error")
        write_error_log(err_msg)
        return None
    except DiskCommandError as e:
        err_msg = f"磁盘命令异常：{str(e)}"
        send_alert(err_msg, level="error")
        write_error_log(err_msg)
        return None
    except DiskParseError as e:
        err_msg = f"磁盘数据解析异常：{str(e)}"
        send_alert(err_msg, level="error")
        write_error_log(err_msg)
        return None
    # 兜底捕获所有未知异常
    except Exception as e:
        err_msg = f"未知采集异常：{str(e)}"
        send_alert(err_msg, level="error")
        write_error_log(err_msg)
        return None

# ===================== 巡检告警判断 =====================
def check_warning(disk_list):
    if not disk_list:
        send_alert("无有效磁盘数据，跳过报表生成", level="warn")
        return ""
    
    report_content = "===== 磁盘巡检报表 =====\n"
    report_content += f"告警阈值：{WARN_THRESHOLD}%\n\n"
    print("===== 磁盘巡检结果 =====")
    for disk in disk_list:
        line_text = f"分区：{disk['fs']:12} 挂载点：{disk['mount']:15} 使用率：{disk['rate']}%"
        if disk["rate"] >= WARN_THRESHOLD:
            send_alert(line_text, level="error")
            report_content += f"【告警】{line_text}\n"
        else:
            send_alert(line_text, level="success")
            report_content += f"【正常】{line_text}\n"
    return report_content

# ===================== 写入报表文件（捕获文件操作异常） =====================
def write_report(content):
    try:
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.write(content)
        send_alert(f"巡检报表已保存至：{REPORT_FILE}", level="info")
    except PermissionError as e:
        err_msg = f"报表文件写入权限不足：{str(e)}"
        send_alert(err_msg, level="error")
        write_error_log(err_msg)
    except OSError as e:
        err_msg = f"报表文件系统异常：{str(e)}"
        send_alert(err_msg, level="error")
        write_error_log(err_msg)

# ===================== 程序入口 全局顶层异常捕获 =====================
if __name__ == "__main__":
    try:
        disk_data = get_disk_info()
        report_txt = check_warning(disk_data)
        if report_txt:
            write_report(report_txt)
    except Exception as e:
        err_msg = f"程序顶层未知崩溃异常：{str(e)}"
        send_alert(err_msg, level="error")
        write_error_log(err_msg)
