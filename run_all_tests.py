#!/usr/bin/env python3
"""
自动化测试完整执行脚本
按顺序执行所有测试：Chrome -> Edge -> BDD测试
提供详细的执行提示和结果反馈
"""

import os
import sys
import subprocess
import time
import argparse
from datetime import datetime
from pathlib import Path
from loguru import logger


class TestExecutor:
    """测试执行器 - 统一管理所有测试的执行"""

    def __init__(self, auto_start=True):
        """
        初始化测试执行器

        Args:
            auto_start: 是否自动开始执行（默认True）
        """
        self.auto_start = auto_start
        self.project_root = Path(__file__).parent
        self.reports_dir = self.project_root / "reports"
        self.screenshots_dir = self.project_root / "screenshots"
        
        # 确保目录存在
        self.reports_dir.mkdir(exist_ok=True)
        self.screenshots_dir.mkdir(exist_ok=True)
        
        # 配置日志
        logger.remove()
        logger.add(
            sys.stdout,
            format="{time:HH:mm:ss} | {level} | {message}",
            level="INFO",
            colorize=True
        )
    
    def print_banner(self, title: str, width: int = 80):
        """打印标题横幅"""
        print("\n" + "=" * width)
        print(f"{title:^{width}}")
        print("=" * width + "\n")
    
    def print_step_info(self, message: str):
        """打印步骤信息"""
        print(f"\n🔔 {message}")
        print("-" * 60)
    
    def execute_script(self, script_name: str, description: str) -> bool:
        """
        执行Python脚本
        
        Args:
            script_name: 脚本文件名
            description: 脚本描述
            
        Returns:
            执行是否成功
        """
        try:
            script_path = self.project_root / script_name
            
            if not script_path.exists():
                logger.error(f"❌ 脚本文件不存在: {script_path}")
                return False
            
            logger.info(f"🚀 开始执行 {description}...")
            logger.info(f"📄 脚本路径: {script_path}")
            
            # 执行脚本
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=str(self.project_root),
                capture_output=False,  # 让输出直接显示在控制台
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"✅ {description} 执行成功！")
                return True
            else:
                logger.error(f"❌ {description} 执行失败！返回码: {result.returncode}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 执行 {description} 时发生异常: {e}")
            return False
    
    def get_latest_report_files(self):
        """获取最新生成的报告文件信息"""
        try:
            # 查找Chrome报告
            chrome_reports = list(self.reports_dir.glob("Chrome_Detailed_Test_Report_*.html"))
            chrome_report = max(chrome_reports, key=lambda x: x.stat().st_mtime) if chrome_reports else None
            
            # 查找Edge报告
            edge_reports = list(self.reports_dir.glob("Edge_Detailed_Test_Report_*.html"))
            edge_report = max(edge_reports, key=lambda x: x.stat().st_mtime) if edge_reports else None
            
            # 查找BDD报告
            bdd_reports = list(self.reports_dir.glob("bdd_tests_*.html"))
            bdd_report = max(bdd_reports, key=lambda x: x.stat().st_mtime) if bdd_reports else None
            
            return chrome_report, edge_report, bdd_report
            
        except Exception as e:
            logger.error(f"获取报告文件信息时出错: {e}")
            return None, None, None
    
    def get_latest_screenshot_dirs(self):
        """获取最新生成的截图目录信息"""
        try:
            # 查找Chrome截图目录
            chrome_dirs = list(self.screenshots_dir.glob("chrome_tests_*"))
            chrome_dir = max(chrome_dirs, key=lambda x: x.stat().st_mtime) if chrome_dirs else None
            
            # 查找Edge截图目录
            edge_dirs = list(self.screenshots_dir.glob("edge_tests_*"))
            edge_dir = max(edge_dirs, key=lambda x: x.stat().st_mtime) if edge_dirs else None
            
            # 查找BDD截图目录
            bdd_dirs = list(self.screenshots_dir.glob("bdd_tests_*"))
            bdd_dir = max(bdd_dirs, key=lambda x: x.stat().st_mtime) if bdd_dirs else None
            
            return chrome_dir, edge_dir, bdd_dir
            
        except Exception as e:
            logger.error(f"获取截图目录信息时出错: {e}")
            return None, None, None
    
    def run_all_tests(self):
        """执行所有测试的主流程"""
        start_time = datetime.now()
        
        self.print_banner("🚀 自动化测试完整执行流程")
        
        print("""
📋 测试执行计划:
  1️⃣  第一题 - Chrome浏览器测试
  2️⃣  第一题 - Edge浏览器测试
  3️⃣  第二题 - BDD行为驱动测试
        """)

        if self.auto_start:
            # 自动开始执行
            print("🚀 自动开始执行测试...")
            time.sleep(2)  # 给用户2秒时间查看计划
        else:
            # 等待用户确认（保留原有功能）
            input("按回车键开始执行测试...")
        
        # ==================== 第一题：Chrome测试 ====================
        self.print_step_info("这是第一题的Chrome版本")
        
        chrome_success = self.execute_script("run_chrome_tests.py", "Chrome浏览器测试")
        
        if chrome_success:
            print("\n✅ Chrome版本已完成！")
        else:
            print("\n❌ Chrome测试执行失败，但继续执行后续测试...")
        
        time.sleep(2)  # 短暂等待
        
        # ==================== 第一题：Edge测试 ====================
        self.print_step_info("Chrome版本已完成，现在用Edge进行测试")
        
        edge_success = self.execute_script("run_edge_tests.py", "Edge浏览器测试")
        
        if edge_success:
            print("\n✅ Edge版本已完成！")
        else:
            print("\n❌ Edge测试执行失败，但继续执行后续测试...")
        
        # 第一题完成总结
        self.print_banner("📊 第一题执行完成")
        
        chrome_report, edge_report, _ = self.get_latest_report_files()
        chrome_screenshots, edge_screenshots, _ = self.get_latest_screenshot_dirs()
        
        print("🎉 第一题已完成！")
        print("\n📄 测试报告位置:")
        print(f"  📁 reports目录: {self.reports_dir}")
        if chrome_report:
            print(f"  🌐 Chrome报告: {chrome_report.name}")
        if edge_report:
            print(f"  🌐 Edge报告: {edge_report.name}")
        
        print("\n📸 截图位置:")
        print(f"  📁 screenshots目录: {self.screenshots_dir}")
        if chrome_screenshots:
            print(f"  📷 Chrome截图: {chrome_screenshots.name}/")
        if edge_screenshots:
            print(f"  📷 Edge截图: {edge_screenshots.name}/")
        
        time.sleep(3)  # 等待用户查看
        
        # ==================== 第二题：BDD测试 ====================
        self.print_step_info("现在开始进行第二题")
        
        bdd_success = self.execute_script("run_bdd_tests.py", "BDD行为驱动测试")
        
        # 第二题完成总结
        self.print_banner("📊 第二题执行完成")
        
        _, _, bdd_report = self.get_latest_report_files()
        _, _, bdd_screenshots = self.get_latest_screenshot_dirs()
        
        if bdd_success:
            print("🎉 第二题已完成！")
        else:
            print("⚠️  第二题执行完成（可能有部分问题）")
        
        print("\n📄 测试报告位置:")
        print(f"  📁 reports目录: {self.reports_dir}")
        if bdd_report:
            print(f"  📊 BDD报告: {bdd_report.name}")
        
        print("\n📸 截图位置:")
        print(f"  📁 screenshots目录: {self.screenshots_dir}")
        if bdd_screenshots:
            print(f"  📷 BDD截图: {bdd_screenshots.name}/")
        
        # ==================== 总体执行总结 ====================
        end_time = datetime.now()
        duration = end_time - start_time
        
        self.print_banner("🏁 所有测试执行完成")
        
        print(f"⏱️  总执行时间: {duration}")
        print(f"📅 完成时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 执行结果统计
        success_count = sum([chrome_success, edge_success, bdd_success])
        total_count = 3
        
        print(f"\n📊 执行结果统计:")
        print(f"  ✅ 成功: {success_count}/{total_count}")
        print(f"  ❌ 失败: {total_count - success_count}/{total_count}")
        print(f"  📈 成功率: {success_count/total_count*100:.1f}%")
        
        print(f"\n💡 提示:")
        print(f"  - 所有报告文件都在 reports/ 目录下")
        print(f"  - 所有截图文件都在 screenshots/ 目录下")
        print(f"  - 可以用浏览器打开HTML报告查看详细结果")
        
        return success_count == total_count


def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(
        description="自动化测试完整执行脚本",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python run_all_tests.py              # 自动执行所有测试
  python run_all_tests.py --manual     # 需要手动确认后执行
  python run_all_tests.py --help       # 显示帮助信息
        """
    )
    parser.add_argument(
        '--manual',
        action='store_true',
        help='需要手动按回车确认后才开始执行测试（默认自动执行）'
    )

    args = parser.parse_args()

    try:
        # 根据参数决定是否自动开始
        auto_start = not args.manual
        executor = TestExecutor(auto_start=auto_start)
        success = executor.run_all_tests()

        if success:
            print("\n🎉 所有测试执行成功！")
            sys.exit(0)
        else:
            print("\n⚠️  部分测试执行失败，请查看上述日志信息。")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断了测试执行")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 执行过程中发生未预期的错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
