# COM组件分析工具

> COM (Component Object Model) 组件差异分析和管理工具集

## 📋 工具列表

### com_diff.py - COM组件差异分析工具

专业的COM组件版本比较工具，用于分析新旧版本COM组件之间的CLSID和TLBID差异。

#### ✨ 主要功能

- **🔍 自动化分析**: 使用mt.exe自动从COM组件DLL生成manifest文件
- **📊 差异对比**: 详细比较新旧版本的CLSID和TLBID变化
- **📈 统计报告**: 生成完整的变化统计信息和变化率分析
- **🛡️ 错误处理**: 完善的文件验证和异常处理机制
- **🧹 临时文件管理**: 可选择保留或自动清理临时manifest文件

#### 🚀 使用方法

##### 基本用法
```bash
python com_diff.py old_component.dll new_component.dll
```

##### 高级用法
```bash
# 保留临时manifest文件
python com_diff.py --keep-temp old_component.dll new_component.dll

# 指定输出目录
python com_diff.py --output-dir temp/ old_component.dll new_component.dll

# 完整路径示例
python com_diff.py "C:/old/SmartView.dll" "C:/new/SmartView.dll"
```

#### 📋 命令参数

| 参数 | 描述 | 必需 |
|------|------|------|
| `old_dll` | 旧版本COM组件DLL文件路径 | 是 |
| `new_dll` | 新版本COM组件DLL文件路径 | 是 |
| `--keep-temp` | 保留生成的临时manifest文件 | 否 |
| `--output-dir` | manifest文件输出目录（默认当前目录） | 否 |

#### 📊 输出报告

工具会生成两个详细的对比表格：

1. **CLSID变化对比表**
   - 显示每个COM类的CLSID前后变化
   - 标记相同的ID（带*符号）
   - 提供变化统计和变化率

2. **TLBID变化对比表**
   - 显示每个COM类的TLBID前后变化
   - 标记相同的ID（带*符号）
   - 提供变化统计和变化率

#### 📦 依赖要求

- **Python 3.6+**
- **tabulate** 库：用于表格格式化输出
  ```bash
  pip install tabulate
  ```
- **Windows SDK** 或 **Visual Studio Build Tools**：提供mt.exe工具

#### 🔧 工作原理

1. **文件验证**: 检查输入的DLL文件是否存在且有效
2. **工具初始化**: 自动查找并初始化mt.exe工具
3. **Manifest生成**: 使用mt.exe从DLL文件生成XML manifest
4. **数据解析**: 解析manifest文件提取COM类信息
5. **差异分析**: 比较新旧版本的CLSID和TLBID
6. **报告生成**: 生成详细的对比表格和统计信息
7. **清理工作**: 可选择清理或保留临时文件

#### ⚠️ 注意事项

- 需要安装Windows SDK或Visual Studio Build Tools以获得mt.exe工具
- 确保COM组件DLL文件可读且未被其他程序占用
- 工具会自动查找系统中的mt.exe，优先选择x64版本
- 生成的manifest文件为XML格式，可手动查看详细信息

#### 💡 使用场景

- **版本升级验证**: 确认COM组件升级后的ID变化情况
- **兼容性分析**: 分析组件更新对现有系统的影响
- **部署规划**: 为COM组件部署制定详细的变更计划
- **问题诊断**: 快速定位COM组件相关的兼容性问题

#### 📝 输出示例

```
==========================================
CLSID 变化对比表
==========================================
+------------------+----------------------+----------------------+
| Description      | Old CLSID           | New CLSID           |
+==================+======================+======================+
| ComponentA*      | {12345678-1234-...} | {12345678-1234-...} |
| ComponentB       | {87654321-4321-...} | {11111111-1111-...} |
+------------------+----------------------+----------------------+

[统计] CLSID 统计:
  总计比较: 2 条
  相同: 1 条
  不同: 1 条
  变化率: 50.0%
```

---

*该工具专为Windows COM组件开发和维护场景设计，提供专业级的组件差异分析能力。*