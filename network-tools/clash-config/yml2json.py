import yaml
import json
import sys
import os

def convert_yml_to_json(yml_file_path, json_file_path):
    """
    将YAML文件转换为JSON文件
    
    参数:
        yml_file_path (str): YAML源文件路径
        json_file_path (str): JSON目标文件路径
    
    异常:
        FileNotFoundError: 当源文件不存在时抛出
        yaml.YAMLError: 当YAML文件格式错误时抛出
        IOError: 当文件读写出现错误时抛出
    """
    try:
        # 检查YAML源文件是否存在
        if not os.path.exists(yml_file_path):
            raise FileNotFoundError(f"YAML源文件不存在: {yml_file_path}")
        
        # 检查YAML源文件是否为文件（而非目录）
        if not os.path.isfile(yml_file_path):
            raise ValueError(f"指定的YAML路径不是文件: {yml_file_path}")
        
        # 读取YML文件，明确指定使用utf-8编码
        print(f"正在读取YAML文件: {yml_file_path}")
        with open(yml_file_path, 'r', encoding='utf-8') as yml_file:
            yml_data = yaml.safe_load(yml_file)
        
        # 检查YAML数据是否为空
        if yml_data is None:
            print("警告: YAML文件为空或无有效内容")
            yml_data = {}
        
        # 确保JSON目标文件的目录存在
        json_dir = os.path.dirname(json_file_path)
        if json_dir and not os.path.exists(json_dir):
            os.makedirs(json_dir, exist_ok=True)
            print(f"已创建目录: {json_dir}")
        
        # 转换为格式化JSON并保存到文件，使用utf-8编码，保留中文字符
        print(f"正在写入JSON文件: {json_file_path}")
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(yml_data, json_file, indent=2, ensure_ascii=False)
        
        print(f"转换成功完成: {yml_file_path} -> {json_file_path}")
        
    except FileNotFoundError as e:
        print(f"错误: {e}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"YAML解析错误: {e}")
        sys.exit(1)
    except IOError as e:
        print(f"文件读写错误: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}")
        sys.exit(1)

def show_usage():
    """显示程序使用方法"""
    print("使用方法:")
    print("  python yml2json.py <yaml文件路径> <json文件路径>")
    print("")
    print("参数说明:")
    print("  <yaml文件路径>  : 要转换的YAML源文件路径（必须存在）")
    print("  <json文件路径>  : 要生成的JSON目标文件路径")
    print("")
    print("示例:")
    print("  python yml2json.py config.yml config.json")
    print("  python yml2json.py data/settings.yaml output/settings.json")

def main():
    """
    主函数：处理命令行参数并执行YAML到JSON的转换
    
    要求:
        - 必须提供2个参数：YAML源文件路径和JSON目标文件路径
        - YAML源文件必须存在
    """
    # 检查命令行参数数量（sys.argv[0]是脚本名，实际参数从索引1开始）
    if len(sys.argv) != 3:
        print("错误: 参数数量不正确")
        print(f"提供了 {len(sys.argv) - 1} 个参数，需要 2 个参数")
        print("")
        show_usage()
        sys.exit(1)
    
    # 获取命令行参数
    yml_file_path = sys.argv[1]
    json_file_path = sys.argv[2]
    
    # 检查YAML源文件是否存在
    if not os.path.exists(yml_file_path):
        print(f"错误: YAML源文件不存在: {yml_file_path}")
        print("")
        show_usage()
        sys.exit(1)
    
    # 检查YAML源文件是否为文件（而非目录）
    if not os.path.isfile(yml_file_path):
        print(f"错误: 指定的YAML路径不是文件: {yml_file_path}")
        print("")
        show_usage()
        sys.exit(1)
    
    # 执行转换
    convert_yml_to_json(yml_file_path, json_file_path)

# 程序入口点
if __name__ == "__main__":
    main()