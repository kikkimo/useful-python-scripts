# 实用Python脚本工具集

> 一个精心整理的Python实用脚本合集，涵盖文件处理、网络配置、文档管理等多个领域的常用工具。

## 📁 项目结构

```
useful-python-scripts/
├── network-tools/          # 网络工具类脚本
│   └── clash-config/       # Clash配置文件处理工具
├── file-utilities/         # 文件操作工具类脚本
│   └── file-copier/        # 智能文件复制工具
├── document-management/    # 文档管理工具类脚本
│   └── obsidian-tools/     # Obsidian相关工具
└── system-tools/           # 系统分析工具类脚本
    └── com-analysis/       # COM组件分析工具
```

## 🚀 功能概览

### 🌐 网络工具 (network-tools)
- **clash-config**: Clash配置文件处理工具集
  - YAML配置文件转JSON格式
  - 多配置文件智能合并
  - 地区代理自动分组

### 📁 文件工具 (file-utilities)
- **file-copier**: 智能文件复制工具
  - 多种复制模式支持
  - 文件差异检测
  - 批量文件操作
  - 通配符匹配支持

### 📝 文档管理 (document-management)
- **obsidian-tools**: Obsidian文档工具集
  - Markdown图片附件管理
  - 链接格式自动转换
  - 多种替换模式支持

### ⚙️ 系统工具 (system-tools)
- **com-analysis**: COM组件分析工具集
  - COM组件CLSID/TLBID差异分析
  - 自动manifest文件生成
  - 详细的变化统计报告

## 🔧 使用说明

每个工具类别下的具体脚本都包含独立的README.md文件，详细说明了：
- 功能介绍和特性
- 使用方法和参数说明
- 示例代码和执行效果
- 注意事项和依赖要求

## 📦 安装依赖

大部分脚本使用Python标准库，部分脚本可能需要额外依赖：

```bash
# Clash配置工具需要PyYAML
pip install PyYAML

# COM分析工具需要tabulate
pip install tabulate

# 其他脚本主要使用标准库
```

## 🎯 快速开始

1. **选择需要的工具类别**
   ```bash
   cd network-tools/clash-config     # 网络配置工具
   # 或
   cd file-utilities/file-copier     # 文件操作工具
   # 或
   cd document-management/obsidian-tools  # 文档管理工具
   # 或
   cd system-tools/com-analysis      # 系统分析工具
   ```

2. **查看具体使用说明**
   ```bash
   cat README.md  # 查看该工具的详细说明
   ```

3. **执行脚本**
   ```bash
   python script_name.py [参数]
   ```

## ⭐ 特色功能

- **🔄 智能处理**: 大多数脚本支持多种处理模式，适应不同使用场景
- **🛡️ 错误处理**: 完善的异常处理机制，提供友好的中文错误提示
- **📊 详细日志**: 完整的执行日志记录，便于问题诊断和进度跟踪
- **🌍 编码支持**: 全面支持UTF-8编码，正确处理中文字符
- **⚡ 高效执行**: 优化的算法设计，支持批量操作和并发处理

## 📋 脚本分类规则

- **网络工具**: 与网络配置、代理设置相关的脚本
- **文件工具**: 文件操作、复制、管理相关的脚本
- **文档管理**: 文档格式转换、链接处理、内容管理相关的脚本
- **系统工具**: 系统组件分析、版本比较相关的脚本

## 🔗 相关链接

- 每个工具的详细文档请查看对应文件夹下的README.md
- 建议在使用前仔细阅读各工具的使用说明和注意事项

## 📄 许可证

本项目为个人工具合集，仅供学习和个人使用。

---

*最后更新：2025-07-13*