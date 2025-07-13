import os
import sys
import re

def display_help():
    help_text = """
    使用说明:
    python replace_links.py <folder_path> <mode>

    参数:
    <folder_path>  - 需要遍历的文件夹路径
    <mode>         - 运行模式，可选值为 1, 2, 3, 4, 5, 6, 7, 8

    模式说明:
    模式1: 将GitHub链接替换为Gitea链接。用于外网文档向内网迁移。

    模式2: 将Gitea链接替换为Github链接。用于内外文档向外分享。

    模式3: 将GitHub、Gitea链接替换为本地链接。用于离线查看文档图片。

    模式4: 将本地链接替换为Github链接。同模式2，用于向外分享。

    模式5: 将本地链接替换为Gitea链接。Gitea链接应该是组织内分享文档的默认链接方式。
    
    模式6: 将Obsidian内链替换为Gitea链接。用于解决遗漏文档的链接替换问题。
    
    模式7: 将Markdown格式图片链接替换为html格式。
    
    模式8: 依次执行模式 6 和模式 7。

    注意事项:
    - 确保文件夹路径有效且包含Markdown文件（.md后缀）。
    - 请在执行前备份文件以防数据丢失。

    示例:
    python replace_links.py /path/to/your/folder 1
    """
    print(help_text)
    
def replace_mode6(content, folder_path):
    # 使用正则表达式匹配所有 [[...]] 中的内容
    matches = re.findall(r'\[\[(.*?)\]\]', content)
    
    # 遍历所有匹配的内容
    for match in matches:
        # 拼接文件路径
        file_path = os.path.join(folder_path, match)
        
        # 检查文件路径是否存在
        if os.path.exists(file_path):
            # 替换匹配内容为指定的替换文字
            replacement_text=f"<div align=\"center\"><img src=\"https://tmcodeserver:3000/TerraMatrix/wiki-cache/raw/branch/master/img-cache/{match}\" alt=\"{match}\" style=\"zoom:100%;\" /></div>"
            
            content = content.replace(f'![[{match}]]', replacement_text)
    
    return content

def replace_mode7(content):
    # 正则表达式，用于匹配Markdown格式的图片链接 ![title](link)
    markdown_image_pattern = r'!\[(.*?)\]\((.*?)\)'

    # 替换函数
    def replace_match(match):
        title = match.group(1)
        link = match.group(2)
        # 如果 title 为空，生成的 HTML 中不包含 alt 属性
        if title:
            replacement_text = f'<div align="center"><img src="{link}" alt="{title}" style="zoom:100%;" /></div>'
        else:
            replacement_text = f'<div align="center"><img src="{link}" style="zoom:100%;" /></div>'
        return replacement_text

    # 使用 re.sub() 函数进行替换
    result = re.sub(markdown_image_pattern, replace_match, content)

    return result


def check_file_in_except(file_name):
    """
    检查指定文件名是否在队列中。

    :param file_name: 要检查的文件名
    :return: 如果文件名在队列中返回True，否则返回False
    """
    file_name_queue = ["wiki图床链接自动替换脚本.md", 
                       "2024-02-21 小组会议.md",
                       "vcpkg手册.md",
                       "Markdown Reference.md",
                       "从0开始小组知识共享.md"]
    
    return file_name in file_name_queue

def replace_links_in_file(file_path, mode, folder_path):
    file_name = os.path.basename(file_path)
    
    # 跳过脚本代码
    if check_file_in_except(file_name):
        return
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    if mode == 1:
        content = re.sub(r'https://raw\.githubusercontent\.com/TerraMatrix/wiki-cache/(?:upstream-master|master)/img-cache',
                         r'https://tmcodeserver/gitea/TerraMatrix/wiki-cache/raw/branch/master/img-cache', content)
    elif mode == 2:
        content = re.sub(r'https://tmcodeserver:3000/TerraMatrix/wiki-cache/raw/branch/master/img-cache',
                         r'https://raw.githubusercontent.com/TerraMatrix/wiki-cache/master/img-cache', content)
        content = re.sub(r'https://tmcodeserver/gitea/TerraMatrix/wiki-cache/raw/branch/master/img-cache',
                         r'https://raw.githubusercontent.com/TerraMatrix/wiki-cache/master/img-cache', content)
    elif mode == 3:
        folder_uri = 'file://' + folder_path.replace(os.sep, '/') + '/附件/img-cache'
        content = re.sub(r'https://raw\.githubusercontent\.com/TerraMatrix/wiki-cache/(?:upstream-master|master)/img-cache',
                         folder_uri, content)
        content = re.sub(r'https://tmcodeserver:3000/TerraMatrix/wiki-cache/raw/branch/master/img-cache',
                         folder_uri, content)
        content = re.sub(r'https://tmcodeserver/gitea/TerraMatrix/wiki-cache/raw/branch/master/img-cache',
                         folder_uri, content)
    elif mode == 4:
        folder_uri = 'file://' + folder_path.replace(os.sep, '/') + '/附件/img-cache'
        content = re.sub(re.escape(folder_uri),
                         r'https://raw.githubusercontent.com/TerraMatrix/wiki-cache/master/img-cache', content)
    elif mode == 5:
        folder_uri = 'file://' + folder_path.replace(os.sep, '/') + '/附件/img-cache'
        content = re.sub(re.escape(folder_uri),
                         r'https://tmcodeserver/gitea/TerraMatrix/wiki-cache/raw/branch/master/img-cache', content)
    elif mode == 6:
        content = replace_mode6(content, folder_path.replace(os.sep, '/') + '/附件/img-cache')
    elif mode == 7:
        content = replace_mode7(content)
    elif mode == 8:
        content = replace_mode6(content, folder_path.replace(os.sep, '/') + '/附件/img-cache')
        content = replace_mode7(content)

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

    if mode not in [1, 2, 3, 4, 5, 6, 7, 8]:
        print(f"错误: {mode} 不是有效的模式。必须为 1 ~ 8。\n")
        display_help()
        sys.exit(1)

    process_folder(folder_path, mode)

if __name__ == "__main__":
    main()