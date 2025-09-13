#!/usr/bin/env python3
"""
优化的测试运行器
按照指定顺序执行测试：
1. Chrome登录测试 -> Chrome异常测试
2. Edge登录测试 -> Edge异常测试  
3. Edge IE登录测试 -> Edge IE异常测试
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from loguru import logger


class OptimizedTestRunner:
    """优化的测试运行器类"""
    
    def __init__(self):
        """初始化测试运行器"""
        self.project_root = Path(__file__).parent
        self.reports_dir = self.project_root / "reports"
        self.screenshots_dir = self.project_root / "screenshots"
        
    def clean(self):
        """清理之前的测试结果"""
        logger.info("=== 开始清理测试环境 ===")
        
        # 清理报告目录
        if self.reports_dir.exists():
            shutil.rmtree(self.reports_dir)
            logger.info("已清理报告目录")
        
        # 清理截图目录
        if self.screenshots_dir.exists():
            shutil.rmtree(self.screenshots_dir)
            logger.info("已清理截图目录")
        
        # 重新创建必要目录
        self.reports_dir.mkdir(exist_ok=True)
        self.screenshots_dir.mkdir(exist_ok=True)
        
        logger.info("=== 测试环境清理完成 ===")
    
    def install_dependencies(self):
        """安装测试依赖"""
        logger.info("检查并安装测试依赖...")
        
        try:
            # 安装pytest-ordering
            subprocess.run([
                sys.executable, "-m", "pip", "install", "pytest-ordering"
            ], check=True, capture_output=True, text=True)
            
            logger.info("✅ pytest-ordering 安装完成")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ 依赖安装失败: {e}")
            return False
    
    def run_chrome_tests(self):
        """运行Chrome浏览器测试"""
        logger.info("=== 开始执行Chrome浏览器测试 ===")
        
        # Chrome登录测试
        logger.info("1. 执行Chrome登录页面测试...")
        cmd_login = [
            sys.executable, "-m", "pytest",
            "tests/test_selenium_basic.py::TestSeleniumBasic::test_01_chrome_login_page_validation",
            "-v", "-s",
            "--html=reports/chrome_login_report.html",
            "--self-contained-html"
        ]
        
        result_login = self._run_test_command(cmd_login, "Chrome登录测试")
        
        if result_login:
            logger.info("✅ Chrome登录测试完成")
            
            # Chrome异常测试
            logger.info("2. 执行Chrome异常页面测试...")
            cmd_exceptions = [
                sys.executable, "-m", "pytest",
                "tests/test_selenium_basic.py::TestSeleniumBasic::test_02_chrome_exceptions_page_validation",
                "-v", "-s",
                "--html=reports/chrome_exceptions_report.html",
                "--self-contained-html"
            ]
            
            result_exceptions = self._run_test_command(cmd_exceptions, "Chrome异常测试")
            
            if result_exceptions:
                logger.info("✅ Chrome所有测试完成")
                return True
        
        return False
    
    def run_edge_tests(self):
        """运行Edge浏览器测试"""
        logger.info("=== 开始执行Edge浏览器测试 ===")
        
        # Edge登录测试
        logger.info("3. 执行Edge登录页面测试...")
        cmd_login = [
            sys.executable, "-m", "pytest",
            "tests/test_selenium_basic.py::TestSeleniumBasic::test_03_edge_login_page_validation",
            "-v", "-s",
            "--html=reports/edge_login_report.html",
            "--self-contained-html"
        ]
        
        result_login = self._run_test_command(cmd_login, "Edge登录测试")
        
        if result_login:
            logger.info("✅ Edge登录测试完成")
            
            # Edge异常测试
            logger.info("4. 执行Edge异常页面测试...")
            cmd_exceptions = [
                sys.executable, "-m", "pytest",
                "tests/test_selenium_basic.py::TestSeleniumBasic::test_04_edge_exceptions_page_validation",
                "-v", "-s",
                "--html=reports/edge_exceptions_report.html",
                "--self-contained-html"
            ]
            
            result_exceptions = self._run_test_command(cmd_exceptions, "Edge异常测试")
            
            if result_exceptions:
                logger.info("✅ Edge所有测试完成")
                return True
        
        return False
    
    def run_edge_ie_tests(self):
        """运行Edge IE模式测试"""
        logger.info("=== 开始执行Edge IE模式测试 ===")
        
        # Edge IE登录测试
        logger.info("5. 执行Edge IE登录页面测试...")
        cmd_login = [
            sys.executable, "-m", "pytest",
            "tests/test_selenium_basic.py::TestSeleniumBasic::test_05_edge_ie_login_page_validation",
            "-v", "-s",
            "--html=reports/edge_ie_login_report.html",
            "--self-contained-html"
        ]
        
        result_login = self._run_test_command(cmd_login, "Edge IE登录测试")
        
        if result_login:
            logger.info("✅ Edge IE登录测试完成")
            
            # Edge IE异常测试
            logger.info("6. 执行Edge IE异常页面测试...")
            cmd_exceptions = [
                sys.executable, "-m", "pytest",
                "tests/test_selenium_basic.py::TestSeleniumBasic::test_06_edge_ie_exceptions_page_validation",
                "-v", "-s",
                "--html=reports/edge_ie_exceptions_report.html",
                "--self-contained-html"
            ]
            
            result_exceptions = self._run_test_command(cmd_exceptions, "Edge IE异常测试")
            
            if result_exceptions:
                logger.info("✅ Edge IE所有测试完成")
                return True
        
        return False
    
    def _run_test_command(self, cmd, test_name):
        """执行测试命令"""
        try:
            env = os.environ.copy()
            env["PYTHONPATH"] = str(self.project_root)
            
            logger.info(f"执行命令: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd, 
                cwd=self.project_root,
                env=env,
                text=True,
                capture_output=False
            )
            
            if result.returncode == 0:
                logger.info(f"✅ {test_name} 执行成功")
                return True
            else:
                logger.error(f"❌ {test_name} 执行失败")
                return False
                
        except Exception as e:
            logger.error(f"❌ {test_name} 执行出错: {e}")
            return False
    
    def generate_summary(self, chrome_success, edge_success, edge_ie_success):
        """生成测试总结"""
        logger.info("=== 生成测试总结 ===")
        
        # 检查生成的文件
        report_files = list(self.reports_dir.glob("*.html"))
        screenshot_files = list(self.screenshots_dir.glob("*.png"))
        
        summary = f"""
{'='*60}
优化的Selenium自动化测试执行总结
{'='*60}
执行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
执行顺序: Chrome -> Edge -> Edge IE (每个浏览器先登录后异常)

测试结果:
{'✅ 成功' if chrome_success else '❌ 失败'} Chrome浏览器测试 (登录 + 异常)
{'✅ 成功' if edge_success else '❌ 失败'} Edge浏览器测试 (登录 + 异常)  
{'✅ 成功' if edge_ie_success else '❌ 失败'} Edge IE模式测试 (登录 + 异常)

生成的文件:
📊 HTML报告: {len(report_files)} 个
📸 截图文件: {len(screenshot_files)} 个

优化特性:
✅ 按指定顺序执行测试
✅ 登录测试增加用户名/密码输入等待
✅ 异常测试每步之间等待1秒
✅ 分浏览器生成独立报告
✅ 详细的步骤截图记录
{'='*60}
"""
        
        print(summary)
        
        # 保存总结到文件
        summary_file = self.reports_dir / "optimized_test_summary.txt"
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        logger.info(f"测试总结已保存到: {summary_file}")
    
    def run(self):
        """运行完整的优化测试流程"""
        # 配置日志
        logger.remove()
        logger.add(
            sys.stdout,
            format="{time:HH:mm:ss} | {level} | {message}",
            level="INFO",
            colorize=True
        )
        
        start_time = datetime.now()
        
        try:
            # 1. 清理环境
            self.clean()
            
            # 2. 安装依赖
            if not self.install_dependencies():
                return False
            
            # 3. 按顺序执行测试
            chrome_success = self.run_chrome_tests()
            edge_success = self.run_edge_tests()
            edge_ie_success = self.run_edge_ie_tests()
            
            # 4. 生成总结
            self.generate_summary(chrome_success, edge_success, edge_ie_success)
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info(f"总执行时间: {duration}")
            
            return chrome_success and edge_success and edge_ie_success
            
        except KeyboardInterrupt:
            logger.warning("测试被用户中断")
            return False
        except Exception as e:
            logger.error(f"测试执行出错: {e}")
            return False


def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                优化的Selenium自动化测试                      ║
║                                                              ║
║  执行顺序:                                                   ║
║  1. Chrome登录测试 -> Chrome异常测试                         ║
║  2. Edge登录测试 -> Edge异常测试                             ║
║  3. Edge IE登录测试 -> Edge IE异常测试                       ║
║                                                              ║
║  优化特性:                                                   ║
║  - 登录测试: 用户名/密码输入后等待1秒                        ║
║  - 异常测试: 每个步骤之间等待1秒                             ║
║  - 分浏览器生成独立报告                                      ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    runner = OptimizedTestRunner()
    success = runner.run()
    
    if success:
        print("\n🎉 所有优化测试执行成功！请查看生成的报告和截图。")
        sys.exit(0)
    else:
        print("\n⚠️ 部分测试执行失败，请查看详细日志。")
        sys.exit(1)


if __name__ == "__main__":
    main()
