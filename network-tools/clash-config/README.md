# Clash配置文件处理工具集

本项目包含两个Python脚本，用于处理Clash for Windows的配置文件转换和合并。

## 📄 脚本概述

### 1. yml2json.py - YAML到JSON转换工具

#### 功能说明
- 将Clash的YAML配置文件转换为JSON格式
- 支持完整的YAML结构转换，包括代理配置、分组配置、规则等
- 提供详细的中文错误提示和使用说明
- 具备完整的参数验证和错误处理机制

#### 使用方法
```bash
python yml2json.py <yaml_file_path> <json_file_path>
```

#### 参数说明
- `yaml_file_path`: 输入的YAML文件路径
- `json_file_path`: 输出的JSON文件路径

#### 使用示例
```bash
# 转换单个配置文件
python yml2json.py glados.yml glados.json

# 转换带中文名称的文件
python yml2json.py "飞鸟云.yml" "飞鸟云.json"
```

#### 特性
- ✅ 支持UTF-8编码，正确处理中文字符
- ✅ 完整保留YAML文件的所有配置信息
- ✅ 智能错误检测和友好的中文提示
- ✅ 自动验证文件格式和路径有效性
- ✅ 提供详细的使用说明和帮助信息

---

### 2. yaml_merger.py - 多配置文件合并工具

#### 功能说明
这是一个功能强大的YAML配置文件合并工具，能够将多个代理配置文件合并为一个统一的Clash配置文件。

#### 主要功能

##### 🔄 四阶段处理流程
1. **阶段一：YAML到JSON转换**
   - 自动调用yml2json.py转换所有源文件
   - 支持并发转换提高效率
   - 实时验证转换结果

2. **阶段二：代理配置提取**
   - 从转换后的JSON文件中提取所有代理配置
   - 自动处理重复代理名称冲突
   - 验证代理配置的完整性和有效性

3. **阶段三：智能分组配置**
   - **AI-Proxy分组**：根据地区代码自动筛选特定地区的代理
   - **Auto分组**：包含所有代理的自动测试分组

4. **阶段四：最终配置生成**
   - 合并所有配置到模板文件
   - 生成带日期的最终配置文件
   - 完整的配置验证和质量检查

##### 🌍 支持的地区筛选
AI-Proxy分组支持以下地区的自动筛选：
- 🇺🇸 美国 (US, USA, United States)
- 🇬🇧 英国 (UK, United Kingdom, Britain)
- 🇨🇦 加拿大 (CA, Canada)
- 🇯🇵 日本 (JP, Japan)
- 🇸🇬 新加坡 (SG, Singapore)
- 🇹🇼 台湾 (TW, Taiwan)
- 🇻🇳 越南 (VN, Vietnam)

##### 📁 文件结构要求
```
工作目录/
├── yml2json.py                 # YAML转换脚本
├── yaml_merger.py              # 主合并脚本
├── all-in-one-template.json    # 配置模板文件
├── glados.yml                  # GLaDOS配置文件
├── xeno.yml                    # Xeno配置文件
├── 飞鸟云.yml                   # 飞鸟云配置文件
└── all-in-one-YYYYMMDD.json    # 生成的最终配置文件
```

#### 使用方法
```bash
python yaml_merger.py
```

#### 配置自定义
```python
# 示例：添加新的地区匹配模式
merger = YamlToJsonMerger()
merger.add_ai_proxy_pattern(r'(?i).*(德国|DE|Germany).*')
merger.add_ai_proxy_pattern(r'(?i).*(法国|FR|France).*')
```

#### 输出文件命名
- 格式：`all-in-one-YYYYMMDD.json`
- 示例：`all-in-one-20250713.json`
- 每天生成的文件名都不同，便于版本管理

#### 特性亮点
- ✅ **智能编码处理**：自动处理UTF-8/GBK编码问题
- ✅ **正则表达式扩展**：支持自定义地区匹配模式
- ✅ **详细日志记录**：完整的执行日志和错误追踪
- ✅ **配置验证**：多层次的配置文件验证机制
- ✅ **错误恢复**：智能的错误处理和恢复策略
- ✅ **模块化设计**：面向对象的清晰代码结构

## 📊 处理统计示例

最新执行统计：
```
总代理数量: 312
├── GLaDOS: 45 个代理
├── Xeno: 216 个代理
└── 飞鸟云: 51 个代理

分组配置:
├── AI-Proxy分组: 103 个代理
└── Auto分组: 312 个代理
```

## 🚀 快速开始

1. **准备文件**
   ```bash
   # 确保以下文件存在于同一目录
   ls *.yml *.json *.py
   ```

2. **执行转换**
   ```bash
   # 单文件转换
   python yml2json.py glados.yml glados.json
   
   # 批量合并
   python yaml_merger.py
   ```

3. **查看结果**
   ```bash
   # 检查生成的配置文件
   ls all-in-one-*.json
   
   # 查看执行日志
   tail -f merger.log
   ```

## 📝 日志文件

- **merger.log**: 详细的执行日志，包含所有阶段的处理信息
- 支持中文日志记录，便于问题诊断
- 实时记录代理数量、分组配置等统计信息

## ⚠️ 注意事项

1. **文件编码**：确保所有YAML文件使用UTF-8编码
2. **文件路径**：避免使用包含特殊字符的路径
3. **模板文件**：不要修改`all-in-one-template.json`的基础结构
4. **依赖环境**：需要安装PyYAML库 (`pip install PyYAML`)

## 🔧 技术架构

- **编程语言**: Python 3.7+
- **核心依赖**: PyYAML, json, re, subprocess
- **设计模式**: 面向对象设计，单一职责原则
- **错误处理**: 多层次异常捕获和友好错误提示
- **日志系统**: 分离式文件和控制台日志记录

## 📄 许可证

本项目为内部工具，仅供学习和个人使用。

---

## 🆘 常见问题

### Q: 转换失败怎么办？
A: 检查merger.log文件中的详细错误信息，通常是编码或文件路径问题。

### Q: 如何添加新的地区匹配？
A: 在yaml_merger.py中的main()函数里添加自定义模式：
```python
merger.add_ai_proxy_pattern(r'(?i).*(你的地区|CODE).*')
```

### Q: 生成的配置文件在哪里？
A: 在脚本同目录下，文件名格式为`all-in-one-YYYYMMDD.json`。

---

*最后更新：2025-07-13*