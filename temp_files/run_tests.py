#!/usr/bin/env python3
"""
自动化测试运行脚本
支持多种测试运行模式和配置选项
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_command(cmd, description=""):
    """运行命令并处理结果"""
    print(f"\n{'='*60}")
    print(f"执行: {description}")
    print(f"命令: {' '.join(cmd)}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)
        
        if result.stdout:
            print("输出:")
            print(result.stdout)
        
        if result.stderr:
            print("错误:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} 成功完成")
        else:
            print(f"❌ {description} 失败 (返回码: {result.returncode})")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 执行命令时出错: {e}")
        return False

def run_basic_tests():
    """运行基础功能测试"""
    cmd = [sys.executable, "-m", "pytest", "tests/test_basic_functionality.py", "-v"]
    return run_command(cmd, "基础功能测试")

def run_all_tests():
    """运行所有测试"""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-v"]
    return run_command(cmd, "所有测试")

def run_smoke_tests():
    """运行冒烟测试"""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-m", "smoke", "-v"]
    return run_command(cmd, "冒烟测试")

def run_bdd_tests():
    """运行BDD测试"""
    cmd = [sys.executable, "run_bdd_tests.py"]
    return run_command(cmd, "BDD Cucumber测试")

def run_ui_tests():
    """运行UI测试"""
    cmd = [sys.executable, "-m", "pytest", "tests/", "-m", "ui", "-v"]
    return run_command(cmd, "UI测试")

def generate_report():
    """生成测试报告"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/test_report_{timestamp}.html"
    
    cmd = [
        sys.executable, "-m", "pytest", 
        "tests/", 
        f"--html={report_file}",
        "--self-contained-html",
        "-v"
    ]
    
    success = run_command(cmd, f"生成测试报告到 {report_file}")
    
    if success:
        print(f"\n📊 测试报告已生成: {report_file}")
    
    return success

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="自动化测试运行脚本")
    parser.add_argument("--mode", "-m", 
                       choices=["basic", "all", "smoke", "bdd", "ui", "report"],
                       default="basic",
                       help="测试运行模式")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细输出")
    
    args = parser.parse_args()
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    自动化测试运行脚本                        ║
║                                                              ║
║  模式: {args.mode:<10}                                      ║
║  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S'):<10}                                      ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # 确保必要的目录存在
    os.makedirs("../reports", exist_ok=True)
    os.makedirs("../screenshots", exist_ok=True)
    
    success = False
    
    if args.mode == "basic":
        success = run_basic_tests()
    elif args.mode == "all":
        success = run_all_tests()
    elif args.mode == "smoke":
        success = run_smoke_tests()
    elif args.mode == "bdd":
        success = run_bdd_tests()
    elif args.mode == "ui":
        success = run_ui_tests()
    elif args.mode == "report":
        success = generate_report()
    
    print(f"\n{'='*60}")
    if success:
        print("🎉 测试执行成功完成！")
        exit_code = 0
    else:
        print("❌ 测试执行失败！")
        exit_code = 1
    
    print(f"{'='*60}")
    
    return exit_code

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
