# k8s_ns_create.py Day5 PyYAML读写 批量生成K8s Namespace资源清单
import yaml
import os

# 全局配置
CONFIG_YAML = os.path.join(os.getcwd(), "ns_list.yaml")
OUTPUT_DIR = os.path.join(os.getcwd(), "k8s_ns_yaml")

def read_ns_config():
    """读取ns_list.yaml配置文件，返回字典数据"""
    if not os.path.exists(CONFIG_YAML):
        raise FileNotFoundError(f"配置文件不存在：{CONFIG_YAML}")
    with open(CONFIG_YAML, "r", encoding="utf-8") as f:
        # safe_load 安全读取yaml，禁止危险序列化对象
        config = yaml.safe_load(f)
    return config

def build_k8s_ns_manifest(ns_name, label_dict):
    """拼接标准K8s Namespace yaml结构体（Python字典）"""
    k8s_ns_template = {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata": {
            "name": ns_name,
            "labels": label_dict
        }
    }
    return k8s_ns_template

def write_manifest_file(ns_data, ns_name):
    """将k8s字典结构体dump写入yaml文件"""
    # 不存在输出目录则自动创建
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    file_path = os.path.join(OUTPUT_DIR, f"ns-{ns_name}.yaml")
    with open(file_path, "w", encoding="utf-8") as f:
        # safe_dump 安全导出yaml，关闭排序、保留原生顺序
        yaml.safe_dump(
            ns_data,
            f,
            sort_keys=False,
            default_flow_style=False,
            encoding="utf-8"
        )
    print(f"✅ 已生成资源文件：k8s_ns_yaml/ns-{ns_name}.yaml")

if __name__ == "__main__":
    try:
        # 1. 读取配置yaml
        cfg = read_ns_config()
        ns_name_list = cfg["namespace"]
        public_labels = cfg["labels"]

        # 2. 循环所有namespace，批量生成资源清单
        for ns in ns_name_list:
            ns_manifest = build_k8s_ns_manifest(ns, public_labels)
            write_manifest_file(ns_manifest, ns)

        print(f"\n🎉 全部{len(ns_name_list)}个Namespace清单生成完成！")
        print(f"部署命令示例：kubectl apply -f k8s_ns_yaml/")
    except Exception as e:
        print(f"❌ 执行失败：{e}")
