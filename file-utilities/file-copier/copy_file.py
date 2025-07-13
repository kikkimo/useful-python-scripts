import sys
import shutil
import os
import hashlib
import glob

# 定义创建文件夹函数，兼容新旧版本
def makedirs_compat(dest_path):
    if sys.version_info < (3, 2):
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
    else:
        if not os.path.exists(dest_path):
            os.makedirs(dest_path, exist_ok=True)

def compare_files(file1, file2):
    # 计算文件的哈希值并比较
    hash1 = hashlib.md5()
    hash2 = hashlib.md5()

    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        for chunk in iter(lambda: f1.read(4096), b""):
            hash1.update(chunk)
        for chunk in iter(lambda: f2.read(4096), b""):
            hash2.update(chunk)

    return hash1.hexdigest() == hash2.hexdigest()

def shutil_copy(src_path, dest_path):
    try:
        shutil.copy2(src_path, dest_path)
        return True
    except Exception as e:
        print("Copying {} -> {} failed: {}".format(src_path, dest_path, e))
        return False

def copy_file(src_path, dest_path, mode="copy_if_different", verbose=True):
    src_path = src_path.replace('\\', '/')
    dest_path = dest_path.replace('\\', '/')
    # 检查 src_path 文件是否存在，如果不存在直接返回
    if not os.path.exists(src_path):
        print("Source file does not exist: {}".format(repr(src_path)))
        return
    # 使用 lower() 方法将 mode 转换成全小写
    mode = mode.lower()
    # 根据不同的 MODE 参数执行不同的文件拷贝操作
    if mode == "copy_always":
        dest_dir = os.path.dirname(dest_path)
        makedirs_compat(dest_dir)
        res = shutil_copy(src_path, dest_path)
        if verbose and res:
            print("Copying {} -> {}".format(repr(src_path), repr(dest_path)))
    elif mode == "copy_if_different":
        if not os.path.exists(dest_path) or not compare_files(src_path, dest_path):
            dest_dir = os.path.dirname(dest_path)
            makedirs_compat(dest_dir)
            res = shutil_copy(src_path, dest_path)
            if verbose and res:
                print("Copying (if different): {} -> {}".format(repr(src_path), repr(dest_path)))
        else:
            if verbose:
                print("Copying (if different): {} skipped".format(repr(src_path)))
    elif mode == "copy_if_not_exist":
        if not os.path.exists(dest_path):
            dest_dir = os.path.dirname(dest_path)
            makedirs_compat(dest_dir)
            res = shutil_copy(src_path, dest_path)
            if verbose and res:
                print("Copying (if not exist): {} -> {}".format(repr(src_path), repr(dest_path)))
        else:
            if verbose:
                print("Copying (if not exist): {} skipped".format(repr(src_path)))
    else:
        print("Invalid mode argument: {}".format(mode))

# copy_file（用法说明）示例：
def usage_copy_file():
    print("Usage: copy_file(src_path, dest_path, [mode], [verbose])")
    print("  src_path  : The source file to copy from.")
    print("  dest_path : The destination file path to copy to.")
    print("  mode      : (Optional) Copy mode. Default is 'copy_if_different'.")
    print("              Valid values: 'copy_always', 'copy_if_different', 'copy_if_not_exist'.")
    print("              - 'copy_always'      : Always copy the files, overwriting any existing files.")
    print("              - 'copy_if_different': Copy the files only if they are different from the")
    print("                                     corresponding files in the destination directory.")
    print("              - 'copy_if_not_exist': Copy the files only if they do not already exist in")
    print("                                     the destination directory.")
    print("  verbose   : (Optional) If True (default), print information during the copying process.")
    
def copy_files(dest_path, mode, *src_files, **kwargs):
    if not src_files:
        print("src_files is not defined")
        return
    elif len(src_files) == 1:
        src_files = src_files[0].split(";")

    verbose = kwargs.get("verbose", True)

    # 创建dest_path文件夹
    makedirs_compat(dest_path)
    
    for src_file in src_files:
        # 使用glob模块匹配通配符
        matched_files = glob.glob(src_file)
        
        if not matched_files:
            # print(f"No files matched the wildcard: {src_file}")
            # 修改以兼容低版本的python
            print("No files matched the wildcard: {}".format(repr(src_file)))
            continue
        
        for matched_file in matched_files:
            file_name = os.path.basename(matched_file)
            dest_file = os.path.join(dest_path, file_name)
            copy_file(matched_file, dest_file, mode, verbose=verbose)

# copy_files（用法说明）示例：
def usage_copy_files():
    print("Usage: copy_files(dest_path, mode, *src_files, **kwargs)")
    print("  dest_path : The destination directory path where files will be copied to.")
    print("  mode      : Copy mode. Specify how to handle the copying process.")
    print("              Valid values: 'copy_always', 'copy_if_different', 'copy_if_not_exist'.")
    print("              - 'copy_always'      : Always copy the files, overwriting any existing files.")
    print("              - 'copy_if_different': Copy the files only if they are different from the")
    print("                                     corresponding files in the destination directory.")
    print("              - 'copy_if_not_exist': Copy the files only if they do not already exist in")
    print("                                     the destination directory.")
    print("  *src_files: (Variable number of arguments) Source file paths or patterns to copy from.")
    print("              You can pass multiple source file paths or patterns (with wildcards) as separate arguments.")
    print("  **kwargs  : (Optional) Additional keyword arguments to control the copying process.")
    print("              - 'verbose' (bool, default=True): If True, print information during the copying process.")
    print("                                                 If False, do not print any information.")
    print("                                                 Note: Other keyword arguments may be added in the future.")
    print("Example: copy_files('destination_dir', 'copy_if_different', 'file1.txt', 'libQt*.so;libgdal.so', verbose=True)")

def copy_relative_files(src_path, dest_path, mode, *relative_file_names, **kwargs):
    if not src_path:
        print("src_path is not defined")
        return
    
    if not dest_path:
        print("dest_path is not defined")
        return
    
    if not relative_file_names:
        print("relative_file_names is not defined")
        return
    elif len(relative_file_names) == 1:
        relative_file_names = relative_file_names[0].split(";")
        
    verbose = kwargs.get("verbose", True)

    src_path = src_path.replace('\\','/')
    dest_path = dest_path.replace('\\','/')
     # 判断src_path对应的文件夹是否存在
    if not os.path.exists(src_path) or not os.path.isdir(src_path):
        print("Path does not exist: {}".format(repr(src_path)))
        return
    # 创建dest_path文件夹
    makedirs_compat(dest_path)
    
    for relative_file_name in relative_file_names:
        src_file = os.path.join(src_path, relative_file_name)
        dest_file = os.path.join(dest_path, relative_file_name)
        copy_file(src_file, dest_file, mode, verbose=verbose)
   
# copy_relative_files（用法说明）示例：     
def usage_copy_relative_files():
    print("Usage: copy_relative_files(src_path, dest_path, mode, *relative_file_names, **kwargs)")
    print("  src_path           : The source directory path where files are located.")
    print("  dest_path          : The destination directory path where files will be copied to.")
    print("  mode               : Copy mode. Specify how to handle the copying process.")
    print("                       Valid values: 'copy_always', 'copy_if_different', 'copy_if_not_exist'.")
    print("                       - 'copy_always'      : Always copy the files, overwriting any existing files.")
    print("                       - 'copy_if_different': Copy the files only if they are different from the")
    print("                                              corresponding files in the destination directory.")
    print("                       - 'copy_if_not_exist': Copy the files only if they do not already exist in")
    print("                                              the destination directory.")
    print("  *relative_file_names: (Variable number of arguments) File names relative to src_path to copy from.")
    print("                       You can pass multiple file names as separate arguments.")
    print("  **kwargs            : (Optional) Additional keyword arguments to control the copying process.")
    print("                       - 'verbose' (bool, default=True): If True, print information during the copying process.")
    print("                                                         If False, do not print any information.")
    print("                                                         Note: Other keyword arguments may be added in the future.")
    print("Example: copy_relative_files('src_dir', 'dest_dir', 'copy_if_different', 'file1.txt', 'file2.txt', verbose=True)")

def copy_directory(src_path, dest_path, mode="copy_if_different", *exceptions, **kwargs):
    if not src_path:
        print("src_path is not defined")
        return
    
    if not dest_path:
        print("dest_path is not defined")
        return
    src_path = src_path.replace('\\','/')
    dest_path = dest_path.replace('\\','/')
    verbose = kwargs.get("verbose", True)
     # 判断src_path对应的文件夹是否存在
    if not os.path.exists(src_path) or not os.path.isdir(src_path):
        print("Path does not exist: {}".format(repr(src_path)))
        return

    if exceptions:
        if len(exceptions) == 1:
            exceptions = exceptions[0].split(";")
        if verbose:
            print("exceptions: {}".format(exceptions))
        
    #创建dest_path文件夹
    makedirs_compat(dest_path)

    # 递归遍历src_path的所有文件和文件夹
    for root, dirs, files in os.walk(src_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_path = file_path.replace('\\','/')
            file_name = file.lower()  # 将文件名转换为小写，以便忽略大小写

             # 判断exceptions列表是否为空，如果不为空，检查文件名是否在exceptions中
            if exceptions and file_name in [ex.lower() for ex in exceptions]:
                if verbose:
                    print("Copying (in exceptions): {} skipped".format(file_path))
                continue

            # 获取相对路径
            relative_path = os.path.relpath(file_path, src_path)
            real_dest_path = os.path.join(dest_path, relative_path)
            real_dest_path = real_dest_path.replace('\\','/')

            # 复制文件到目标路径
            copy_file(file_path, real_dest_path, mode, verbose=verbose)
            

# copy_directory（usage）示例：
def usage_copy_directory():
    print("Usage: copy_directory(src_path, dest_path, [mode], [*exceptions], [verbose])")
    print("  src_path      : The source directory to copy from.")
    print("  dest_path     : The destination directory to copy to.")
    print("  mode          : (Optional) Copy mode. Default is 'copy_if_different'.")
    print("                  Valid values: 'copy_always', 'copy_if_different', 'copy_if_not_exist'.")
    print("                  - 'copy_always'      : Always copy the files, overwriting any existing files.")
    print("                  - 'copy_if_different': Copy the files only if they are different from the")
    print("                                         corresponding files in the destination directory.")
    print("                  - 'copy_if_not_exist': Copy the files only if they do not already exist in")
    print("                                         the destination directory.")
    print("  *exceptions   : (Optional) A variable number of strings representing")
    print("                  filenames to exclude from the copy process.")
    print("                  These filenames will not be copied.")
    print("  **kwargs      : (Optional) Additional keyword arguments to control the copying process.")
    print("                  - 'verbose' (bool, default=True): If True, print information during the copying process.")
    print("                                                    If False, do not print any information.")
    print("                                                    Note: Other keyword arguments may be added in the future.")
    print("Example: copy_directory('src_dir', 'dest_dir', 'copy_if_different', 'file1.txt', 'file2.txt', verbose=True)")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python file_copy.py function_name [args...] [verbose]")
        sys.exit(1)
        
    # for i, arg in enumerate(sys.argv):
    #    print("参数 {}: {}".format(i, arg))

    function_name = sys.argv[1]
    args = sys.argv[2:]
    
    if args[-1].lower() == "true":
        print(sys.argv)

    if function_name == "copy_file":
        if len(args) < 3:
            usage_copy_file()
            sys.exit(1)
        verbose = True if args[-1].lower() == "true" else False
        copy_file(*args[:-1], verbose=verbose)

    elif function_name == "copy_files":
        if len(args) < 3:
            usage_copy_files()
            sys.exit(1)
        verbose = True if args[-1].lower() == "true" else False
        copy_files(*args[:-1], verbose=verbose)

    elif function_name == "copy_relative_files":
        if len(args) < 4:
            usage_copy_relative_files()
            sys.exit(1)
        verbose = True if args[-1].lower() == "true" else False
        copy_relative_files(*args[:-1], verbose=verbose)

    elif function_name == "copy_directory":
        if len(args) < 3:
            usage_copy_directory()
            sys.exit(1)
        verbose = True if args[-1].lower() == "true" else False
        copy_directory(*args[:-1], verbose=verbose)

    else:
        print("Invalid function name: {}".format(function_name))
        sys.exit(1)
