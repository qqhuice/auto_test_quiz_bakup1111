#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示Expense失败场景的报告生成
直接生成一个失败场景的测试报告，展示修复后的功能
"""

import os
import sys
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pages.orangehrm_create_claim_request_page import OrangeHRMCreateClaimRequestPage


def main():
    """生成Expense失败场景的演示报告"""
    print("🚀 开始生成Expense失败场景演示报告")
    print("="*60)

    # ========== 模拟测试结果数据 ==========
    test_results = {
        "overall_status": "PARTIAL_SUCCESS",
        "claim_request_success": True,
        "expense_success": False,
        "steps": [
            {"step": 1, "name": "创建Assign Claims记录", "status": "SUCCESS"},
            {"step": 2, "name": "点击Create按钮", "status": "SUCCESS"},
            {"step": 3, "name": "导航到详情页", "status": "SUCCESS"},
            {"step": 4, "name": "添加Expense费用", "status": "FAILED", "error": "找不到Expense Type 'Transport'"},
            {"step": 5, "name": "验证费用详情", "status": "SKIPPED", "error": "Expense未成功添加"},
            {"step": 6, "name": "验证记录存在性", "status": "SUCCESS"},
            {"step": 7, "name": "生成测试报告", "status": "SUCCESS"}
        ],
        "errors": [
            "Step 4: 找不到Expense Type 'Transport'",
            "Step 4: Expense添加失败，无法继续费用流程"
        ],
        "warnings": [
            "Step 5: 由于Expense失败而跳过费用详情验证"
        ]
    }

    # ========== 创建模拟的页面对象 ==========
    # 我们不需要真实的driver，只是用来生成报告
    class MockCreateClaimRequestPage:
        def __init__(self):
            self._valid_employee_name = "Timothy Amiano"
            
        def generate_html_report(self, test_results):
            """生成HTML测试报告"""
            print("正在生成HTML测试报告...")
            try:
                import os
                from datetime import datetime

                # 创建报告目录
                report_dir = "reports"
                if not os.path.exists(report_dir):
                    os.makedirs(report_dir)

                # 生成报告文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                report_file = os.path.join(report_dir, f"expense_failure_demo_report_{timestamp}.html")

                # 获取截图目录 - 使用演示截图
                screenshot_dir = "screenshots"
                screenshots = []
                actual_screenshot_dir = None

                if os.path.exists(screenshot_dir):
                    # 查找最新的bdd_tests_*目录作为演示
                    bdd_dirs = [d for d in os.listdir(screenshot_dir) if d.startswith('bdd_tests_')]
                    if bdd_dirs:
                        bdd_dirs.sort(reverse=True)
                        bdd_screenshot_dir = os.path.join(screenshot_dir, bdd_dirs[0])
                        if os.path.exists(bdd_screenshot_dir):
                            screenshots = [f for f in os.listdir(bdd_screenshot_dir) if f.endswith('.png')]
                            screenshots.sort()
                            actual_screenshot_dir = bdd_screenshot_dir
                            print(f"找到演示截图目录: {actual_screenshot_dir}, 包含 {len(screenshots)} 张截图")

                if not actual_screenshot_dir:
                    actual_screenshot_dir = screenshot_dir
                    print(f"使用默认截图目录: {actual_screenshot_dir}")

                # 根据测试结果确定状态显示
                overall_status_display = {
                    "SUCCESS": "✅ 全部成功",
                    "PARTIAL_SUCCESS": "⚠️ 部分成功",
                    "FAILED": "❌ 测试失败",
                    "UNKNOWN": "❓ 状态未知"
                }.get(test_results["overall_status"], "❓ 状态未知")

                claim_status = "✅ 成功" if test_results.get("claim_request_success", False) else "❌ 失败"
                expense_status = "✅ 成功" if test_results.get("expense_success", False) else "❌ 失败"

                # 准备模板变量
                screenshot_dir_path = actual_screenshot_dir.replace('\\', '/') if actual_screenshot_dir else 'screenshots'
                relative_screenshot_path = f"../{screenshot_dir_path}"
                employee_name = self._valid_employee_name or "Timothy Amiano"
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                screenshot_count = len(screenshots)

                # 生成HTML内容
                html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OrangeHRM Expense失败场景 演示报告</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
            color: white;
            padding: 30px;
            text-align: center;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .header h1 {{ margin: 0; font-size: 2.5em; }}
        .header p {{ margin: 10px 0; font-size: 1.2em; opacity: 0.9; }}
        .step {{
            margin: 30px 0;
            padding: 25px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            background-color: #fafafa;
        }}
        .step-header {{
            color: white;
            padding: 15px 20px;
            margin: -25px -25px 20px -25px;
            border-radius: 8px 8px 0 0;
            font-size: 1.3em;
            font-weight: bold;
        }}
        .step-header.success {{ background-color: #28a745; }}
        .step-header.failed {{ background-color: #dc3545; }}
        .step-header.skipped {{ background-color: #6c757d; }}
        .step-content {{
            padding: 10px 0;
        }}
        .step-description {{
            font-size: 1.1em;
            color: #333;
            margin-bottom: 15px;
            line-height: 1.6;
        }}
        .screenshot {{
            text-align: center;
            margin: 20px 0;
            padding: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .screenshot img {{
            max-width: 100%;
            height: auto;
            border: 2px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .screenshot-caption {{
            margin-top: 10px;
            font-style: italic;
            color: #666;
            font-size: 0.9em;
        }}
        .success-icon {{ color: #28a745; font-size: 1.2em; }}
        .failed-icon {{ color: #dc3545; font-size: 1.2em; }}
        .skipped-icon {{ color: #6c757d; font-size: 1.2em; }}
        .step-details {{
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
            border-left: 4px solid #28a745;
        }}
        .step-details.success {{ background-color: #e8f5e8; border-left-color: #28a745; }}
        .step-details.failed {{ background-color: #f8d7da; border-left-color: #dc3545; }}
        .step-details.skipped {{ background-color: #e2e3e5; border-left-color: #6c757d; }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 8px;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚠️ OrangeHRM Expense失败场景 演示报告</h1>
            <p><strong>测试员工:</strong> {employee_name}</p>
            <p><strong>测试时间:</strong> {current_time}</p>
            <p><strong>测试状态:</strong> {overall_status_display}</p>
        </div>

        <div class="step">
            <div class="step-header success">
                <span class="success-icon">✅</span> Step 1: 点击Employee Claims，添加一条Assign Claims记录
            </div>
            <div class="step-content">
                <div class="step-description">
                    点击<strong>Employee Claims</strong>，添加一条<strong>Assign Claims</strong>记录：<br>
                    <strong>Create Claim Request</strong>：填写员工姓名、选择事件类型和货币类型
                </div>
                <div class="step-details success">
                    <strong>创建内容:</strong><br>
                    • 员工姓名: {employee_name}<br>
                    • 事件类型: Travel allowances<br>
                    • 货币类型: Euro<br>
                    • 创建状态: ✅ 成功
                </div>
            </div>
        </div>

        <div class="step">
            <div class="step-header success">
                <span class="success-icon">✅</span> Step 2: 点击Create后验证成功提示信息
            </div>
            <div class="step-content">
                <div class="step-description">
                    点击<strong>Create</strong>后验证成功提示信息，确认Claim Request创建成功
                </div>
                <div class="step-details success">
                    <strong>验证内容:</strong><br>
                    • 成功提示信息显示 ✅<br>
                    • 页面跳转正常 ✅<br>
                    • 数据保存成功 ✅<br>
                    • 状态更新正确 ✅
                </div>
            </div>
        </div>

        <div class="step">
            <div class="step-header success">
                <span class="success-icon">✅</span> Step 3: 跳转至Assign Claim详情页，验证与前一步数据一致
            </div>
            <div class="step-content">
                <div class="step-description">
                    跳转至<strong>Assign Claim</strong>详情页，验证与前一步数据一致，确保数据传递准确
                </div>
                <div class="step-details success">
                    <strong>验证项目:</strong><br>
                    • 员工姓名一致性 ✅<br>
                    • 事件类型一致性 ✅<br>
                    • 货币类型一致性 ✅<br>
                    • 页面显示完整性 ✅
                </div>
            </div>
        </div>

        <div class="step">
            <div class="step-header failed">
                <span class="failed-icon">❌</span> Step 4: 添加Expenses - 失败场景演示
            </div>
            <div class="step-content">
                <div class="step-description">
                    尝试添加<strong>Expenses</strong>，选择<strong>Expense Type</strong>和<strong>Date</strong>，填写<strong>amount</strong>，但遇到错误
                </div>
                <div class="step-details failed">
                    <strong>Expense信息:</strong><br>
                    • 费用类型: Transport<br>
                    • 日期: 2023-05-01<br>
                    • 金额: 50<br>
                    • 提交状态: {expense_status}<br>
                    <br>
                    <strong>❌ 错误详情:</strong><br>
                    • 找不到Expense Type 'Transport'<br>
                    • 页面元素定位失败<br>
                    • 无法完成费用添加流程
                </div>
            </div>
        </div>

        <div class="step">
            <div class="step-header skipped">
                <span class="skipped-icon">⏭️</span> Step 5: 检查数据与填写数据一致 - 已跳过
            </div>
            <div class="step-content">
                <div class="step-description">
                    由于Step 4失败，无法验证费用详情，此步骤被跳过
                </div>
                <div class="step-details skipped">
                    <strong>跳过原因:</strong><br>
                    • Expense添加失败<br>
                    • 无费用数据可验证<br>
                    • 依赖步骤未完成<br>
                    • 状态: ⏭️ 已跳过
                </div>
            </div>
        </div>

        <div class="step">
            <div class="step-header success">
                <span class="success-icon">✅</span> Step 6: 验证Record中存在刚才的提交记录
            </div>
            <div class="step-content">
                <div class="step-description">
                    验证Record中存在Claim Request记录（不包含Expense），确认基础流程的完整性
                </div>
                <div class="step-details success">
                    <strong>记录验证:</strong><br>
                    • Claim Request记录存在 ✅<br>
                    • 基础数据完整性 ✅<br>
                    • 状态正确性 ✅<br>
                    • 注意: Expense记录不存在（预期行为）
                </div>
            </div>
        </div>

        <div class="footer">
            <h3>⚠️ 测试总结</h3>
            <p><strong>测试结果:</strong> {overall_status_display}</p>
            <p><strong>Claim Request:</strong> {claim_status}</p>
            <p><strong>Expense添加:</strong> {expense_status}</p>
            <p><strong>截图数量:</strong> {screenshot_count}张（来自最新BDD测试）</p>
            <p><strong>报告生成时间:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>"""

                # 添加错误和警告信息
                if test_results.get("errors"):
                    html_content += f"""
            <div style="background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h4>❌ 错误信息 ({len(test_results["errors"])}个)</h4>
                <ul>"""
                    for error in test_results["errors"]:
                        html_content += f"<li>{error}</li>"
                    html_content += """
                </ul>
            </div>"""

                if test_results.get("warnings"):
                    html_content += f"""
            <div style="background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <h4>⚠️ 警告信息 ({len(test_results["warnings"])}个)</h4>
                <ul>"""
                    for warning in test_results["warnings"]:
                        html_content += f"<li>{warning}</li>"
                    html_content += """
                </ul>
            </div>"""

                html_content += f"""
            <h4>🚀 关键功能验证</h4>
            <ul style="text-align: left; display: inline-block;">
                <li>{claim_status} Employee Claims访问 - 进入Claims页面</li>
                <li>{claim_status} Assign Claims创建 - Create Claim Request</li>
                <li>{claim_status} Create成功验证 - 成功提示信息确认</li>
                <li>{claim_status} 详情页数据一致性 - 前后数据匹配验证</li>
                <li>{expense_status} Expense费用添加 - 费用信息录入</li>
                <li>⏭️ 跳过 数据验证与返回 - 由于Expense失败而跳过</li>
                <li>✅ 成功 记录存在性验证 - Claim Request记录确认</li>
            </ul>

            <h4>🎯 演示说明</h4>
            <ul style="text-align: left; display: inline-block;">
                <li>🎭 这是一个演示报告，展示Expense失败时的报告格式</li>
                <li>🔧 修复后的系统能正确识别和报告失败状态</li>
                <li>📊 测试结果现在反映真实的执行情况</li>
                <li>⚠️ 部分成功状态表示Claim Request成功但Expense失败</li>
                <li>🚨 错误和警告信息清晰显示在报告中</li>
                <li>📈 这解决了用户报告的"明明失败却显示成功"的问题</li>
            </ul>

            <h4>📁 截图信息</h4>
            <div style="text-align: left; background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
                <p><strong>截图目录:</strong> {screenshot_dir_path}</p>
                <p><strong>截图数量:</strong> {screenshot_count} 张</p>
                <p><strong>💡 说明:</strong></p>
                <ul>
                    <li>此演示报告使用最新BDD测试的截图作为示例</li>
                    <li>实际失败场景会包含失败时的截图</li>
                    <li>修复后的系统会为每种状态生成对应的截图</li>
                </ul>
            </div>
        </div>
    </div>
</body>
</html>
                """

                # 写入HTML文件
                with open(report_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)

                print(f"✅ HTML演示报告已生成: {report_file}")
                self._report_file = report_file
                return True

            except Exception as e:
                print(f"生成HTML演示报告失败: {e}")
                return False

    # ========== 生成演示报告 ==========
    mock_page = MockCreateClaimRequestPage()
    if mock_page.generate_html_report(test_results):
        print("✅ 演示报告生成成功")
        print(f"📄 报告文件位置: {mock_page._report_file}")
        
        # 输出测试结果总结
        print(f"\n📋 演示场景总结:")
        print(f"   • 整体状态: {test_results['overall_status']}")
        print(f"   • Claim Request: {'✅ 成功' if test_results['claim_request_success'] else '❌ 失败'}")
        print(f"   • Expense添加: {'✅ 成功' if test_results['expense_success'] else '❌ 失败'}")
        if test_results["errors"]:
            print(f"   • 错误数量: {len(test_results['errors'])}")
            for error in test_results["errors"]:
                print(f"     - {error}")
        if test_results["warnings"]:
            print(f"   • 警告数量: {len(test_results['warnings'])}")
            for warning in test_results["warnings"]:
                print(f"     - {warning}")
        
        print("\n🎉 演示报告生成完成！")
        print("="*60)
        return True
    else:
        print("❌ 演示报告生成失败")
        return False


if __name__ == "__main__":
    main()
