#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示如何通过API调用本项目的测试功能

这个脚本展示了README.md中提到的各种API调用方式
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def demo_chrome_tests():
    """演示Chrome测试API调用"""
    print("🚀 演示Chrome测试API调用...")
    
    try:
        from run_chrome_tests import ChromeTestRunner
        
        # 创建Chrome测试运行器
        chrome_runner = ChromeTestRunner()
        
        # 只生成报告（不执行实际测试，避免启动浏览器）
        print("📊 生成Chrome测试报告...")
        chrome_report = chrome_runner.generate_detailed_test_report(success=True)
        print(f"✅ Chrome报告已生成: {chrome_report}")
        
        return True
        
    except Exception as e:
        print(f"❌ Chrome测试API调用失败: {e}")
        return False

def demo_edge_tests():
    """演示Edge测试API调用"""
    print("\n🚀 演示Edge测试API调用...")

    try:
        from run_edge_tests import EdgeTestRunner

        # 创建Edge测试运行器
        edge_runner = EdgeTestRunner()

        # 只生成报告（不执行实际测试）
        print("📊 生成Edge测试报告...")
        edge_runner._generate_detailed_report()  # Edge使用私有方法
        print(f"✅ Edge报告生成完成")

        return True

    except Exception as e:
        print(f"❌ Edge测试API调用失败: {e}")
        return False

def demo_project_structure():
    """演示项目结构检查"""
    print("\n📁 检查项目结构...")
    
    required_dirs = [
        "config", "pages", "tests", "features", "utils", 
        "reports", "screenshots", "logs"
    ]
    
    required_files = [
        "run_chrome_tests.py", "run_edge_tests.py", "run_bdd_tests.py",
        "run_all_tests.py", "README.md", "config/requirements.txt"
    ]
    
    print("📂 检查必需目录:")
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        status = "✅" if dir_path.exists() else "❌"
        print(f"  {status} {dir_name}/")
    
    print("\n📄 检查必需文件:")
    for file_name in required_files:
        file_path = project_root / file_name
        status = "✅" if file_path.exists() else "❌"
        print(f"  {status} {file_name}")

def demo_config_loading():
    """演示配置加载"""
    print("\n⚙️ 演示配置加载...")
    
    try:
        config_file = project_root / "config" / "config.yaml"
        if config_file.exists():
            print(f"✅ 配置文件存在: {config_file}")
            
            # 尝试读取配置
            import yaml
            with open(config_file, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            print("📋 配置内容预览:")
            for key in config.keys():
                print(f"  - {key}")
                
        else:
            print("❌ 配置文件不存在")
            
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")

def main():
    """主函数"""
    print("=" * 60)
    print("🎯 Auto Test Quiz - API使用演示")
    print("=" * 60)
    
    # 检查项目结构
    demo_project_structure()
    
    # 演示配置加载
    demo_config_loading()
    
    # 演示API调用
    chrome_success = demo_chrome_tests()
    edge_success = demo_edge_tests()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 演示总结:")
    print(f"  Chrome API: {'✅ 成功' if chrome_success else '❌ 失败'}")
    print(f"  Edge API:   {'✅ 成功' if edge_success else '❌ 失败'}")
    print("=" * 60)
    
    print("\n💡 使用提示:")
    print("1. 执行完整测试: python run_all_tests.py")
    print("2. 只执行Chrome: python run_chrome_tests.py")
    print("3. 只执行Edge:   python run_edge_tests.py")
    print("4. 只执行BDD:    python run_bdd_tests.py")
    print("5. 查看报告:     打开 reports/ 目录下的HTML文件")
    print("6. 查看截图:     打开 screenshots/ 目录")

if __name__ == "__main__":
    main()
