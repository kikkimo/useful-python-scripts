#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COM Diff - COM Components Comparison Tool
COM 组件差异分析工具

功能：
- 自动从 COM 组件 DLL 生成 manifest 文件
- 比较新旧版本 COM 组件的 CLSID 和 TLBID 变化
- 生成详细的差异报告和统计信息
- 支持命令行操作，提供完整的错误处理

作者：FangYi
版本：1.0
"""

import xml.etree.ElementTree as ET
import re
import os
import sys
import glob
import subprocess
import tempfile
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from tabulate import tabulate

@dataclass
class ComClass:
    """COM 类信息结构体"""
    description: str
    clsid: str
    tlbid: str
    
    def __post_init__(self):
        # 清理 CLSID 和 TLBID，移除大括号
        self.clsid = self.clsid.strip('{}')
        self.tlbid = self.tlbid.strip('{}')

class ManifestTool:
    """MT.exe 工具包装器"""
    
    def __init__(self):
        self.mt_exe_path: Optional[str] = None
        self._find_mt_exe()
    
    def _find_mt_exe(self) -> None:
        """查找 mt.exe 工具，优先选择 x64 版本"""
        possible_paths = [
            r"C:\Program Files (x86)\Windows Kits\*\bin\*\x64\mt.exe",
            r"C:\Program Files (x86)\Windows Kits\*\bin\*\mt.exe",
            r"C:\Program Files\Windows Kits\*\bin\*\x64\mt.exe", 
            r"C:\Program Files\Windows Kits\*\bin\*\mt.exe"
        ]
        
        for pattern in possible_paths:
            matches = glob.glob(pattern)
            if matches:
                # 按版本号排序，选择最新版本
                matches.sort(reverse=True)
                self.mt_exe_path = matches[0]
                print(f"找到 mt.exe: {self.mt_exe_path}")
                return
        
        raise FileNotFoundError("未找到 mt.exe 工具。请确保已安装 Windows SDK 或 Visual Studio Build Tools")
    
    def generate_manifest(self, dll_path: str, output_path: str) -> bool:
        """
        使用 mt.exe 从 COM 组件 DLL 生成 manifest 文件
        
        Args:
            dll_path: COM 组件 DLL 文件路径
            output_path: 输出的 manifest 文件路径
            
        Returns:
            bool: 是否成功生成
        """
        if not self.mt_exe_path:
            raise RuntimeError("mt.exe 工具未找到")
        
        if not os.path.exists(dll_path):
            raise FileNotFoundError(f"COM 组件文件不存在: {dll_path}")
        
        # 构建 mt.exe 命令
        cmd = [
            self.mt_exe_path,
            f"-tlb:{dll_path}",
            f"-dll:{dll_path}",
            f"-out:{output_path}"
        ]
        
        try:
            print(f"正在生成 manifest 文件: {os.path.basename(dll_path)} -> {os.path.basename(output_path)}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                timeout=60  # 60秒超时
            )
            
            if os.path.exists(output_path):
                print(f"成功生成: {output_path}")
                return True
            else:
                print(f"警告: 命令执行成功但未生成文件: {output_path}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"错误: mt.exe 执行失败")
            print(f"返回码: {e.returncode}")
            print(f"错误输出: {e.stderr}")
            return False
        except subprocess.TimeoutExpired:
            print(f"错误: mt.exe 执行超时")
            return False
        except Exception as e:
            print(f"错误: 执行 mt.exe 时发生异常: {e}")
            return False


class ManifestParser:
    """Manifest 文件解析器"""
    
    def __init__(self):
        self.old_classes: List[ComClass] = []
        self.new_classes: List[ComClass] = []
    
    def parse_manifest(self, file_path: str) -> List[ComClass]:
        """解析 manifest 文件，提取 COM 类信息"""
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 由于文件是单行的，我们需要用正则表达式来解析
            classes = []
            
            # 匹配所有的 comClass 元素
            com_class_pattern = r'<comClass\s+([^>]+)></comClass>'
            matches = re.findall(com_class_pattern, content)
            
            for match in matches:
                # 提取属性
                clsid_match = re.search(r'clsid="([^"]+)"', match)
                tlbid_match = re.search(r'tlbid="([^"]+)"', match)
                desc_match = re.search(r'description="([^"]+)"', match)
                
                if clsid_match and tlbid_match:
                    clsid = clsid_match.group(1)
                    tlbid = tlbid_match.group(1)
                    description = desc_match.group(1).replace(' Class', '') if desc_match else ''
                    
                    # 如果没有 description，我们也添加进去，但 description 为空
                    classes.append(ComClass(
                        description=description,
                        clsid=clsid,
                        tlbid=tlbid
                    ))
            
            return classes
            
        except Exception as e:
            print(f"解析文件 {file_path} 时发生错误: {e}")
            return []
    
    def load_files(self, old_file: str, new_file: str):
        """载入新旧两个 manifest 文件"""
        print(f"正在解析旧文件: {old_file}")
        self.old_classes = self.parse_manifest(old_file)
        old_with_desc = [cls for cls in self.old_classes if cls.description]
        print(f"找到 {len(self.old_classes)} 个 COM 类，其中 {len(old_with_desc)} 个有描述")
        
        print(f"正在解析新文件: {new_file}")
        self.new_classes = self.parse_manifest(new_file)
        new_with_desc = [cls for cls in self.new_classes if cls.description]
        print(f"找到 {len(self.new_classes)} 个 COM 类，其中 {len(new_with_desc)} 个有描述")
    
    def create_clsid_comparison_table(self) -> List[List[str]]:
        """创建 CLSID 对比表格"""
        # 创建描述到类信息的映射（只包含有描述的类）
        old_dict = {cls.description: cls for cls in self.old_classes if cls.description}
        new_dict = {cls.description: cls for cls in self.new_classes if cls.description}
        
        # 获取所有描述的并集
        all_descriptions = set(old_dict.keys()) | set(new_dict.keys())
        
        table_data = []
        for desc in sorted(all_descriptions):
            old_clsid = old_dict.get(desc, ComClass('', '', '')).clsid
            new_clsid = new_dict.get(desc, ComClass('', '', '')).clsid
            
            # 如果前后 CLSID 相同，在描述后添加 * 标记
            display_desc = desc
            if old_clsid and new_clsid and old_clsid == new_clsid:
                display_desc += "*"
            
            table_data.append([display_desc, old_clsid, new_clsid])
        
        return table_data
    
    def create_tlbid_comparison_table(self) -> List[List[str]]:
        """创建 TLBID 对比表格"""
        # 创建描述到类信息的映射（只包含有描述的类）
        old_dict = {cls.description: cls for cls in self.old_classes if cls.description}
        new_dict = {cls.description: cls for cls in self.new_classes if cls.description}
        
        # 获取所有描述的并集
        all_descriptions = set(old_dict.keys()) | set(new_dict.keys())
        
        table_data = []
        for desc in sorted(all_descriptions):
            old_tlbid = old_dict.get(desc, ComClass('', '', '')).tlbid
            new_tlbid = new_dict.get(desc, ComClass('', '', '')).tlbid
            
            # 如果前后 TLBID 相同，在描述后添加 * 标记
            display_desc = desc
            if old_tlbid and new_tlbid and old_tlbid == new_tlbid:
                display_desc += "*"
            
            table_data.append([display_desc, old_tlbid, new_tlbid])
        
        return table_data
    
    def print_comparison_tables(self):
        """打印对比表格"""
        print("\n" + "="*80)
        print("CLSID 变化对比表")
        print("="*80)
        
        clsid_table = self.create_clsid_comparison_table()
        headers = ["Description", "Old CLSID", "New CLSID"]
        print(tabulate(clsid_table, headers=headers, tablefmt="grid"))
        
        # CLSID 统计
        clsid_same_count = 0
        clsid_different_count = 0
        clsid_total = len(clsid_table)
        
        for row in clsid_table:
            old_clsid = row[1]
            new_clsid = row[2]
            if old_clsid and new_clsid and old_clsid == new_clsid:
                clsid_same_count += 1
            elif old_clsid and new_clsid:  # 都不为空才算不同
                clsid_different_count += 1
        
        print(f"\n[统计] CLSID 统计:")
        print(f"  总计比较: {clsid_total} 条")
        print(f"  相同: {clsid_same_count} 条")
        print(f"  不同: {clsid_different_count} 条")
        if clsid_total > 0:
            print(f"  变化率: {clsid_different_count/clsid_total*100:.1f}%")
        
        print("\n" + "="*80)
        print("TLBID 变化对比表")
        print("="*80)
        
        tlbid_table = self.create_tlbid_comparison_table()
        headers = ["Description", "Old TLBID", "New TLBID"]
        print(tabulate(tlbid_table, headers=headers, tablefmt="grid"))
        
        # TLBID 统计
        tlbid_same_count = 0
        tlbid_different_count = 0
        tlbid_total = len(tlbid_table)
        
        for row in tlbid_table:
            old_tlbid = row[1]
            new_tlbid = row[2]
            if old_tlbid and new_tlbid and old_tlbid == new_tlbid:
                tlbid_same_count += 1
            elif old_tlbid and new_tlbid:  # 都不为空才算不同
                tlbid_different_count += 1
        
        print(f"\n[统计] TLBID 统计:")
        print(f"  总计比较: {tlbid_total} 条")
        print(f"  相同: {tlbid_same_count} 条")
        print(f"  不同: {tlbid_different_count} 条")
        if tlbid_total > 0:
            print(f"  变化率: {tlbid_different_count/tlbid_total*100:.1f}%")
        
        print("\n说明：带有 * 标记的条目表示前后 ID 相同")

def validate_dll_file(file_path: str) -> bool:
    """
    验证 DLL 文件是否存在且有效
    
    Args:
        file_path: DLL 文件路径
        
    Returns:
        bool: 文件是否有效
    """
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在: {file_path}")
        return False
    
    if not os.path.isfile(file_path):
        print(f"错误: 路径不是文件: {file_path}")
        return False
    
    if not file_path.lower().endswith('.dll'):
        print(f"警告: 文件扩展名不是 .dll: {file_path}")
    
    try:
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            print(f"错误: 文件大小为 0: {file_path}")
            return False
    except OSError as e:
        print(f"错误: 无法获取文件信息: {file_path}, {e}")
        return False
    
    return True


def parse_arguments() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        prog="com_diff",
        description="COM Diff - COM 组件差异分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python com_diff.py old_component.dll new_component.dll
  python com_diff.py "C:/old/SmartView.dll" "C:/new/SmartView.dll"
  python com_diff.py --keep-temp --output-dir temp/ old.dll new.dll
  
功能说明:
  自动使用 mt.exe 从 COM 组件 DLL 生成 manifest 文件，
  然后比较新旧版本的 CLSID 和 TLBID 差异，生成详细报告。
        """
    )
    
    parser.add_argument(
        "old_dll",
        help="旧版本 COM 组件 DLL 文件路径"
    )
    
    parser.add_argument(
        "new_dll", 
        help="新版本 COM 组件 DLL 文件路径"
    )
    
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="保留临时生成的 manifest 文件"
    )
    
    parser.add_argument(
        "--output-dir",
        default=".",
        help="manifest 文件输出目录 (默认: 当前目录)"
    )
    
    return parser.parse_args()


def main():
    """主函数"""
    try:
        # 解析命令行参数
        args = parse_arguments()
        
        # 验证输入文件
        print("=" * 60)
        print("COM Diff - COM 组件差异分析工具 v1.0")
        print("=" * 60)
        
        print("\n1. 验证输入文件...")
        if not validate_dll_file(args.old_dll):
            sys.exit(1)
        if not validate_dll_file(args.new_dll):
            sys.exit(1)
        
        print(f"旧版本 DLL: {args.old_dll}")
        print(f"新版本 DLL: {args.new_dll}")
        
        # 创建输出目录
        output_dir = Path(args.output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化工具
        print("\n2. 初始化 mt.exe 工具...")
        try:
            mt_tool = ManifestTool()
        except FileNotFoundError as e:
            print(f"错误: {e}")
            sys.exit(1)
        
        # 生成临时 manifest 文件
        print("\n3. 生成 manifest 文件...")
        old_manifest = output_dir / "old_manifest.xml"
        new_manifest = output_dir / "new_manifest.xml"
        
        success_old = mt_tool.generate_manifest(args.old_dll, str(old_manifest))
        success_new = mt_tool.generate_manifest(args.new_dll, str(new_manifest))
        
        if not success_old or not success_new:
            print("错误: 无法生成 manifest 文件")
            sys.exit(1)
        
        # 解析和比较
        print("\n4. 解析和比较 COM 类信息...")
        parser = ManifestParser()
        parser.load_files(str(old_manifest), str(new_manifest))
        parser.print_comparison_tables()
        
        # 清理临时文件
        if not args.keep_temp:
            print("\n5. 清理临时文件...")
            try:
                if old_manifest.exists():
                    old_manifest.unlink()
                    print(f"删除: {old_manifest}")
                if new_manifest.exists():
                    new_manifest.unlink() 
                    print(f"删除: {new_manifest}")
            except OSError as e:
                print(f"警告: 清理临时文件时出错: {e}")
        else:
            print(f"\n临时文件保留在: {output_dir}")
            print(f"  旧版本 manifest: {old_manifest}")
            print(f"  新版本 manifest: {new_manifest}")
        
        print("\n比较完成!")
        
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: 程序执行时发生异常: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()