# host_list.py 运维主机清单读取工具
import os

def get_host_list():
    """
    读取本地hosts.txt主机清单，过滤无效内容，返回结构化主机列表
    :return: 列表嵌套字典 [{}, {}, ...]
    """
    # 1. 定义空列表：用于存放最终干净的机器数据（内存临时变量）
    host_info_list = []

    # 2. 安全拼接文件路径（跨Windows/Linux通用）
    file_path = os.path.join(os.getcwd(), "hosts.txt")

    # 3. 上下文方式读取文件
    with open(file_path, mode="r", encoding="utf-8") as f:
        # 逐行遍历文件所有内容
        for line in f:
            # 去除首尾空格、换行符
            line_strip = line.strip()

            # 过滤规则1：空行直接跳过
            if not line_strip:
                continue
            # 过滤规则2：注释行直接跳过
            if line_strip.startswith("#"):
                continue

            # 4. 文本切割：一行字符串拆分为 IP、用户名、密码
            ip, username, password = line_strip.split()

            # 5. 封装为字典（打标签，程序精准识别每个字段）
            host_info_list.append({
                "ip": ip,
                "username": username,
                "password": password
            })

    # 6. 返回结构化数据，供其他脚本调用
    return host_info_list

# 本地测试运行
if __name__ == "__main__":
    res = get_host_list()
    print("===== 清洗后的有效主机清单 =====")
    for host in res:
        print(host)

