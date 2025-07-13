# 智能文件复制工具

本项目提供了一个功能强大的Python文件复制工具，支持多种复制模式和智能文件处理功能。

## 📄 脚本概述

### copy_file.py - 智能文件复制工具

#### 功能说明
- 提供多种文件复制模式，满足不同使用场景
- 支持文件差异检测，避免不必要的复制操作
- 具备完整的参数验证和错误处理机制
- 支持通配符匹配和批量文件操作
- 兼容不同Python版本，提供详细的中文错误提示

#### 核心功能

##### 🔄 四种主要函数

1. **copy_file** - 单文件复制
   - 支持三种复制模式
   - 自动创建目标目录
   - 文件内容MD5比较

2. **copy_files** - 批量文件复制
   - 支持通配符匹配
   - 批量处理多个文件
   - 灵活的参数传递

3. **copy_relative_files** - 相对路径文件复制
   - 基于源目录的相对路径复制
   - 保持文件的相对目录结构
   - 适用于项目文件迁移

4. **copy_directory** - 目录复制
   - 递归复制整个目录结构
   - 支持文件排除列表
   - 保持原有目录结构

#### 复制模式说明

##### 📋 三种复制模式
- **copy_always**: 始终复制文件，覆盖现有文件
- **copy_if_different**: 仅在文件内容不同时复制（默认模式）
- **copy_if_not_exist**: 仅在目标文件不存在时复制

#### 使用方法

##### 单文件复制
```bash
python copy_file.py copy_file <源文件路径> <目标文件路径> [复制模式] [详细输出]
```

##### 批量文件复制
```bash
python copy_file.py copy_files <目标目录> <复制模式> <源文件1> [源文件2] ... [详细输出]
```

##### 相对路径文件复制
```bash
python copy_file.py copy_relative_files <源目录> <目标目录> <复制模式> <相对文件1> [相对文件2] ... [详细输出]
```

##### 目录复制
```bash
python copy_file.py copy_directory <源目录> <目标目录> [复制模式] [排除文件1] ... [详细输出]
```

#### 参数说明
- `复制模式`: copy_always | copy_if_different | copy_if_not_exist
- `详细输出`: true | false (是否显示详细的复制信息)

#### 使用示例

```bash
# 单文件复制示例
python copy_file.py copy_file "source.txt" "backup/source.txt" copy_if_different true

# 批量文件复制示例
python copy_file.py copy_files "backup/" copy_if_different "*.txt" "*.py" true

# 相对路径复制示例
python copy_file.py copy_relative_files "src/" "backup/" copy_if_different "config.ini" "data.json" true

# 目录复制示例
python copy_file.py copy_directory "project/" "backup/" copy_if_different "temp.txt" "cache.log" true
```

#### 程序化调用示例

```python
from copy_file import copy_file, copy_files, copy_relative_files, copy_directory

# 单文件复制
copy_file("source.txt", "backup/source.txt", "copy_if_different", verbose=True)

# 批量文件复制
copy_files("backup/", "copy_if_different", "*.txt", "*.py", verbose=True)

# 相对路径文件复制
copy_relative_files("src/", "backup/", "copy_if_different", "config.ini", "data.json", verbose=True)

# 目录复制（排除某些文件）
copy_directory("project/", "backup/", "copy_if_different", "temp.txt", "cache.log", verbose=True)
```

#### 特性亮点
- ✅ **智能文件比较**：使用MD5哈希值比较文件内容，准确判断文件差异
- ✅ **通配符支持**：支持使用通配符匹配多个文件，如 `*.txt`, `libQt*.so` 等
- ✅ **路径兼容性**：自动处理Windows和Unix风格的路径分隔符
- ✅ **版本兼容性**：兼容Python 2.7和Python 3.x版本
- ✅ **详细日志记录**：可选的详细输出模式，显示每个文件的复制状态
- ✅ **错误恢复**：完善的异常处理机制，单个文件失败不影响批量操作
- ✅ **目录自动创建**：自动创建不存在的目标目录
- ✅ **文件排除功能**：目录复制时支持排除指定文件

## 📊 性能特点

### 效率优化
- **文件差异检测**: 避免重复复制相同文件，节省时间和磁盘空间
- **批量操作**: 支持一次处理多个文件，提高操作效率
- **内存优化**: 使用分块读取方式计算MD5，适用于大文件处理

### 安全性
- **完整性验证**: 通过MD5比较确保文件复制的完整性
- **原子性操作**: 单个文件复制失败不影响其他文件的处理
- **路径验证**: 自动验证源文件和目标路径的有效性

## 🚀 快速开始

1. **查看帮助信息**
   ```bash
   python copy_file.py
   ```

2. **简单文件复制**
   ```bash
   python copy_file.py copy_file "input.txt" "output.txt" copy_if_different true
   ```

3. **批量复制文档文件**
   ```bash
   python copy_file.py copy_files "documents/" copy_if_different "*.txt;*.doc;*.pdf" true
   ```

4. **备份整个项目目录**
   ```bash
   python copy_file.py copy_directory "project/" "backup/" copy_if_different ".git;*.tmp" true
   ```

## ⚠️ 注意事项

1. **文件路径**: 支持相对路径和绝对路径，建议使用双引号包围包含空格的路径
2. **复制模式**: 默认使用`copy_if_different`模式，建议根据实际需求选择合适的模式
3. **大文件处理**: 对于大文件，MD5计算可能需要较长时间，请耐心等待
4. **权限要求**: 确保对源文件有读取权限，对目标目录有写入权限
5. **磁盘空间**: 复制前请确保目标磁盘有足够的可用空间

## 🔧 技术架构

- **编程语言**: Python 2.7 / 3.x
- **核心依赖**: os, sys, shutil, hashlib, glob
- **设计模式**: 函数式编程，模块化设计
- **错误处理**: 分层异常捕获和友好错误提示
- **兼容性**: 跨平台支持，Windows/Linux/macOS

## 📄 许可证

本项目为内部工具，仅供学习和个人使用。

---

## 🆘 常见问题

### Q: 如何处理包含空格的文件路径？
A: 使用双引号包围路径，例如：`"C:\\Program Files\\file.txt"`

### Q: 批量复制时如何指定多个文件模式？
A: 可以使用分号分隔，例如：`"*.txt;*.py;*.md"`，或者分别作为独立参数传递

### Q: copy_if_different模式如何判断文件是否不同？
A: 使用MD5哈希值比较文件内容，确保准确判断文件差异

### Q: 复制大量小文件时性能如何优化？
A: 建议使用`copy_if_different`模式避免重复复制，使用`verbose=False`减少输出开销

---

*最后更新：2025-07-13*