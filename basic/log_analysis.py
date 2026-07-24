# log_analysis.py Day4 re正则日志错误过滤统计
import re
import os
from collections import defaultdict

# 配置常量
LOG_FILE = os.path.join(os.getcwd(), "app.log")
# 正则规则：匹配包含 error / fail / 500 的日志（忽略大小写）
ERROR_PATTERN = re.compile(r"error|fail|500", re.IGNORECASE)
# 提取错误类型分组正则，捕获ERROR后面的报错描述
TYPE_PATTERN = re.compile(r"ERROR (.*?)(?= uid=|$)", re.IGNORECASE)

def read_error_log():
    """读取日志，过滤所有错误行，返回错误行列表"""
    error_lines = []
    # 判断日志文件是否存在
    if not os.path.exists(LOG_FILE):
        print(f"日志文件 {LOG_FILE} 不存在！")
        return []
    
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line_strip = line.strip()
            if not line_strip:
                continue
            # re.search：整行任意位置匹配错误关键字
            if ERROR_PATTERN.search(line_strip):
                error_lines.append(line_strip)
    return error_lines

def count_error_top10(error_lines):
    """统计错误类型出现次数，排序取Top10"""
    error_count = defaultdict(int)
    for line in error_lines:
        # 分组提取错误详情
        match = TYPE_PATTERN.search(line)
        if match:
            error_msg = match.group(1).strip()
            error_count[error_msg] += 1
    # 按出现次数倒序排序，取前10
    top10 = sorted(error_count.items(), key=lambda x: x[1], reverse=True)[:10]
    return top10

def print_report(error_lines, top10):
    """格式化输出统计报表"""
    print("=" * 60)
    print(f"日志分析报告 | 日志文件：{LOG_FILE}")
    print(f"总日志行数中错误总行数：{len(error_lines)}")
    print("=" * 60)

    print("\n【Top10 高频错误排行】")
    print(f"{'排名':<4}{'出现次数':<8}{'错误详情'}")
    print("-" * 60)
    for idx, (err_msg, count) in enumerate(top10, start=1):
        print(f"{idx:<4}{count:<8}{err_msg}")

    print("\n【全部原始错误日志】")
    print("-" * 60)
    for line in error_lines:
        print(line)

if __name__ == "__main__":
    # 1. 读取过滤错误日志
    error_data = read_error_log()
    if not error_data:
        exit()
    # 2. 统计Top10错误
    top_error = count_error_top10(error_data)
    # 3. 打印完整报表
    print_report(error_data, top_error)
