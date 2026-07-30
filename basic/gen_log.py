# gen_log.py Day10 循环进阶 批量生成模拟业务日志
import random
import time
from alert_func import send_alert
import sys

# 日志模板
normal_log_tpl = [
    "INFO request finish uri=/api/user code=200 cost={}ms",
    "INFO query database success cost={}ms",
    "INFO cache hit key=user_info_10086",
    "INFO async task execute success task_id={}",
]

error_log_tpl = [
    "ERROR request fail uri=/api/pay code=500 cost={}ms",
    "ERROR database connect failed timeout",
    "WARN redis connection fail, retry connect",
    "ERROR file write failed IOError",
]

def random_timestamp():
    """生成近1小时内随机时间戳，格式化日志时间"""
    now = time.time()
    # 随机减去0~3600秒
    random_sec = random.randint(0, 3600)
    t = time.localtime(now - random_sec)
    return time.strftime("%Y-%m-%d %H:%M:%S", t)

def generate_logs(total_line=100):
    """
    批量生成日志写入文件
    :param total_line: 日志总行数
    """
    log_file = "app_sim.log"
    try:
        with open(log_file, "w", encoding="utf-8") as f:
            # for循环 range 生成指定条数日志
            for line_num in range(total_line):
                current_time = random_timestamp()
                # 70%概率正常日志，30%错误日志
                if random.random() < 0.7:
                    content = random.choice(normal_log_tpl)
                else:
                    content = random.choice(error_log_tpl)

                # 填充随机数字
                cost_ms = random.randint(10, 500)
                task_id = random.randint(10000, 99999)
                log_content = content.format(cost_ms, task_id)

                full_line = f"[{current_time}] {log_content}\n"
                f.write(full_line)

        send_alert(f"日志生成完成！总共 {total_line} 行", level="success")
        send_alert(f"日志文件：{log_file}", level="info")

    except PermissionError:
        send_alert("文件写入权限不足！", level="error")
        sys.exit(1)

def demo_while_loop():
    """【拓展】while循环实现同等效果，对比两种循环写法"""
    send_alert("\n==== while循环实现演示（可选学习） ====", level="info")
    count = 0
    while count < 5:
        print(f"while循环计数：{count}")
        count += 1

if __name__ == "__main__":
    # 判断是否传入自定义行数参数
    if len(sys.argv) == 2:
        try:
            line_count = int(sys.argv[1])
            generate_logs(line_count)
        except ValueError:
            send_alert("参数必须为数字！示例：python3 gen_log.py 200", level="error")
    else:
        # 默认生成100条日志
        generate_logs(100)
    demo_while_loop()
