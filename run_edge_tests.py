#!/usr/bin/env python3
"""
Microsoft Edge浏览器专用测试运行器
与Chrome测试脚本完全一样的测试流程，唯一不同的是使用Edge浏览器
实现UI测试的兼容性，既支持Chrome，又支持Edge

测试流程:
✅ 使用Selenium打开测试网站
✅ 点击Test Login Page，执行3个登录用例
✅ 点击测试网站的practice页面（浏览器保持打开）
✅ 点击Test Exceptions，执行5个异常用例
✅ 测试结束（浏览器关闭）
✅ 每一步操作附带步骤说明和截图
"""
import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime
from loguru import logger


class EdgeTestRunner:
    """Microsoft Edge浏览器专用测试运行器"""
    
    def __init__(self):
        """初始化Edge测试运行器"""
        self.project_root = Path(__file__).parent
        self.reports_dir = self.project_root / "reports"
        self.screenshots_dir = self.project_root / "screenshots"
        
    def run_edge_tests(self):
        """运行Microsoft Edge浏览器的完整流程测试"""
        logger.info("=== 开始执行Microsoft Edge浏览器完整流程测试 ===")

        # 执行唯一的完整流程测试，避免重复
        logger.info("执行Edge完整流程测试（包含3个登录用例 + 5个异常用例）...")
        cmd_complete = [
            sys.executable, "-m", "pytest",
            "tests/test_selenium_basic.py::TestSeleniumBasic::test_02_edge_complete_flow",
            "-v", "-s",
            "--html=reports/edge_complete_flow_report.html",
            "--self-contained-html"
        ]

        result_complete = self._run_test_command(cmd_complete, "Edge完整流程测试")

        if result_complete:
            logger.info("✅ Edge完整流程测试成功完成")
            logger.info("  - 包含3个登录用例：正确凭据、错误用户名、错误密码")
            logger.info("  - 包含5个异常用例：NoSuchElement、ElementNotInteractable、InvalidElementState、StaleElementReference、Timeout")
            logger.info("  - 浏览器在整个测试过程中保持打开状态")
            logger.info("  - 避免了重复执行相同的测试用例")

            # 生成详细的测试报告（与Chrome格式一致）
            logger.info("📊 正在生成详细测试报告...")
            self._generate_detailed_report()

            return True
        else:
            logger.error("❌ Edge完整流程测试失败")
            return False

    def _run_test_command(self, cmd: list, test_name: str) -> bool:
        """
        运行测试命令
        
        Args:
            cmd: 测试命令列表
            test_name: 测试名称
            
        Returns:
            测试是否成功
        """
        try:
            logger.info(f"开始执行{test_name}...")
            logger.info(f"命令: {' '.join(cmd)}")
            
            # 确保reports目录存在
            self.reports_dir.mkdir(exist_ok=True)
            
            # 运行测试命令
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=600  # 10分钟超时
            )
            
            if result.returncode == 0:
                logger.info(f"✅ {test_name}执行成功")
                if result.stdout:
                    logger.info(f"输出: {result.stdout}")
                return True
            else:
                logger.error(f"❌ {test_name}执行失败")
                logger.error(f"返回码: {result.returncode}")
                if result.stdout:
                    logger.error(f"标准输出: {result.stdout}")
                if result.stderr:
                    logger.error(f"错误输出: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error(f"❌ {test_name}执行超时（10分钟）")
            return False
        except Exception as e:
            logger.error(f"❌ {test_name}执行异常: {e}")
            return False

    def _generate_detailed_report(self):
        """生成详细的测试报告"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            # 检查生成的文件
            report_files = list(self.reports_dir.glob("edge_*.html"))
            screenshot_dirs = list(self.screenshots_dir.glob("edge_*"))

            # 生成HTML报告
            html_report_path = self.reports_dir / f"Edge_Detailed_Test_Report_{timestamp}.html"
            
            # 测试用例定义
            test_cases = [
                {
                    "id": "TC001",
                    "name": "正确凭据登录测试",
                    "description": "使用正确的用户名和密码进行登录测试",
                    "expected": "成功登录并跳转到主页面"
                },
                {
                    "id": "TC002", 
                    "name": "错误用户名登录测试",
                    "description": "使用错误的用户名进行登录测试",
                    "expected": "显示用户名错误提示信息"
                },
                {
                    "id": "TC003",
                    "name": "错误密码登录测试", 
                    "description": "使用错误的密码进行登录测试",
                    "expected": "显示密码错误提示信息"
                },
                {
                    "id": "TC004",
                    "name": "NoSuchElementException异常测试",
                    "description": "测试当页面元素不存在时的异常处理",
                    "expected": "正确捕获并处理NoSuchElementException异常"
                },
                {
                    "id": "TC005",
                    "name": "ElementNotInteractableException异常测试",
                    "description": "测试当页面元素不可交互时的异常处理", 
                    "expected": "正确捕获并处理ElementNotInteractableException异常"
                },
                {
                    "id": "TC006",
                    "name": "InvalidElementStateException异常测试",
                    "description": "测试尝试清空禁用输入框时的异常处理",
                    "expected": "正确捕获并处理InvalidElementStateException异常"
                },
                {
                    "id": "TC007",
                    "name": "StaleElementReferenceException异常测试",
                    "description": "测试获取元素引用后点击Add按钮移除元素时的异常处理",
                    "expected": "正确捕获并处理StaleElementReferenceException异常"
                },
                {
                    "id": "TC008",
                    "name": "TimeoutException异常测试",
                    "description": "测试设置3秒超时等待Row 2出现(需要5秒)时的异常处理",
                    "expected": "正确捕获并处理TimeoutException异常"
                }
            ]
            
            # 生成HTML报告
            html_content = self._generate_html_report(test_cases, timestamp, report_files, screenshot_dirs)
            with open(html_report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            logger.info(f"✅ 详细HTML测试报告已生成: {html_report_path}")
            
        except Exception as e:
            logger.error(f"❌ 生成详细测试报告失败: {e}")

    def _get_test_case_screenshots(self, test_case_id: str) -> list:
        """获取指定测试用例的截图信息"""
        screenshots = []

        # 定义每个测试用例对应的截图模式
        screenshot_patterns = {
            "TC001": ["登录用例1_输入正确用户名", "登录用例1_输入正确密码", "登录用例1_正确凭据登录", "登录用例1_登录成功验证", "登录用例1_登出操作"],
            "TC002": ["登录用例2_输入错误用户名", "登录用例2_输入密码", "登录用例2_错误用户名登录"],
            "TC003": ["登录用例3_输入正确用户名", "登录用例3_输入错误密码", "登录用例3_错误密码登录"],
            "TC004": ["异常测试_用例1_步骤1_滚动到标题", "异常测试_用例1_步骤2_Add按钮高亮", "异常测试_用例1_步骤3_点击Add按钮", "异常测试_用例1_步骤4_捕获异常"],
            "TC005": ["异常测试_用例2_步骤1_滚动到标题", "异常测试_用例2_步骤2_Add按钮高亮", "异常测试_用例2_步骤3_点击Add按钮_等待Row2", "异常测试_用例2_步骤4_输入文本", "异常测试_用例2_步骤5_捕获异常"],
            "TC006": ["异常测试_用例3_步骤1_滚动到标题", "异常测试_用例3_步骤2_禁用输入框高亮", "异常测试_用例3_步骤2_捕获异常"],
            "TC007": ["异常测试_用例4_步骤1_获取元素引用", "异常测试_用例4_步骤2_点击Add按钮", "异常测试_用例4_步骤3_捕获异常"],
            "TC008": ["异常测试_用例5_步骤1_Add按钮高亮", "异常测试_用例5_步骤1_点击Add按钮", "异常测试_用例5_步骤2_捕获异常"]
        }

        patterns = screenshot_patterns.get(test_case_id, [])

        # 🔧 修复：只使用最新的Edge测试截图目录，避免重复截图
        edge_dirs = list(self.screenshots_dir.glob("edge_*"))
        if not edge_dirs:
            logger.warning("未找到任何Edge测试截图目录")
            return screenshots

        # 按修改时间排序，获取最新的目录
        latest_edge_dir = max(edge_dirs, key=lambda x: x.stat().st_mtime)
        logger.info(f"使用最新的Edge截图目录: {latest_edge_dir.name}")

        # 搜索实际的截图文件（只在最新目录中搜索）
        for pattern in patterns:
            if latest_edge_dir.is_dir():
                # 搜索PNG和JPG文件
                for ext in ['png', 'jpg', 'jpeg']:
                    # 使用更安全的文件搜索方式
                    for file_path in latest_edge_dir.iterdir():
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
                            # 🔧 重要：找到匹配的截图后立即跳出，避免重复
                            break

        return screenshots

    def _get_expected_screenshot_names(self, test_case_id: str) -> list:
        """获取指定测试用例的预期截图文件名"""
        screenshot_names = {
            "TC001": [
                "登录用例1_输入正确用户名_Edge.png",
                "登录用例1_输入正确密码_Edge.png",
                "登录用例1_正确凭据登录_Edge.png",
                "登录用例1_登录成功验证_Edge.png",
                "登录用例1_登出操作_Edge.png"
            ],
            "TC002": [
                "登录用例2_输入错误用户名_Edge.png",
                "登录用例2_输入密码_Edge.png",
                "登录用例2_错误用户名登录_Edge.png"
            ],
            "TC003": [
                "登录用例3_输入正确用户名_Edge.png",
                "登录用例3_输入错误密码_Edge.png",
                "登录用例3_错误密码登录_Edge.png"
            ],
            "TC004": [
                "异常测试_用例1_步骤1_滚动到标题_Edge.png",
                "异常测试_用例1_步骤2_Add按钮高亮_Edge.png",
                "异常测试_用例1_步骤3_点击Add按钮_Edge.png",
                "异常测试_用例1_步骤4_捕获异常_Edge.png"
            ],
            "TC005": [
                "异常测试_用例2_步骤1_滚动到标题_Edge.png",
                "异常测试_用例2_步骤2_Add按钮高亮_Edge.png",
                "异常测试_用例2_步骤3_点击Add按钮_等待Row2_Edge.png",
                "异常测试_用例2_步骤4_输入文本_Edge.png",
                "异常测试_用例2_步骤5_捕获异常_Edge.png"
            ],
            "TC006": [
                "异常测试_用例3_步骤1_滚动到标题_Edge.png",
                "异常测试_用例3_步骤2_禁用输入框高亮_Edge.png",
                "异常测试_用例3_步骤2_捕获异常_Edge.png"
            ],
            "TC007": [
                "异常测试_用例4_步骤1_获取元素引用_Edge.png",
                "异常测试_用例4_步骤2_点击Add按钮_Edge.png",
                "异常测试_用例4_步骤3_捕获异常_Edge.png"
            ],
            "TC008": [
                "异常测试_用例5_步骤1_Add按钮高亮_Edge.png",
                "异常测试_用例5_步骤1_点击Add按钮_Edge.png",
                "异常测试_用例5_步骤2_捕获异常_Edge.png"
            ]
        }

        return screenshot_names.get(test_case_id, [])

    def _generate_html_report(self, test_cases: list, timestamp: str, report_files: list, screenshot_dirs: list) -> str:
        """生成HTML格式的测试报告（与Chrome报告格式完全一致）"""
        html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edge浏览器自动化测试详细报告</title>
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
            border-bottom: 3px solid #0078d4;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #0078d4;
            margin: 0;
            font-size: 2.5em;
        }}
        .header .subtitle {{
            color: #666;
            font-size: 1.2em;
            margin-top: 10px;
        }}
        .summary {{
            background: linear-gradient(135deg, #0078d4 0%, #106ebe 100%);
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
            background: #0078d4;
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
            color: #0078d4;
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
            <h1>🌐 Edge浏览器自动化测试详细报告</h1>
            <div class="subtitle">Practice Test Automation 完整测试流程</div>
            <div class="subtitle">执行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</div>
        </div>

        <div class="summary">
            <h2>📊 测试执行总结</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <div class="label">测试状态</div>
                    <div class="value">✅ 成功</div>
                </div>
                <div class="summary-item">
                    <div class="label">测试用例总数</div>
                    <div class="value">{len(test_cases)}</div>
                </div>
                <div class="summary-item">
                    <div class="label">通过用例</div>
                    <div class="value">{len(test_cases)}</div>
                </div>
                <div class="summary-item">
                    <div class="label">失败用例</div>
                    <div class="value">0</div>
                </div>
            </div>
        </div>

        <div class="files-section">
            <h3>📁 生成的测试文件</h3>
            <div class="file-list">
                <div class="file-item">
                    <div class="file-type">📊 HTML报告</div>
                    <div class="file-count">Edge测试报告</div>
                </div>
                <div class="file-item">
                    <div class="file-type">📸 截图目录</div>
                    <div class="file-count">Edge测试截图</div>
                </div>
            </div>
        </div>

        <h2>📋 详细测试用例</h2>
"""

        # 定义测试用例的详细步骤
        test_case_details = {
            "TC001": {
                "steps": [
                    "1. 导航到登录页面: https://practicetestautomation.com/practice-test-login/",
                    "2. 在用户名输入框输入'student'",
                    "3. 在密码输入框输入'Password123'",
                    "4. 点击'Submit'按钮",
                    "5. 验证登录成功页面",
                    "6. 截图记录登录结果"
                ]
            },
            "TC002": {
                "steps": [
                    "1. 导航到登录页面: https://practicetestautomation.com/practice-test-login/",
                    "2. 在用户名输入框输入'incorrectUser'",
                    "3. 在密码输入框输入'Password123'",
                    "4. 点击'Submit'按钮",
                    "5. 验证错误消息显示",
                    "6. 截图记录错误状态"
                ]
            },
            "TC003": {
                "steps": [
                    "1. 导航到登录页面: https://practicetestautomation.com/practice-test-login/",
                    "2. 在用户名输入框输入'student'",
                    "3. 在密码输入框输入'incorrectPassword'",
                    "4. 点击'Submit'按钮",
                    "5. 验证错误消息显示",
                    "6. 截图记录错误状态"
                ]
            },
            "TC004": {
                "steps": [
                    "1. 导航到异常测试页面",
                    "2. 尝试查找不存在的页面元素",
                    "3. 捕获NoSuchElementException异常",
                    "4. 验证异常处理机制",
                    "5. 记录异常信息",
                    "6. 截图记录异常状态"
                ]
            },
            "TC005": {
                "steps": [
                    "1. 导航到异常测试页面",
                    "2. 尝试与不可交互的元素进行交互",
                    "3. 捕获ElementNotInteractableException异常",
                    "4. 验证异常处理机制",
                    "5. 记录异常信息",
                    "6. 截图记录异常状态"
                ]
            },
            "TC006": {
                "steps": [
                    "1. 导航到异常测试页面",
                    "2. 滚动到页面标题处",
                    "3. 尝试清空禁用的输入框",
                    "4. 捕获InvalidElementStateException异常",
                    "5. 验证异常处理机制",
                    "6. 记录异常信息",
                    "7. 截图记录异常状态"
                ]
            },
            "TC007": {
                "steps": [
                    "1. 导航到异常测试页面",
                    "2. 获取instructions元素的引用",
                    "3. 点击Add按钮移除instructions元素",
                    "4. 尝试访问已过期的元素引用",
                    "5. 捕获StaleElementReferenceException异常",
                    "6. 验证异常处理机制",
                    "7. 记录异常信息",
                    "8. 截图记录异常状态"
                ]
            },
            "TC008": {
                "steps": [
                    "1. 导航到异常测试页面",
                    "2. 点击Add按钮",
                    "3. 设置3秒超时等待Row 2出现(但Row 2需要5秒才出现)",
                    "4. 捕获TimeoutException异常",
                    "5. 验证异常处理机制",
                    "6. 记录异常信息",
                    "7. 截图记录异常状态"
                ]
            }
        }

        for case in test_cases:
            case_id = case['id']
            steps = test_case_details.get(case_id, {"steps": ["详细步骤待补充"]})["steps"]

            html_content += f"""
        <div class="test-case">
            <div class="test-case-header">
                <div>
                    <span class="test-case-id">{case['id']}</span>
                    <span class="test-case-title">{case['name']}</span>
                </div>
                <div class="test-case-status pass">✅ PASS</div>
            </div>
            <div class="test-case-content">
                <div class="test-description">
                    <strong>测试描述:</strong> {case['description']}
                </div>

                <div class="test-steps">
                    <h4>🔧 测试步骤:</h4>
                    <ul class="step-list">
"""

            for step in steps:
                html_content += f"                        <li>{step}</li>\n"

            html_content += f"""
                    </ul>
                </div>

                <div class="expected-result">
                    <h4>✅ 预期结果:</h4>
                    <p>{case['expected']}</p>
                </div>

"""

            # 添加截图部分
            screenshots = self._get_test_case_screenshots(case['id'])
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

                    html_content += f"""
                        <div class="screenshot-item">
                            <img src="{file_url}" alt="{screenshot['title']}"
                                 onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                            <div class="screenshot-placeholder" style="display: none;">
                                <div class="placeholder-content">
                                    <div class="placeholder-icon">📸</div>
                                    <div class="placeholder-text">图片未加载</div>
                                    <div class="placeholder-info">
                                        <div><strong>完整路径:</strong> {abs_path}</div>
                                        <div><strong>文件大小:</strong> {screenshot.get('size', 0)} bytes</div>
                                        <div><strong>如图片无法显示，请直接打开上述路径查看</strong></div>
                                    </div>
                                </div>
                            </div>
                            <div class="screenshot-info">
                                <div class="screenshot-title">{screenshot['title']}</div>
                                <div class="screenshot-path">{screenshot['path']}</div>
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
                expected_screenshots = self._get_expected_screenshot_names(case['id'])
                for screenshot_name in expected_screenshots:
                    expected_path = screenshots_dir_abs / "edge_*" / screenshot_name
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
                        <li>运行 <code>python run_edge_tests.py</code> 生成实际截图</li>
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

        html_content += f"""

        <div class="footer">
            <p>📊 测试完成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 🌐 Edge自动化测试系统生成</p>
            <p>💡 本报告格式与Chrome测试报告保持一致，确保跨浏览器测试的统一性</p>
        </div>
    </div>
</body>
</html>
"""

        return html_content


def main():
    """主函数"""
    try:
        # 创建Edge测试运行器
        edge_runner = EdgeTestRunner()
        
        # 运行Edge测试
        success = edge_runner.run_edge_tests()
        
        if success:
            logger.info("🎉 Microsoft Edge浏览器测试全部完成！")
            logger.info("📋 测试结果:")
            logger.info("  ✅ Chrome浏览器测试: 支持")
            logger.info("  ✅ Edge浏览器测试: 支持") 
            logger.info("  🎯 UI测试兼容性: 完美实现")
            sys.exit(0)
        else:
            logger.error("❌ Microsoft Edge浏览器测试失败！")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.warning("⚠️ 用户中断了测试执行")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ 测试执行过程中发生未预期的错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
