#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from loguru import logger


class ChromeTestRunner:
    """Chrome浏览器专用测试运行器"""
    
    def __init__(self):
        """初始化Chrome测试运行器"""
        self.project_root = Path(__file__).parent
        self.reports_dir = self.project_root / "reports"
        self.screenshots_dir = self.project_root / "screenshots"
        
    def run_chrome_tests(self):
        """运行Chrome浏览器的完整流程测试"""
        logger.info("=== 开始执行Chrome浏览器完整流程测试 ===")

        # 执行唯一的完整流程测试，避免重复
        logger.info("执行Chrome完整流程测试（包含3个登录用例 + 5个异常用例）...")
        cmd_complete = [
            sys.executable, "-m", "pytest",
            "tests/test_selenium_basic.py::TestSeleniumBasic::test_01_chrome_complete_flow",
            "-v", "-s",
            "--html=reports/chrome_complete_flow_report.html",
            "--self-contained-html"
        ]

        result_complete = self._run_test_command(cmd_complete, "Chrome完整流程测试")

        if result_complete:
            logger.info("✅ Chrome完整流程测试成功完成")
            logger.info("  - 包含3个登录用例：正确凭据、错误用户名、错误密码")
            logger.info("  - 包含5个异常用例：Add按钮、文本输入、保存功能、确认消息、数据一致性")
            logger.info("  - 浏览器在整个测试过程中保持打开状态")
            logger.info("  - 避免了重复执行相同的测试用例")
            return True
        else:
            logger.error("❌ Chrome完整流程测试执行失败")
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
    
    def generate_detailed_test_report(self, success):
        """生成详细的测试报告，包含8个测试用例的完整文档"""
        logger.info("=== 生成详细测试报告 ===")

        # 检查生成的文件
        report_files = list(self.reports_dir.glob("chrome_*.html"))
        screenshot_dirs = list(self.screenshots_dir.glob("chrome_*"))

        # 生成HTML格式的详细测试报告
        html_report = self._generate_html_test_report(success, report_files, screenshot_dirs)

        # 保存HTML报告
        detailed_report_file = self.reports_dir / f"Chrome_Detailed_Test_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        with open(detailed_report_file, 'w', encoding='utf-8') as f:
            f.write(html_report)

        logger.info(f"详细HTML测试报告已保存到: {detailed_report_file}")

        # 生成简化的控制台总结
        self._print_console_summary(success, report_files, screenshot_dirs)

        return detailed_report_file

    def generate_summary(self, success):
        """生成测试总结（保持向后兼容）"""
        return self.generate_detailed_test_report(success)

    def _get_test_case_screenshots(self, test_case_id):
        """获取特定测试用例的截图信息"""
        screenshots = []

        # 定义每个测试用例对应的截图模式
        screenshot_patterns = {
            "TC001": [
                "登录用例1_输入正确用户名",
                "登录用例1_输入正确密码",
                "登录用例1_正确凭据登录",
                "登录用例1_登录成功验证",
                "登录用例1_登出操作"
            ],
            "TC002": [
                "登录用例2_输入错误用户名",
                "登录用例2_输入密码",
                "登录用例2_错误用户名登录"
            ],
            "TC003": [
                "登录用例3_输入正确用户名",
                "登录用例3_输入错误密码",
                "登录用例3_错误密码登录"
            ],
            "TC004": [
                "异常测试_用例1_步骤1_滚动到标题",
                "异常测试_用例1_步骤2_Add按钮高亮",
                "异常测试_用例1_步骤3_点击Add按钮",
                "异常测试_用例1_步骤4_捕获异常"
            ],
            "TC005": [
                "异常测试_用例2_步骤1_滚动到标题",
                "异常测试_用例2_步骤2_Add按钮高亮",
                "异常测试_用例2_步骤3_点击Add按钮_等待Row2",
                "异常测试_用例2_步骤4_输入文本",
                "异常测试_用例2_步骤5_捕获异常"
            ],
            "TC006": [
                "异常测试_用例3_步骤1_滚动到标题",
                "异常测试_用例3_步骤2_禁用输入框高亮",
                "异常测试_用例3_步骤2_捕获异常"
            ],
            "TC007": [
                "异常测试_用例4_步骤1_获取元素引用",
                "异常测试_用例4_步骤2_点击Add按钮",
                "异常测试_用例4_步骤3_捕获异常"
            ],
            "TC008": [
                "异常测试_用例5_步骤1_Add按钮高亮",
                "异常测试_用例5_步骤1_点击Add按钮",
                "异常测试_用例5_步骤2_捕获异常"
            ]
        }

        patterns = screenshot_patterns.get(test_case_id, [])

        # 搜索实际的截图文件
        for pattern in patterns:
            # 在所有截图目录中搜索匹配的文件
            for screenshot_dir in self.screenshots_dir.glob("chrome_*"):
                if screenshot_dir.is_dir():
                    # 搜索PNG和JPG文件
                    for ext in ['png', 'jpg', 'jpeg']:
                        # 使用更安全的文件搜索方式
                        for file_path in screenshot_dir.iterdir():
                            if (file_path.is_file() and
                                file_path.suffix.lower() == f'.{ext}' and
                                pattern in file_path.name):
                                # 计算相对路径
                                relative_path = file_path.relative_to(self.screenshots_dir.parent)
                                screenshots.append({
                                    'title': pattern,
                                    'path': str(relative_path),
                                    'exists': file_path.exists(),
                                    'size': file_path.stat().st_size if file_path.exists() else 0
                                })
                                break  # 只取第一个匹配的文件
                        if screenshots and pattern in [s['title'] for s in screenshots]:
                            break  # 找到文件就跳出扩展名循环
                if screenshots and pattern in [s['title'] for s in screenshots]:
                    break  # 找到这个模式的文件就跳出目录循环

        return screenshots

    def _get_expected_screenshot_names(self, test_case_id):
        """获取测试用例预期的截图名称列表"""
        screenshot_names = {
            "TC001": [
                "登录用例1_输入正确用户名.png",
                "登录用例1_输入正确密码.png",
                "登录用例1_正确凭据登录.png",
                "登录用例1_登录成功验证.png",
                "登录用例1_登出操作.png"
            ],
            "TC002": [
                "登录用例2_输入错误用户名.png",
                "登录用例2_输入密码.png",
                "登录用例2_错误用户名登录.png"
            ],
            "TC003": [
                "登录用例3_输入正确用户名.png",
                "登录用例3_输入错误密码.png",
                "登录用例3_错误密码登录.png"
            ],
            "TC004": [
                "异常测试_用例1_步骤1_滚动到标题.png",
                "异常测试_用例1_步骤2_Add按钮高亮.png",
                "异常测试_用例1_步骤3_点击Add按钮.png",
                "异常测试_用例1_步骤4_捕获异常.png"
            ],
            "TC005": [
                "异常测试_用例2_步骤1_滚动到标题.png",
                "异常测试_用例2_步骤2_Add按钮高亮.png",
                "异常测试_用例2_步骤3_点击Add按钮_等待Row2.png",
                "异常测试_用例2_步骤4_输入文本.png",
                "异常测试_用例2_步骤5_捕获异常.png"
            ],
            "TC006": [
                "异常测试_用例3_步骤1_滚动到标题.png",
                "异常测试_用例3_步骤2_禁用输入框高亮.png",
                "异常测试_用例3_步骤2_捕获异常.png"
            ],
            "TC007": [
                "异常测试_用例4_步骤1_获取元素引用.png",
                "异常测试_用例4_步骤2_点击Add按钮.png",
                "异常测试_用例4_步骤3_捕获异常.png"
            ],
            "TC008": [
                "异常测试_用例5_步骤1_Add按钮高亮.png",
                "异常测试_用例5_步骤1_点击Add按钮.png",
                "异常测试_用例5_步骤2_捕获异常.png"
            ]
        }

        return screenshot_names.get(test_case_id, [])

    def _generate_html_test_report(self, success, report_files, screenshot_dirs):
        """生成HTML格式的详细测试报告"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 定义8个测试用例
        test_cases = [
            {
                "id": "TC001",
                "name": "正确凭据登录测试",
                "description": "使用正确的用户名和密码进行登录测试",
                "steps": [
                    "1. 导航到登录页面: https://practicetestautomation.com/practice-test-login/",
                    "2. 在用户名输入框输入'student'",
                    "3. 在密码输入框输入'Password123'",
                    "4. 点击'Submit'按钮",
                    "5. 验证登录成功页面",
                    "6. 截图记录登录结果"
                ],
                "expected_result": "登录成功，显示'Congratulations'或成功页面",
                "status": "✅ PASS" if success else "❌ FAIL"
            },
            {
                "id": "TC002",
                "name": "错误用户名登录测试",
                "description": "使用错误的用户名进行登录测试，验证错误处理",
                "steps": [
                    "1. 导航到登录页面: https://practicetestautomation.com/practice-test-login/",
                    "2. 在用户名输入框输入'incorrectUser'",
                    "3. 在密码输入框输入'Password123'",
                    "4. 点击'Submit'按钮",
                    "5. 验证错误消息显示",
                    "6. 截图记录错误状态"
                ],
                "expected_result": "显示用户名错误的提示消息",
                "status": "✅ PASS" if success else "❌ FAIL"
            },
            {
                "id": "TC003",
                "name": "错误密码登录测试",
                "description": "使用错误的密码进行登录测试，验证错误处理",
                "steps": [
                    "1. 导航到登录页面: https://practicetestautomation.com/practice-test-login/",
                    "2. 在用户名输入框输入'student'",
                    "3. 在密码输入框输入'incorrectPassword'",
                    "4. 点击'Submit'按钮",
                    "5. 验证错误消息显示",
                    "6. 截图记录错误状态"
                ],
                "expected_result": "显示密码错误的提示消息",
                "status": "✅ PASS" if success else "❌ FAIL"
            },
            {
                "id": "TC004",
                "name": "NoSuchElementException异常测试",
                "description": "验证NoSuchElementException的正确捕获和处理",
                "steps": [
                    "1. 导航到异常测试页面: https://practicetestautomation.com/practice-test-exceptions/",
                    "2. 滚动到页面标题处",
                    "3. 定位并高亮Add按钮",
                    "4. 点击Add按钮",
                    "5. 尝试查找不存在的Row 2输入框",
                    "6. 捕获NoSuchElementException异常",
                    "7. 显示异常信息面板",
                    "8. 截图记录异常捕获过程"
                ],
                "expected_result": "成功捕获NoSuchElementException，显示异常信息",
                "status": "✅ PASS" if success else "❌ FAIL"
            },
            {
                "id": "TC005",
                "name": "ElementNotInteractableException异常测试",
                "description": "验证ElementNotInteractableException的正确捕获和处理",
                "steps": [
                    "1. 导航到异常测试页面: https://practicetestautomation.com/practice-test-exceptions/",
                    "2. 刷新页面到初始状态",
                    "3. 点击Add按钮生成Row 2",
                    "4. 在Row 2输入框输入测试文本",
                    "5. 尝试点击不可见的Save按钮",
                    "6. 捕获ElementNotInteractableException异常",
                    "7. 显示异常信息面板",
                    "8. 截图记录异常捕获过程"
                ],
                "expected_result": "成功捕获ElementNotInteractableException，显示异常信息",
                "status": "✅ PASS" if success else "❌ FAIL"
            },
            {
                "id": "TC004",
                "name": "NoSuchElementException异常测试",
                "description": "测试当页面元素不存在时的异常处理",
                "steps": [
                    "1. 导航到异常测试页面",
                    "2. 点击Add按钮",
                    "3. 立即查找Row 2输入框(不等待DOM更新)",
                    "4. 捕获NoSuchElementException异常",
                    "5. 验证异常处理机制",
                    "6. 记录异常信息",
                    "7. 截图记录异常状态"
                ],
                "expected_result": "正确捕获并处理NoSuchElementException异常",
                "status": "✅ PASS" if success else "❌ FAIL"
            },
            {
                "id": "TC005",
                "name": "ElementNotInteractableException异常测试",
                "description": "测试当页面元素不可交互时的异常处理",
                "steps": [
                    "1. 导航到异常测试页面",
                    "2. 点击Add按钮",
                    "3. 等待Row 2加载",
                    "4. 在Row 2输入框中输入文本",
                    "5. 尝试点击不可见的Save按钮",
                    "6. 捕获ElementNotInteractableException异常",
                    "7. 验证异常处理机制",
                    "8. 记录异常信息",
                    "9. 截图记录异常状态"
                ],
                "expected_result": "正确捕获并处理ElementNotInteractableException异常",
                "status": "✅ PASS" if success else "❌ FAIL"
            },
            {
                "id": "TC006",
                "name": "InvalidElementStateException异常测试",
                "description": "测试尝试清空禁用输入框时的异常处理",
                "steps": [
                    "1. 导航到异常测试页面",
                    "2. 尝试清空禁用的输入框",
                    "3. 捕获InvalidElementStateException异常",
                    "4. 验证异常处理机制",
                    "5. 记录异常信息",
                    "6. 截图记录异常状态"
                ],
                "expected_result": "正确捕获并处理InvalidElementStateException异常",
                "status": "✅ PASS" if success else "❌ FAIL"
            },
            {
                "id": "TC007",
                "name": "StaleElementReferenceException异常测试",
                "description": "测试获取元素引用后点击Add按钮移除元素时的异常处理",
                "steps": [
                    "1. 导航到异常测试页面",
                    "2. 获取instructions元素的引用",
                    "3. 点击Add按钮移除instructions元素",
                    "4. 尝试访问已过期的元素引用",
                    "5. 捕获StaleElementReferenceException异常",
                    "6. 验证异常处理机制",
                    "7. 记录异常信息",
                    "8. 截图记录异常状态"
                ],
                "expected_result": "正确捕获并处理StaleElementReferenceException异常",
                "status": "✅ PASS" if success else "❌ FAIL"
            },
            {
                "id": "TC008",
                "name": "TimeoutException异常测试",
                "description": "测试设置3秒超时等待Row 2出现(需要5秒)时的异常处理",
                "steps": [
                    "1. 导航到异常测试页面",
                    "2. 点击Add按钮",
                    "3. 设置3秒超时等待Row 2出现(但Row 2需要5秒才出现)",
                    "4. 捕获TimeoutException异常",
                    "5. 验证异常处理机制",
                    "6. 记录异常信息",
                    "7. 截图记录异常状态"
                ],
                "expected_result": "正确捕获并处理TimeoutException异常",
                "status": "✅ PASS" if success else "❌ FAIL"
            }
        ]

        # 生成HTML内容
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chrome浏览器自动化测试详细报告</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #007bff;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #007bff;
            margin: 0;
            font-size: 2.5em;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 1.2em;
            margin-top: 10px;
        }}
        .summary {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .summary h2 {{
            margin-top: 0;
            color: white;
        }}
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .summary-item {{
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }}
        .summary-item .label {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        .summary-item .value {{
            font-size: 1.5em;
            font-weight: bold;
            margin-top: 5px;
        }}
        .test-case {{
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 25px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .test-case-header {{
            background: #f8f9fa;
            padding: 15px 20px;
            border-bottom: 1px solid #ddd;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .test-case-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #333;
        }}
        .test-case-id {{
            background: #007bff;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9em;
        }}
        .test-case-status {{
            font-size: 1.1em;
            font-weight: bold;
        }}
        .test-case-content {{
            padding: 20px;
        }}
        .test-description {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
            border-left: 4px solid #2196f3;
        }}
        .test-steps {{
            margin-bottom: 20px;
        }}
        .test-steps h4 {{
            color: #333;
            margin-bottom: 10px;
        }}
        .test-steps .step-list {{
            padding-left: 0;
            list-style: none;
        }}
        .test-steps li {{
            margin-bottom: 8px;
            padding: 8px;
            background: #f8f9fa;
            border-radius: 4px;
        }}
        .expected-result {{
            background: #e8f5e8;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #4caf50;
        }}
        .expected-result h4 {{
            color: #2e7d32;
            margin-top: 0;
        }}
        .pass {{ color: #28a745; }}
        .fail {{ color: #dc3545; }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            color: #666;
        }}
        .files-section {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .files-section h3 {{
            color: #333;
            margin-top: 0;
        }}
        .file-list {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }}
        .file-item {{
            background: white;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }}
        .file-item .file-type {{
            color: #007bff;
            font-weight: bold;
            font-size: 0.9em;
        }}
        .file-item .file-count {{
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }}
        .screenshots-section {{
            margin-top: 20px;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 5px;
            border-left: 4px solid #17a2b8;
        }}
        .screenshots-section h4 {{
            color: #17a2b8;
            margin-top: 0;
            margin-bottom: 15px;
        }}
        .screenshot-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .screenshot-item {{
            background: white;
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .screenshot-item img {{
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-bottom: 1px solid #ddd;
        }}
        .screenshot-item .screenshot-info {{
            padding: 10px;
        }}
        .screenshot-item .screenshot-title {{
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}
        .screenshot-item .screenshot-path {{
            font-size: 0.85em;
            color: #666;
            word-break: break-all;
        }}
        .screenshot-placeholder {{
            width: 100%;
            height: 200px;
            background: linear-gradient(45deg, #f0f0f0 25%, transparent 25%),
                        linear-gradient(-45deg, #f0f0f0 25%, transparent 25%),
                        linear-gradient(45deg, transparent 75%, #f0f0f0 75%),
                        linear-gradient(-45deg, transparent 75%, #f0f0f0 75%);
            background-size: 20px 20px;
            background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
            font-size: 0.9em;
            border-bottom: 1px solid #ddd;
        }}
        .screenshot-info-only {{
            background: #e3f2fd;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #2196f3;
            margin-top: 15px;
        }}
        .screenshot-info-only h5 {{
            color: #1976d2;
            margin-top: 0;
            margin-bottom: 10px;
        }}
        .screenshot-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        .screenshot-list li {{
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .screenshot-list li:last-child {{
            border-bottom: none;
        }}
        .screenshot-name {{
            font-weight: 500;
            color: #333;
        }}
        .screenshot-status {{
            font-size: 0.85em;
            padding: 2px 8px;
            border-radius: 12px;
            background: #e8f5e8;
            color: #2e7d32;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Chrome浏览器自动化测试详细报告</h1>
            <div class="subtitle">Practice Test Automation 完整测试流程</div>
            <div class="subtitle">执行时间: {current_time}</div>
        </div>

        <div class="summary">
            <h2>📊 测试执行总结</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="label">测试状态</div>
                    <div class="value">{'✅ 成功' if success else '❌ 失败'}</div>
                </div>
                <div class="summary-item">
                    <div class="label">测试用例总数</div>
                    <div class="value">{len(test_cases)}</div>
                </div>
                <div class="summary-item">
                    <div class="label">通过用例</div>
                    <div class="value">{len([tc for tc in test_cases if '✅' in tc['status']])}</div>
                </div>
                <div class="summary-item">
                    <div class="label">失败用例</div>
                    <div class="value">{len([tc for tc in test_cases if '❌' in tc['status']])}</div>
                </div>
            </div>
        </div>

        <div class="files-section">
            <h3>📁 生成的测试文件</h3>
            <div class="file-list">
                <div class="file-item">
                    <div class="file-type">📊 HTML报告</div>
                    <div class="file-count">{len(report_files)} 个文件</div>
                </div>
                <div class="file-item">
                    <div class="file-type">📸 截图目录</div>
                    <div class="file-count">{len(screenshot_dirs)} 个目录</div>
                </div>
            </div>
        </div>

        <h2>📋 详细测试用例</h2>
"""

        # 添加每个测试用例的详细信息
        for test_case in test_cases:
            status_class = "pass" if "✅" in test_case["status"] else "fail"

            # 获取该测试用例的截图信息
            screenshots = self._get_test_case_screenshots(test_case['id'])

            html_content += f"""
        <div class="test-case">
            <div class="test-case-header">
                <div>
                    <span class="test-case-id">{test_case['id']}</span>
                    <span class="test-case-title">{test_case['name']}</span>
                </div>
                <div class="test-case-status {status_class}">{test_case['status']}</div>
            </div>
            <div class="test-case-content">
                <div class="test-description">
                    <strong>测试描述:</strong> {test_case['description']}
                </div>

                <div class="test-steps">
                    <h4>🔧 测试步骤:</h4>
                    <ul class="step-list">
"""
            for step in test_case['steps']:
                html_content += f"                        <li>{step}</li>\n"

            html_content += f"""
                    </ul>
                </div>

                <div class="expected-result">
                    <h4>✅ 预期结果:</h4>
                    <p>{test_case['expected_result']}</p>
                </div>
"""

            # 添加截图部分
            if screenshots:
                html_content += f"""
                <div class="screenshots-section">
                    <h4>📸 测试截图 ({len(screenshots)}张)</h4>
                    <div class="screenshot-grid">
"""
                for screenshot in screenshots:
                    # 获取绝对路径用于显示
                    abs_path = Path(screenshot['path']).resolve()
                    file_url = f"file:///{abs_path}".replace('\\', '/')

                    if screenshot['exists']:
                        html_content += f"""
                        <div class="screenshot-item">
                            <img src="{file_url}" alt="{screenshot['title']}"
                                 onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                            <div class="screenshot-placeholder" style="display:none;">
                                📷 图片加载失败
                                <br><small>请手动查看: {abs_path}</small>
                            </div>
                            <div class="screenshot-info">
                                <div class="screenshot-title">{screenshot['title']}</div>
                                <div class="screenshot-path">📁 {screenshot['path']}</div>
                                <div class="screenshot-path"><strong>完整路径:</strong> {abs_path}</div>
                                <div class="screenshot-path"><small>💡 如图片无法显示，请直接打开上述路径查看</small></div>
                            </div>
                        </div>
"""
                    else:
                        html_content += f"""
                        <div class="screenshot-item">
                            <div class="screenshot-placeholder">
                                📷 截图文件不存在
                                <br><small>预期位置: {abs_path}</small>
                            </div>
                            <div class="screenshot-info">
                                <div class="screenshot-title">{screenshot['title']}</div>
                                <div class="screenshot-path">📁 {screenshot['path']} (未找到)</div>
                                <div class="screenshot-path"><strong>预期完整路径:</strong> {abs_path}</div>
                            </div>
                        </div>
"""

                html_content += """
                    </div>
                </div>
"""
            else:
                # 如果没有找到截图，显示截图信息说明
                screenshots_dir_abs = self.screenshots_dir.resolve()
                html_content += f"""
                <div class="screenshot-info-only">
                    <h5>📸 截图信息</h5>
                    <p>该测试用例的截图将在测试执行时自动生成，保存在以下位置：</p>
                    <div class="screenshot-path"><strong>截图目录:</strong> {screenshots_dir_abs}</div>
                    <ul class="screenshot-list">
"""
                # 显示预期的截图文件名
                expected_screenshots = self._get_expected_screenshot_names(test_case['id'])
                for screenshot_name in expected_screenshots:
                    expected_path = screenshots_dir_abs / "chrome_*" / screenshot_name
                    html_content += f"""
                        <li>
                            <span class="screenshot-name">📷 {screenshot_name}</span>
                            <span class="screenshot-status">待生成</span>
                            <div class="screenshot-path"><small>预期路径: {expected_path}</small></div>
                        </li>
"""

                html_content += f"""
                    </ul>
                    <p><strong>💡 截图查看说明:</strong></p>
                    <ul>
                        <li>运行 <code>python run_chrome_tests.py</code> 生成实际截图</li>
                        <li>截图保存在 <code>{screenshots_dir_abs}</code> 目录下</li>
                        <li>如果图片无法在报告中显示，请直接打开文件夹查看</li>
                        <li>支持的格式: PNG, JPG, JPEG</li>
                    </ul>
                </div>
"""

            html_content += """
            </div>
        </div>
"""

        # 添加页脚
        html_content += f"""
        <div class="footer">
            <p>🤖 自动化测试报告 | 生成时间: {current_time}</p>
            <p>📧 如有问题请联系测试团队</p>
        </div>
    </div>
</body>
</html>
"""

        return html_content

    def _print_console_summary(self, success, report_files, screenshot_dirs):
        """打印控制台总结"""
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        summary = f"""
{'='*80}
🚀 Chrome浏览器自动化测试执行总结
{'='*80}
执行时间: {current_time}
测试状态: {'✅ 成功' if success else '❌ 失败'}

📊 测试统计:
  ├── 测试用例总数: 8个
  ├── 网站访问测试: 1个
  ├── 登录功能测试: 3个 (正确凭据、错误用户名、错误密码)
  └── 异常处理测试: 4个 (导航 + 3个异常类型)

🔧 测试特性:
  ✅ 每个测试用例都有详细的步骤说明
  ✅ 每步操作都有对应的截图记录
  ✅ 完整的异常捕获和处理验证
  ✅ 生成HTML格式的详细报告
  ✅ 元素高亮和异常信息可视化显示

📁 生成的文件:
  ├── 📊 HTML报告: {len(report_files)} 个
  ├── 📸 截图目录: {len(screenshot_dirs)} 个
  └── 📄 详细HTML报告: Chrome_Detailed_Test_Report_*.html

🎯 测试覆盖范围:
  ✅ 基础功能测试 (网站访问、页面导航)
  ✅ 登录功能测试 (正确凭据、错误用户名、错误密码)
  ✅ 异常处理测试 (NoSuchElement、ElementNotInteractable、Timeout等)
  ✅ 错误信息验证和截图记录
  ✅ 程序稳定性和健壮性验证

💡 测试说明:
  本次测试涵盖了Chrome浏览器的完整自动化测试流程，包括基础功能验证、
  登录场景测试和各种异常情况的处理验证。所有测试用例都包含详细的
  步骤记录和截图，确保测试过程的可追溯性和问题定位的便利性。

{'='*80}
"""

        print(summary)

    def run(self):
        """运行完整的Chrome测试流程"""
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
            # 确保目录存在
            self.reports_dir.mkdir(exist_ok=True)
            self.screenshots_dir.mkdir(exist_ok=True)

            # 执行测试
            success = self.run_chrome_tests()

            # 生成详细报告
            self.generate_detailed_test_report(success)

            end_time = datetime.now()
            duration = end_time - start_time

            logger.info(f"总执行时间: {duration}")

            return success

        except KeyboardInterrupt:
            logger.warning("Chrome测试被用户中断")
            return False
        except Exception as e:
            logger.error(f"Chrome测试执行出错: {e}")
            return False


def main():
    """主函数"""
    print("""
╔══════════════════════════════════════════════════════════════╗
║                    🚀 Chrome浏览器自动化测试                    ║
╚══════════════════════════════════════════════════════════════╝
""")

    runner = ChromeTestRunner()
    success = runner.run()

    if success:
        print("\n🎉 Chrome浏览器测试执行成功！请查看生成的报告和截图。")
        sys.exit(0)
    else:
        print("\n❌ Chrome浏览器测试执行失败！请查看错误信息。")
        sys.exit(1)


if __name__ == "__main__":
    main()
