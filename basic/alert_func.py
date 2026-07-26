# alert_func.py Day6 统一告警工具封装 全局可导入复用
import os
from datetime import datetime

# ===================== 全局颜色常量（所有脚本共用）=====================
COLOR = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "reset": "\033[0m"
}

# 全局日志存储路径
ALERT_LOG_PATH = os.path.join(os.getcwd(), "alert_record.log")

def send_alert(msg, level="info", save_log=True):
    """
    统一告警输出函数
    :param msg: 告警文本内容（必填）
    :param level: 告警等级，默认info；可选 info/success/warn/error
    :param save_log: 是否写入告警日志文件，默认True开启
    :return: 格式化后的完整告警字符串
    """
    # 等级匹配对应颜色与标识
    level_config = {
        "info": {"tag": "[信息]", "color": COLOR["blue"]},
        "success": {"tag": "[正常]", "color": COLOR["green"]},
        "warn": {"tag": "[警告]", "color": COLOR["yellow"]},
        "error": {"tag": "[告警]", "color": COLOR["red"]}
    }
    # 兼容非法等级，默认info
    cfg = level_config.get(level, level_config["info"])
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 组装打印文本
    print_text = f"{cfg['color']}{cfg['tag']} {now_time} | {msg}{COLOR['reset']}"
    # 终端打印带颜色告警
    print(print_text)

    # 判断是否持久化写入日志（日志无颜色）
    if save_log:
        log_text = f"{cfg['tag']} {now_time} | {msg}\n"
        with open(ALERT_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(log_text)
    # 返回格式化文本，供外部脚本接收使用
    return print_text
