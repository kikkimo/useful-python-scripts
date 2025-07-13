# Obsidian文档工具集

本项目包含两个Python脚本，用于处理Obsidian笔记中的图片链接和文档格式转换。

## 📄 脚本概述

### 1. markdown-attachment.py - Markdown图片附件管理工具

#### 功能说明
- 批量处理Markdown文件中的图片链接
- 支持多种链接格式之间的相互转换
- 提供8种不同的转换模式，满足各种使用场景
- 具备完整的文件过滤和错误处理机制

#### 主要功能

##### 🔄 八种转换模式

1. **模式1**: GitHub链接 → Gitea链接
   - 用于外网文档向内网迁移
   - 将GitHub原始文件链接转换为Gitea服务器链接

2. **模式2**: Gitea链接 → GitHub链接  
   - 用于内网文档向外分享
   - 支持两种Gitea链接格式的转换

3. **模式3**: 远程链接 → 本地文件链接
   - 用于离线查看文档图片
   - 将GitHub/Gitea链接转换为本地file://协议

4. **模式4**: 本地链接 → GitHub链接
   - 同模式2，用于向外分享
   - 将本地file://链接转换为GitHub链接

5. **模式5**: 本地链接 → Gitea链接
   - Gitea链接应该是组织内分享文档的默认方式
   - 将本地file://链接转换为Gitea链接

6. **模式6**: Obsidian内链 → Gitea链接
   - 用于解决遗漏文档的链接替换问题
   - 将 `![[图片名]]` 格式转换为HTML格式的Gitea链接

7. **模式7**: Markdown图片 → HTML格式
   - 将 `![title](link)` 格式转换为HTML `<img>` 标签
   - 支持居中对齐和样式设置

8. **模式8**: 组合模式
   - 依次执行模式6和模式7
   - 一次性完成Obsidian内链到HTML格式的完整转换

#### 使用方法
```bash
python markdown-attachment.py <folder_path> <mode>
```

#### 参数说明
- `folder_path`: 需要处理的文件夹路径
- `mode`: 转换模式（1-8）

#### 使用示例
```bash
# 将GitHub链接转换为Gitea链接
python markdown-attachment.py "/path/to/docs" 1

# 将本地链接转换为GitHub链接
python markdown-attachment.py "/path/to/docs" 4

# 将Obsidian内链转换为HTML格式
python markdown-attachment.py "/path/to/docs" 8
```

#### 特性
- ✅ **智能文件过滤**：自动跳过特定文件，避免处理脚本代码
- ✅ **正则表达式匹配**：精确识别各种链接格式
- ✅ **路径格式处理**：自动处理不同操作系统的路径分隔符
- ✅ **HTML格式生成**：支持生成带样式的HTML图片标签
- ✅ **批量处理**：递归处理文件夹中的所有Markdown文件

---

### 2. obsidian_link_replace.py - Obsidian链接替换工具

#### 功能说明
- 专门处理Obsidian笔记中的图片链接格式转换
- 支持GitHub、Gitea、本地文件等多种链接格式
- 提供5种核心转换模式，简化链接管理流程

#### 主要功能

##### 🔄 五种转换模式

1. **模式1**: GitHub链接 → tmcodeserver链接
   - 将GitHub原始文件链接转换为内网服务器链接
   - 支持upstream-master和master分支

2. **模式2**: tmcodeserver链接 → GitHub链接
   - 将内网服务器链接转换回GitHub链接
   - 用于外网分享文档

3. **模式3**: 远程链接 → 本地文件链接
   - 将GitHub/tmcodeserver链接转换为本地file://协议
   - 支持离线文档查看

4. **模式4**: 本地链接 → GitHub链接
   - 将本地file://链接转换为GitHub链接
   - 便于文档外网分享

5. **模式5**: 本地链接 → tmcodeserver链接
   - 将本地file://链接转换为内网服务器链接
   - 适用于组织内部文档分享

#### 使用方法
```bash
python obsidian_link_replace.py <folder_path> <mode>
```

#### 参数说明
- `folder_path`: 需要处理的文件夹路径
- `mode`: 转换模式（1-5）

#### 使用示例
```bash
# 将GitHub链接转换为内网链接
python obsidian_link_replace.py "/path/to/docs" 1

# 将内网链接转换为GitHub链接
python obsidian_link_replace.py "/path/to/docs" 2

# 将远程链接转换为本地链接
python obsidian_link_replace.py "/path/to/docs" 3
```

#### 特性
- ✅ **简化操作**：专注于核心链接转换功能
- ✅ **UTF-8编码支持**：正确处理中文字符和特殊字符
- ✅ **LF换行符**：统一使用LF换行符，确保跨平台兼容性
- ✅ **实时反馈**：处理每个文件后显示转换完成信息

## 📊 使用场景对比

| 场景 | 推荐脚本 | 推荐模式 | 说明 |
|------|----------|----------|------|
| 内外网文档迁移 | markdown-attachment.py | 模式1/2 | 功能更全面，支持多种链接格式 |
| 简单链接转换 | obsidian_link_replace.py | 对应模式 | 操作简单，专注核心功能 |
| Obsidian内链处理 | markdown-attachment.py | 模式6/8 | 独有功能，处理Obsidian特殊格式 |
| 批量格式标准化 | markdown-attachment.py | 模式7/8 | 支持转换为标准HTML格式 |

## 🚀 快速开始

1. **选择合适的脚本**
   ```bash
   # 功能全面的处理
   python markdown-attachment.py --help
   
   # 简单快速的转换
   python obsidian_link_replace.py --help
   ```

2. **执行转换**
   ```bash
   # 示例：将文档从外网格式转换为内网格式
   python markdown-attachment.py "/path/to/docs" 1
   ```

3. **验证结果**
   - 检查转换后的文档链接是否正确
   - 确认图片是否能正常显示

## ⚠️ 注意事项

1. **备份文件**: 执行转换前请备份原始文档，避免数据丢失
2. **路径格式**: 确保文件夹路径有效且包含Markdown文件（.md后缀）
3. **编码问题**: 所有脚本都使用UTF-8编码，确保中文字符正确处理
4. **权限要求**: 确保对目标文件夹有读写权限
5. **文件过滤**: markdown-attachment.py会自动跳过特定的系统文件

## 🔧 技术架构

- **编程语言**: Python 3.x
- **核心依赖**: os, sys, re
- **设计模式**: 函数式编程，单一职责原则
- **正则表达式**: 精确匹配各种链接格式
- **文件处理**: 批量递归处理，保持文件结构

## 📄 许可证

本项目为内部工具，仅供学习和个人使用。

---

## 🆘 常见问题

### Q: 两个脚本有什么区别？
A: markdown-attachment.py功能更全面，支持8种模式和Obsidian特殊格式；obsidian_link_replace.py更简洁，专注于5种核心转换。

### Q: 如何处理Obsidian的内链格式？
A: 使用markdown-attachment.py的模式6或模式8，可以将 `![[图片名]]` 转换为HTML格式。

### Q: 转换后链接无法显示图片怎么办？
A: 检查目标服务器或本地路径是否可访问，确认图片文件是否存在于指定位置。

### Q: 可以自定义转换规则吗？
A: 可以修改脚本中的正则表达式和替换规则，建议先备份原始脚本。

---

*最后更新：2025-07-13*