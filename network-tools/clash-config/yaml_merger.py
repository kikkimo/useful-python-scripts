#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YAML配置文件合并为JSON配置工具

功能说明：
1. 将多个YAML配置文件转换为JSON格式
2. 合并代理配置到统一的模板文件中
3. 配置AI-Proxy和Auto代理分组
4. 生成最终的Clash配置文件

作者：Claude AI Assistant
创建时间：2025-07-13
"""

import os
import sys
import json
import yaml
import re
import subprocess
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging
from datetime import datetime


class YamlToJsonMerger:
    """YAML配置文件合并工具类"""
    
    def __init__(self, work_dir: str = None):
        """
        初始化合并工具
        
        Args:
            work_dir: 工作目录，默认为当前脚本所在目录
        """
        self.work_dir = Path(work_dir) if work_dir else Path(__file__).parent
        self.setup_logging()
        
        # 配置文件路径
        self.yml2json_script = self.work_dir / "yml2json.py"
        self.template_file = self.work_dir / "all-in-one-template.json"
        
        # 生成带日期的输出文件名：all-in-one-yyyymmdd.json
        current_date = datetime.now().strftime("%Y%m%d")
        self.output_file = self.work_dir / f"all-in-one-{current_date}.json"
        
        # 源文件配置
        self.source_files = {
            "glados": {
                "yml": self.work_dir / "glados.yml",
                "json": self.work_dir / "glados.json"
            },
            "xeno": {
                "yml": self.work_dir / "xeno.yml", 
                "json": self.work_dir / "xeno.json"
            },
            "feiniao": {
                "yml": self.work_dir / "飞鸟云.yml",
                "json": self.work_dir / "飞鸟云.json"
            }
        }
        
        # AI-Proxy分组的地区匹配配置（支持正则表达式扩展）
        self.ai_proxy_patterns = [
            # 美国相关
            r'(?i).*(美国|US|USA|United\s*States).*',
            # 英国相关  
            r'(?i).*(英国|UK|United\s*Kingdom|Britain).*',
            # 加拿大相关
            r'(?i).*(加拿大|CA|Canada).*',
            # 日本相关
            r'(?i).*(日本|JP|Japan).*',
            # 新加坡相关
            r'(?i).*(新加坡|SG|Singapore).*',
            # 台湾相关
            r'(?i).*(台湾|TW|Taiwan).*',
            # 越南相关
            r'(?i).*(越南|VN|Vietnam).*'
        ]
        
        # 统计信息
        self.stats = {
            "total_proxies": 0,
            "ai_proxy_count": 0,
            "auto_proxy_count": 0,
            "conversion_errors": [],
            "merge_errors": []
        }
    
    def setup_logging(self):
        """设置日志配置"""
        # 创建日志格式器
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        # 文件处理器（UTF-8编码）
        file_handler = logging.FileHandler(self.work_dir / 'merger.log', encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        # 控制台处理器（使用系统默认编码，避免特殊字符）
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        
        # 配置根日志器
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def add_ai_proxy_pattern(self, pattern: str):
        """
        添加新的AI-Proxy地区匹配模式
        
        Args:
            pattern: 正则表达式模式字符串
        """
        try:
            # 验证正则表达式的有效性
            re.compile(pattern)
            self.ai_proxy_patterns.append(pattern)
            self.logger.info(f"已添加新的AI-Proxy匹配模式: {pattern}")
        except re.error as e:
            self.logger.error(f"无效的正则表达式模式 '{pattern}': {e}")
            raise ValueError(f"无效的正则表达式模式: {e}")
    
    def set_ai_proxy_patterns(self, patterns: List[str]):
        """
        设置AI-Proxy地区匹配模式列表
        
        Args:
            patterns: 正则表达式模式列表
        """
        valid_patterns = []
        for pattern in patterns:
            try:
                re.compile(pattern)
                valid_patterns.append(pattern)
            except re.error as e:
                self.logger.error(f"跳过无效的正则表达式模式 '{pattern}': {e}")
        
        self.ai_proxy_patterns = valid_patterns
        self.logger.info(f"已设置AI-Proxy匹配模式，共{len(valid_patterns)}个模式")
    
    def validate_prerequisites(self) -> bool:
        """
        验证前置条件
        
        Returns:
            bool: 验证是否通过
        """
        self.logger.info("开始验证前置条件...")
        
        # 检查yml2json.py脚本是否存在
        if not self.yml2json_script.exists():
            self.logger.error(f"yml2json.py脚本不存在: {self.yml2json_script}")
            return False
        
        # 检查模板文件是否存在
        if not self.template_file.exists():
            self.logger.error(f"模板文件不存在: {self.template_file}")
            return False
        
        # 检查源YAML文件是否存在
        missing_files = []
        for name, files in self.source_files.items():
            if not files["yml"].exists():
                missing_files.append(str(files["yml"]))
        
        if missing_files:
            self.logger.error(f"以下源文件不存在: {missing_files}")
            return False
        
        self.logger.info("前置条件验证通过")
        return True
    
    def convert_yaml_to_json(self) -> bool:
        """
        阶段一：将所有YAML文件转换为JSON格式
        
        Returns:
            bool: 转换是否成功
        """
        self.logger.info("=== 阶段一：开始YAML到JSON转换 ===")
        
        success_count = 0
        total_count = len(self.source_files)
        
        for name, files in self.source_files.items():
            yml_file = files["yml"]
            json_file = files["json"]
            
            self.logger.info(f"转换 {name}: {yml_file.name} -> {json_file.name}")
            
            try:
                # 调用yml2json.py脚本进行转换
                cmd = [sys.executable, str(self.yml2json_script), str(yml_file), str(json_file)]
                
                # 使用二进制模式避免编码问题，然后手动解码
                result = subprocess.run(cmd, capture_output=True)
                
                # 手动处理输出编码，避免线程编码错误
                if result.stdout:
                    try:
                        stdout = result.stdout.decode('utf-8')
                    except UnicodeDecodeError:
                        stdout = result.stdout.decode('gbk', errors='replace')
                else:
                    stdout = ''
                
                if result.stderr:
                    try:
                        stderr = result.stderr.decode('utf-8')
                    except UnicodeDecodeError:
                        stderr = result.stderr.decode('gbk', errors='replace')
                else:
                    stderr = ''
                
                # 创建一个模拟的result对象
                class ResultWrapper:
                    def __init__(self, returncode, stdout, stderr):
                        self.returncode = returncode
                        self.stdout = stdout
                        self.stderr = stderr
                
                result = ResultWrapper(result.returncode, stdout, stderr)
                
                if result.returncode == 0:
                    self.logger.info(f"[OK] {name} 转换成功")
                    
                    # 验证转换后的JSON文件
                    if self.validate_json_file(json_file):
                        success_count += 1
                    else:
                        self.stats["conversion_errors"].append(f"{name}: JSON格式验证失败")
                else:
                    error_msg = f"{name}: {result.stderr}"
                    self.logger.error(f"[FAIL] {name} 转换失败: {error_msg}")
                    self.stats["conversion_errors"].append(error_msg)
                    
            except Exception as e:
                error_msg = f"{name}: {str(e)}"
                self.logger.error(f"[ERROR] {name} 转换异常: {error_msg}")
                self.stats["conversion_errors"].append(error_msg)
        
        success = success_count == total_count
        self.logger.info(f"YAML转换完成: {success_count}/{total_count} 成功")
        return success
    
    def validate_json_file(self, json_file: Path) -> bool:
        """
        验证JSON文件的有效性
        
        Args:
            json_file: JSON文件路径
            
        Returns:
            bool: 验证是否通过
        """
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查必要的字段
            if 'proxies' not in data:
                self.logger.warning(f"{json_file.name} 缺少 proxies 字段")
                return False
            
            proxy_count = len(data['proxies'])
            self.logger.info(f"{json_file.name} 包含 {proxy_count} 个代理节点")
            
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"{json_file.name} JSON格式错误: {e}")
            return False
        except Exception as e:
            self.logger.error(f"验证 {json_file.name} 时发生错误: {e}")
            return False
    
    def extract_proxies(self) -> List[Dict[str, Any]]:
        """
        阶段二：从转换后的JSON文件中提取所有代理配置
        
        Returns:
            List[Dict]: 所有代理配置的列表
        """
        self.logger.info("=== 阶段二：开始提取代理配置 ===")
        
        all_proxies = []
        proxy_names = set()  # 用于检测重复名称
        
        for name, files in self.source_files.items():
            json_file = files["json"]
            
            if not json_file.exists():
                self.logger.error(f"JSON文件不存在: {json_file}")
                continue
                
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                proxies = data.get('proxies', [])
                self.logger.info(f"从 {name} 提取 {len(proxies)} 个代理")
                
                # 处理代理配置
                for proxy in proxies:
                    proxy_name = proxy.get('name', '')
                    
                    # 跳过无效的代理配置
                    if not proxy_name or not self.is_valid_proxy(proxy):
                        continue
                    
                    # 处理重复名称
                    if proxy_name in proxy_names:
                        original_name = proxy_name
                        counter = 1
                        while proxy_name in proxy_names:
                            proxy_name = f"{original_name}_dup_{counter}"
                            counter += 1
                        proxy['name'] = proxy_name
                        self.logger.warning(f"重复代理名称，重命名: {original_name} -> {proxy_name}")
                    
                    proxy_names.add(proxy_name)
                    all_proxies.append(proxy)
                    
            except Exception as e:
                error_msg = f"提取 {name} 代理配置失败: {str(e)}"
                self.logger.error(error_msg)
                self.stats["merge_errors"].append(error_msg)
        
        self.stats["total_proxies"] = len(all_proxies)
        self.logger.info(f"代理提取完成，共获得 {len(all_proxies)} 个有效代理")
        return all_proxies
    
    def is_valid_proxy(self, proxy: Dict[str, Any]) -> bool:
        """
        验证代理配置的有效性
        
        Args:
            proxy: 代理配置字典
            
        Returns:
            bool: 是否为有效代理
        """
        required_fields = ['name', 'type', 'server', 'port']
        
        for field in required_fields:
            if field not in proxy or not proxy[field]:
                return False
        
        # 检查端口是否为有效数字
        try:
            port = int(proxy['port'])
            if not (1 <= port <= 65535):
                return False
        except (ValueError, TypeError):
            return False
        
        return True
    
    def load_template(self) -> Dict[str, Any]:
        """
        加载模板配置文件
        
        Returns:
            Dict: 模板配置数据
        """
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
                template = json.load(f)
            self.logger.info("模板文件加载成功")
            return template
        except Exception as e:
            self.logger.error(f"加载模板文件失败: {e}")
            raise
    
    def configure_ai_proxy_group(self, proxies: List[Dict[str, Any]], template: Dict[str, Any]) -> List[str]:
        """
        阶段三：配置AI-Proxy分组
        
        Args:
            proxies: 所有代理配置列表
            template: 模板配置
            
        Returns:
            List[str]: 匹配AI-Proxy条件的代理名称列表
        """
        self.logger.info("=== 阶段三：开始配置AI-Proxy分组 ===")
        
        ai_proxy_names = []
        compiled_patterns = []
        
        # 编译正则表达式模式
        for pattern in self.ai_proxy_patterns:
            try:
                compiled_patterns.append(re.compile(pattern))
            except re.error as e:
                self.logger.error(f"正则表达式编译失败: {pattern}, 错误: {e}")
        
        # 遍历所有代理，匹配AI-Proxy条件
        for proxy in proxies:
            proxy_name = proxy['name']
            
            # 检查是否匹配任一模式
            for pattern in compiled_patterns:
                if pattern.search(proxy_name):
                    ai_proxy_names.append(proxy_name)
                    self.logger.debug(f"AI-Proxy匹配: {proxy_name}")
                    break
        
        # 更新模板中的AI-Proxy分组
        for group in template.get('proxy-groups', []):
            if group.get('name') == 'AI-Proxy':
                group['proxies'] = ai_proxy_names
                break
        else:
            self.logger.warning("模板中未找到AI-Proxy分组")
        
        self.stats["ai_proxy_count"] = len(ai_proxy_names)
        self.logger.info(f"AI-Proxy分组配置完成，包含 {len(ai_proxy_names)} 个代理")
        
        # 输出匹配的代理名称（用于调试）
        if ai_proxy_names:
            self.logger.info("AI-Proxy分组包含的代理:")
            for name in ai_proxy_names[:10]:  # 只显示前10个
                self.logger.info(f"  - {name}")
            if len(ai_proxy_names) > 10:
                self.logger.info(f"  ... 还有 {len(ai_proxy_names) - 10} 个代理")
        
        return ai_proxy_names
    
    def configure_auto_group(self, proxies: List[Dict[str, Any]], template: Dict[str, Any]) -> List[str]:
        """
        配置Auto分组（包含所有代理）
        
        Args:
            proxies: 所有代理配置列表
            template: 模板配置
            
        Returns:
            List[str]: 所有代理名称列表
        """
        self.logger.info("开始配置Auto分组...")
        
        all_proxy_names = [proxy['name'] for proxy in proxies]
        
        # 更新模板中的Auto分组
        for group in template.get('proxy-groups', []):
            if group.get('name') == 'Auto':
                group['proxies'] = all_proxy_names
                break
        else:
            self.logger.warning("模板中未找到Auto分组")
        
        self.stats["auto_proxy_count"] = len(all_proxy_names)
        self.logger.info(f"Auto分组配置完成，包含 {len(all_proxy_names)} 个代理")
        
        return all_proxy_names
    
    def generate_final_config(self, proxies: List[Dict[str, Any]], template: Dict[str, Any]) -> bool:
        """
        阶段四：生成最终配置文件
        
        Args:
            proxies: 所有代理配置列表
            template: 配置好分组的模板
            
        Returns:
            bool: 生成是否成功
        """
        self.logger.info("=== 阶段四：开始生成最终配置文件 ===")
        
        try:
            # 将代理配置添加到模板中
            final_config = template.copy()
            final_config['proxies'] = proxies
            
            # 保存最终配置文件
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(final_config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"最终配置文件已生成: {self.output_file}")
            
            # 验证生成的配置文件
            if self.validate_final_config():
                self.logger.info("[OK] 最终配置文件验证通过")
                return True
            else:
                self.logger.error("[FAIL] 最终配置文件验证失败")
                return False
                
        except Exception as e:
            self.logger.error(f"生成最终配置文件失败: {e}")
            return False
    
    def validate_final_config(self) -> bool:
        """
        验证最终配置文件的正确性
        
        Returns:
            bool: 验证是否通过
        """
        self.logger.info("开始验证最终配置文件...")
        
        try:
            with open(self.output_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 验证JSON格式
            self.logger.info("[OK] JSON格式验证通过")
            
            # 验证必要字段
            required_fields = ['proxies', 'proxy-groups', 'rules']
            for field in required_fields:
                if field not in config:
                    self.logger.error(f"[FAIL] 缺少必要字段: {field}")
                    return False
            
            # 验证代理数量
            proxy_count = len(config['proxies'])
            if proxy_count != self.stats["total_proxies"]:
                self.logger.error(f"[FAIL] 代理数量不匹配: 期望{self.stats['total_proxies']}，实际{proxy_count}")
                return False
            
            # 验证分组配置
            groups = config.get('proxy-groups', [])
            ai_proxy_group = None
            auto_group = None
            
            for group in groups:
                if group.get('name') == 'AI-Proxy':
                    ai_proxy_group = group
                elif group.get('name') == 'Auto':
                    auto_group = group
            
            if not ai_proxy_group:
                self.logger.error("[FAIL] 未找到AI-Proxy分组")
                return False
            
            if not auto_group:
                self.logger.error("[FAIL] 未找到Auto分组")
                return False
            
            # 验证分组代理数量
            ai_proxy_count = len(ai_proxy_group.get('proxies', []))
            auto_proxy_count = len(auto_group.get('proxies', []))
            
            if ai_proxy_count != self.stats["ai_proxy_count"]:
                self.logger.error(f"[FAIL] AI-Proxy分组代理数量不匹配: 期望{self.stats['ai_proxy_count']}，实际{ai_proxy_count}")
                return False
            
            if auto_proxy_count != self.stats["auto_proxy_count"]:
                self.logger.error(f"[FAIL] Auto分组代理数量不匹配: 期望{self.stats['auto_proxy_count']}，实际{auto_proxy_count}")
                return False
            
            self.logger.info("[OK] 配置文件结构验证通过")
            self.logger.info(f"[OK] 代理节点总数: {proxy_count}")
            self.logger.info(f"[OK] AI-Proxy分组: {ai_proxy_count} 个代理")
            self.logger.info(f"[OK] Auto分组: {auto_proxy_count} 个代理")
            
            return True
            
        except json.JSONDecodeError as e:
            self.logger.error(f"[FAIL] JSON格式错误: {e}")
            return False
        except Exception as e:
            self.logger.error(f"[FAIL] 验证过程中发生错误: {e}")
            return False
    
    def print_summary(self):
        """打印执行摘要"""
        self.logger.info("=" * 50)
        self.logger.info("执行摘要")
        self.logger.info("=" * 50)
        self.logger.info(f"总代理数量: {self.stats['total_proxies']}")
        self.logger.info(f"AI-Proxy分组: {self.stats['ai_proxy_count']} 个代理")
        self.logger.info(f"Auto分组: {self.stats['auto_proxy_count']} 个代理")
        
        if self.stats["conversion_errors"]:
            self.logger.error("转换错误:")
            for error in self.stats["conversion_errors"]:
                self.logger.error(f"  - {error}")
        
        if self.stats["merge_errors"]:
            self.logger.error("合并错误:")
            for error in self.stats["merge_errors"]:
                self.logger.error(f"  - {error}")
        
        self.logger.info(f"最终配置文件: {self.output_file}")
        self.logger.info("=" * 50)
    
    def run(self) -> bool:
        """
        执行完整的合并流程
        
        Returns:
            bool: 执行是否成功
        """
        self.logger.info("开始执行YAML配置文件合并任务")
        
        try:
            # 验证前置条件
            if not self.validate_prerequisites():
                return False
            
            # 阶段一：YAML到JSON转换
            if not self.convert_yaml_to_json():
                self.logger.error("YAML转换阶段失败")
                return False
            
            # 阶段二：提取代理配置
            all_proxies = self.extract_proxies()
            if not all_proxies:
                self.logger.error("未能提取到任何有效代理配置")
                return False
            
            # 加载模板
            template = self.load_template()
            
            # 阶段三：配置代理分组
            self.configure_ai_proxy_group(all_proxies, template)
            self.configure_auto_group(all_proxies, template)
            
            # 阶段四：生成最终配置
            if not self.generate_final_config(all_proxies, template):
                self.logger.error("生成最终配置失败")
                return False
            
            self.logger.info("[SUCCESS] 所有阶段执行成功")
            return True
            
        except Exception as e:
            self.logger.error(f"执行过程中发生异常: {e}")
            return False
        finally:
            self.print_summary()


def main():
    """主函数"""
    print("YAML配置文件合并工具")
    print("=" * 50)
    
    # 创建合并工具实例
    merger = YamlToJsonMerger()
    
    # 示例：添加自定义的AI-Proxy匹配模式
    # merger.add_ai_proxy_pattern(r'(?i).*(德国|DE|Germany).*')
    # merger.add_ai_proxy_pattern(r'(?i).*(法国|FR|France).*')
    
    # 执行合并任务
    success = merger.run()
    
    if success:
        print("\n[SUCCESS] 任务执行成功！")
        print(f"最终配置文件已生成: {merger.output_file}")
    else:
        print("\n[FAILED] 任务执行失败！")
        print("请检查错误日志以获取详细信息。")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())