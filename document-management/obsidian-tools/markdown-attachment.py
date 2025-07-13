import os
import sys
import re

def display_help():
    help_text = """
    使用说明:
    python replace_links.py <folder_path> <mode>

    参数:
    <folder_path>  - 需要遍历的文件夹路径
    <mode>         - 运行模式，可选值为 1, 2, 3, 4, 5

    模式说明:
    模式1: 将GitHub链接（https://raw.githubusercontent.com/TerraMatrix/wiki-cache/upstream-master/img-cache 或 
           https://raw.githubusercontent.com/TerraMatrix/wiki-cache/master/img-cache）替换为 
           https://tmcodeserver:3000/TerraMatrix/wiki-cache/raw/branch/master/img-cache。

    模式2: 将 https://tmcodeserver:3000/TerraMatrix/wiki-cache/raw/branch/master/img-cache 替换为 
           https://raw.githubusercontent.com/TerraMatrix/wiki-cache/master/img-cache。

    模式3: 将GitHub链接或 https://tmcodeserver:3000/TerraMatrix/wiki-cache/raw/branch/master/img-cache 
           替换为 file://<folder_path>/附件/img-cache（其中 <folder_path> 为你输入的文件夹路径，分隔符会自动转换为 /）。

    模式4: 将 file://<folder_path>/附件/img-cache 替换为 
           https://raw.githubusercontent.com/TerraMatrix/wiki-cache/master/img-cache。

    模式5: 将 file://<folder_path>/附件/img-cache 替换为 
           https://tmcodeserver:3000/TerraMatrix/wiki-cache/raw/branch/master/img-cache。

    注意事项:
    - 确保文件夹路径有效且包含Markdown文件（.md后缀）。
    - 请在执行前备份文件以防数据丢失。

    示例:
    python replace_links.py /path/to/your/folder 1
    """
    print(help_text)

def replace_links_in_file(file_path, mode, folder_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    if mode == 1:
        content = re.sub(r'https://raw\.githubusercontent\.com/TerraMatrix/wiki-cache/(?:upstream-master|master)/img-cache',
                         r'https://tmcodeserver:3000/TerraMatrix/wiki-cache/raw/branch/master/img-cache', content)
    elif mode == 2:
        content = re.sub(r'https://tmcodeserver:3000/TerraMatrix/wiki-cache/raw/branch/master/img-cache',
                         r'https://raw.githubusercontent.com/TerraMatrix/wiki-cache/master/img-cache', content)
    elif mode == 3:
        folder_uri = 'file://' + folder_path.replace(os.sep, '/') + '/附件/img-cache'
        content = re.sub(r'https://raw\.githubusercontent\.com/TerraMatrix/wiki-cache/(?:upstream-master|master)/img-cache',
                         folder_uri, content)
        content = re.sub(r'https://tmcodeserver:3000/TerraMatrix/wiki-cache/raw/branch/master/img-cache',
                         folder_uri, content)
    elif mode == 4:
        folder_uri = 'file://' + folder_path.replace(os.sep, '/') + '/附件/img-cache'
        content = re.sub(re.escape(folder_uri),
                         r'https://raw.githubusercontent.com/TerraMatrix/wiki-cache/master/img-cache', content)
    elif mode == 5:
        folder_uri = 'file://' + folder_path.replace(os.sep, '/') + '/附件/img-cache'
        content = re.sub(re.escape(folder_uri),
                         r'https://tmcodeserver:3000/TerraMatrix/wiki-cache/raw/branch/master/img-cache', content)

    # 注意，这里使用 LF 换行符
    with open(file_path, 'w', encoding='utf-8', newline='\n') as file:
        file.write(content)
    print(f"{file_path.replace(os.sep, '/')} 转换完成!")

def process_folder(folder_path, mode):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                replace_links_in_file(file_path, mode, folder_path)

def main():
    if len(sys.argv) != 3 or sys.argv[1] in ['help', '--help', '-h']:
        display_help()
        sys.exit(1)

    folder_path = sys.argv[1]
    try:
        mode = int(sys.argv[2])
    except ValueError:
        display_help()
        sys.exit(1)

    if not os.path.isdir(folder_path):
        print(f"错误: {folder_path} 不是有效的目录路径。")
        sys.exit(1)

    if mode not in [1, 2, 3, 4, 5]:
        print(f"错误: {mode} 不是有效的模式。必须为 1, 2, 3, 4 或 5。\n")
        display_help()
        sys.exit(1)

    process_folder(folder_path, mode)

if __name__ == "__main__":
    main()
