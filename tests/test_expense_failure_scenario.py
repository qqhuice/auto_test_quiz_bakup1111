#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Expense失败场景的脚本
用于验证当Expense添加失败时，测试报告能正确显示失败状态
"""

import os
import sys
import time
from datetime import datetime
from selenium.webdriver.common.by import By

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.driver_manager import DriverManager
from pages.orangehrm_login_page import OrangeHRMLoginPage
from pages.orangehrm_dashboard_page import OrangeHRMDashboardPage
from pages.orangehrm_claims_page import OrangeHRMClaimsPage
from pages.orangehrm_create_claim_request_page import OrangeHRMCreateClaimRequestPage


def get_bdd_screenshot_path(base_dir: str, filename: str) -> str:
    """获取BDD测试截图的完整路径"""
    return os.path.join(base_dir, filename)


def main() -> bool:
    """
    主函数：模拟Expense失败的测试场景

    Returns:
        bool: 测试是否成功完成
    """
    print("🚀 开始执行Expense失败场景测试")
    print("="*60)

    # ========== 初始化测试状态跟踪 ==========
    test_results = {
        "overall_status": "UNKNOWN",
        "claim_request_success": False,
        "expense_success": False,
        "steps": [],
        "errors": [],
        "warnings": []
    }

    # ========== 创建带时间戳的截图文件夹 ==========
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bdd_screenshot_dir = os.path.join("screenshots", f"expense_failure_test_{timestamp}")
    os.makedirs(bdd_screenshot_dir, exist_ok=True)
    print(f"📁 创建测试截图文件夹: {bdd_screenshot_dir}")

    driver = None
    try:
        # ========== 初始化浏览器 ==========
        print("🔧 正在执行测试前提条件...")
        driver_manager = DriverManager()
        
        for attempt in range(3):
            try:
                print(f"正在尝试打开浏览器，第{attempt + 1}次...")
                driver = driver_manager.create_chrome_driver()
                break
            except Exception as e:
                print(f"第{attempt + 1}次尝试失败: {e}")
                if attempt == 2:
                    print("❌ 浏览器启动失败，无法继续测试")
                    return False
                time.sleep(2)

        # ========== 登录系统 ==========
        print("正在访问OrangeHRM登录页面...")
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        time.sleep(3)
        print("✅ 浏览器打开成功，页面加载完成")

        # 登录
        login_page = OrangeHRMLoginPage(driver)
        login_page.enter_username("Admin")
        login_page.enter_password("admin123")
        login_page.click_login_button()
        time.sleep(3)

        # 导航到Claims页面
        dashboard_page = OrangeHRMDashboardPage(driver)
        dashboard_page.click_sidebar_menu_item("Claim")
        time.sleep(3)

        claims_page = OrangeHRMClaimsPage(driver)
        claims_page.click_employee_claims()
        time.sleep(3)

        print("✅ 所有测试前提条件已完成，开始执行测试步骤...")
        print("="*60)

        # ========== 执行测试步骤 ==========
        create_claim_request_page = OrangeHRMCreateClaimRequestPage(driver)

        # Step 1: 创建Claim Request (成功)
        print("Step 1: 正在创建Assign Claims记录...")
        result = create_claim_request_page.fill_employee_name_conditional("Amelia Brown")
        if result:
            create_claim_request_page.select_event("Travel allowances")
            create_claim_request_page.select_currency("Euro")
            print("✅ Assign Claims记录创建成功")
            create_claim_request_page.screenshot_helper(get_bdd_screenshot_path(bdd_screenshot_dir, "assign_claim_request.png"))
            test_results["steps"].append({"step": 1, "name": "创建Assign Claims记录", "status": "SUCCESS"})
        else:
            print("❌ 员工姓名填写失败，无法继续")
            test_results["steps"].append({"step": 1, "name": "创建Assign Claims记录", "status": "FAILED", "error": "员工姓名填写失败"})
            test_results["errors"].append("Step 1: 员工姓名填写失败")
            test_results["overall_status"] = "FAILED"
            return False

        # Step 2: 点击Create (成功)
        print("Step 2: 正在点击Create按钮...")
        if create_claim_request_page.click_create_button():
            print("✅ Create按钮点击成功")
            time.sleep(2)
            create_claim_request_page.screenshot_helper(get_bdd_screenshot_path(bdd_screenshot_dir, "assign_claim_request_success.png"))
            test_results["steps"].append({"step": 2, "name": "点击Create按钮", "status": "SUCCESS"})
            test_results["claim_request_success"] = True
        else:
            print("❌ Create按钮点击失败")
            test_results["steps"].append({"step": 2, "name": "点击Create按钮", "status": "FAILED", "error": "Create按钮点击失败"})
            test_results["errors"].append("Step 2: Create按钮点击失败")
            test_results["overall_status"] = "FAILED"
            return False

        # Step 3: 导航到详情页 (成功)
        print("Step 3: 正在导航到Assign Claim详情页...")
        if create_claim_request_page.navigate_to_claim_details():
            print("✅ 导航到详情页成功")
            create_claim_request_page.scroll_to_latest_record()
            create_claim_request_page.screenshot_helper(get_bdd_screenshot_path(bdd_screenshot_dir, "assign_claim_records_found.png"))
            result = create_claim_request_page.click_latest_record_view_details()
            if result:
                print("✅ View Details点击成功")
                time.sleep(2)
                create_claim_request_page.screenshot_helper(get_bdd_screenshot_path(bdd_screenshot_dir, "assign_claim_view_details.png"))
                test_results["steps"].append({"step": 3, "name": "导航到详情页", "status": "SUCCESS"})
            else:
                print("❌ View Details点击失败")
                test_results["steps"].append({"step": 3, "name": "导航到详情页", "status": "PARTIAL", "error": "View Details点击失败"})
                test_results["warnings"].append("Step 3: View Details点击失败")
        else:
            print("❌ 导航到详情页失败")
            test_results["steps"].append({"step": 3, "name": "导航到详情页", "status": "FAILED", "error": "导航到详情页失败"})
            test_results["errors"].append("Step 3: 导航到详情页失败")
            test_results["overall_status"] = "FAILED"
            return False

        # Step 4: 模拟Expense添加失败
        print("Step 4: 正在模拟Expense添加失败...")
        print("❌ 模拟场景：找不到Expense Type选项")
        
        # 模拟导航到费用区域成功，但添加费用失败
        if create_claim_request_page.navigate_to_add_expense_section():
            print("✅ 导航到费用区域成功")
            
            # 模拟add_expense失败（比如找不到Expense Type）
            print("❌ 模拟：无法找到Expense Type 'Transport'")
            create_claim_request_page.screenshot_helper(get_bdd_screenshot_path(bdd_screenshot_dir, "expense_type_not_found.png"))
            
            # 记录失败状态
            test_results["steps"].append({"step": 4, "name": "添加Expense费用", "status": "FAILED", "error": "找不到Expense Type 'Transport'"})
            test_results["errors"].append("Step 4: 找不到Expense Type 'Transport'")
            test_results["expense_success"] = False
        else:
            print("❌ 导航到费用区域失败")
            test_results["steps"].append({"step": 4, "name": "添加Expense费用", "status": "FAILED", "error": "导航到费用区域失败"})
            test_results["errors"].append("Step 4: 导航到费用区域失败")

        # Step 5: 由于Expense失败，跳过验证
        print("Step 5: 由于Expense添加失败，跳过费用详情验证...")
        test_results["steps"].append({"step": 5, "name": "验证费用详情", "status": "SKIPPED", "error": "Expense未成功添加"})
        test_results["warnings"].append("Step 5: 由于Expense失败而跳过")

        # Step 6: 记录验证 (仍然执行)
        print("Step 6: 正在验证记录存在性...")
        create_claim_request_page.scroll_to_latest_record()
        time.sleep(2)
        create_claim_request_page.screenshot_helper(get_bdd_screenshot_path(bdd_screenshot_dir, "assign_claim_record_exists.png"))
        test_results["steps"].append({"step": 6, "name": "验证记录存在性", "status": "SUCCESS"})

        # ========== 确定最终测试状态 ==========
        if test_results["overall_status"] == "UNKNOWN":
            if test_results["claim_request_success"] and test_results["expense_success"]:
                test_results["overall_status"] = "SUCCESS"
            elif test_results["claim_request_success"] and not test_results["expense_success"]:
                test_results["overall_status"] = "PARTIAL_SUCCESS"
            else:
                test_results["overall_status"] = "FAILED"

        # ========== 生成测试报告 ==========
        print("\n📊 正在生成测试报告...")
        create_claim_request_page.generate_html_report(test_results)

        # ========== 输出最终测试结果 ==========
        print(f"\n📋 测试结果总结:")
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

        print("\n🎉 测试执行完成！")
        print(f"📸 所有截图已保存到: {bdd_screenshot_dir}")
        print("📄 详细报告已保存到reports目录")
        
        # 返回真实的测试结果
        return test_results["overall_status"] in ["SUCCESS", "PARTIAL_SUCCESS"]

    except Exception as e:
        print(f"❌ 测试执行过程中发生错误: {e}")
        return False
    finally:
        # 关闭浏览器
        if driver:
            try:
                driver.quit()
                print("✅ 浏览器已关闭")
            except Exception as e:
                print(f"⚠️ 浏览器关闭失败: {e}")


if __name__ == "__main__":
    """程序入口点"""
    try:
        success: bool = main()
        if success:
            print("\n🎉 测试场景执行成功！")
            sys.exit(0)
        else:
            print("\n❌ 测试场景执行失败！")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断了测试执行")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试执行过程中发生未预期的错误: {e}")
        sys.exit(1)
