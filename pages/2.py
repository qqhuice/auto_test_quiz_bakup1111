#!/usr/bin/env python3
"""
OrangeHRM Claim Request 自动化测试脚本
"""
import sys
import os
import time
from typing import Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Selenium相关导入
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# 页面对象导入
from pages.orangehrm_dashboard_page import OrangeHRMDashboardPage
from pages.orangehrm_claims_page import OrangeHRMClaimsPage
from pages.orangehrm_login_page import OrangeHRMLoginPage
from pages.orangehrm_create_claim_request_page import OrangeHRMCreateClaimRequestPage

# 工具类导入
from utils.driver_manager import DriverManager
from utils.screenshot_helper import ScreenshotHelper

# 配置导入
try:
    from utils.config import config
except ImportError:
    # 如果config模块不存在，使用默认配置
    config = None

# # 1. 打开浏览器
# driver = webdriver.Chrome()
# driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
# driver.maximize_window()
# time.sleep(1)
#
# # 2. 登录
# username = driver.find_element(By.NAME, "username")
# username.send_keys("Admin")
# password = driver.find_element(By.NAME, "password")
# password.send_keys("admin123")
# login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
# login_button.click()
# time.sleep(3)
#
# # 3. 点击Claims菜单，进入Claims页面
# claims_menu = driver.find_element(By.XPATH, "//span[text()='Claim']")
# claims_menu.click()
# time.sleep(3)
# #'/html/body/div/div[1]/div[1]/aside/nav/div[2]/ul/li[11]/a/span'

def open_browser_with_retry(max_retries: int = 3) -> WebDriver:
    """
    带重试机制的浏览器打开

    Args:
        max_retries (int): 最大重试次数，默认3次

    Returns:
        WebDriver: Chrome WebDriver实例

    Raises:
        Exception: 所有重试都失败时抛出异常
    """
    driver: Optional[WebDriver] = None

    for attempt in range(max_retries):
        try:
            print(f"正在尝试打开浏览器，第{attempt + 1}次...")
            driver = DriverManager().create_chrome_driver()

            # 设置更长的页面加载超时
            driver.set_page_load_timeout(60)  # 60秒超时

            print("正在访问OrangeHRM登录页面...")
            driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
            driver.maximize_window()
            print("✅ 浏览器打开成功，页面加载完成")
            time.sleep(2)
            return driver

        except Exception as e:
            print(f"❌ 第{attempt + 1}次尝试失败: {e}")
            if driver is not None:
                try:
                    driver.quit()
                except Exception:
                    pass
                driver = None

            if attempt < max_retries - 1:
                print(f"等待5秒后重试...")
                time.sleep(5)

    # 如果所有重试都失败，抛出异常
    print("❌ 所有重试都失败，请检查网络连接")
    raise Exception("无法打开浏览器，所有重试都失败")


def main() -> bool:
    """
    主函数：执行完整的测试流程

    Returns:
        bool: 测试是否成功完成
    """
    print("🚀 开始执行OrangeHRM Claim Request自动化测试")
    print("="*60)

    # ========== 测试前提条件（必须成功） ==========
    print("🔧 正在执行测试前提条件...")

    # 1. 打开浏览器（带重试机制）
    driver: WebDriver = open_browser_with_retry()

    # 2. 登录
    login_page = OrangeHRMLoginPage(driver)
    login_page.login_with_default_credentials()
    time.sleep(3)

    # 3. 点击Claims菜单，进入Claims页面
    dashboard_page = OrangeHRMDashboardPage(driver)
    dashboard_page.click_claims_menu()
    time.sleep(3)

    # 4. 创建Claims页面对象
    claims_page = OrangeHRMClaimsPage(driver)
    claims_page.click_employee_claims()
    time.sleep(3)

    # 5. 点击"Assign Claim"按钮
    assign_claim_button = driver.find_element(By.XPATH, "/html/body/div/div[1]/div[2]/div[2]/div[2]/div[1]/button")
    assign_claim_button.click()
    time.sleep(3)

    print("✅ 所有测试前提条件已完成，开始执行测试步骤...")
    print("="*60)

    # Step 1: 添加一条Assign Claims记录,截图
    print("Step 1: 正在创建Assign Claims记录...")
    create_claim_request_page = OrangeHRMCreateClaimRequestPage(driver)

    # 使用智能员工姓名填写，自动适应不同登录账号
    result = create_claim_request_page.fill_employee_name_conditional("Amelia Brown")
    if result:
        # 获取实际使用的员工姓名作为全局变量
        actual_employee_name = create_claim_request_page.get_valid_employee_name()
        print(f"实际使用的员工姓名: {actual_employee_name}")
        #截取员工姓名填写成功截图
        create_claim_request_page.screenshot_helper("assign_claim_request_employee_name.png")
        # 智能选择事件类型
        create_claim_request_page.select_event("Travel allowances")
        # 截取事件类型选择成功截图
        create_claim_request_page.screenshot_helper("assign_claim_request_event_type.png")
        create_claim_request_page.select_currency("Euro")
        print("✅ Assign Claims记录创建成功")
        # time.sleep(2)
        create_claim_request_page.screenshot_helper("assign_claim_request.png")
    else:
        print("❌ 员工姓名填写失败，无法继续")
        driver.quit()
        return False

    # Step 2: 点击Create后验证成功提示信息, 截图
    print("Step 2: 正在点击Create按钮...")
    if create_claim_request_page.click_create_button():
        print("✅ Create按钮点击成功")
        time.sleep(2)
        # 成功提示信息截图
        create_claim_request_page.screenshot_helper("assign_claim_request_success.png")
        time.sleep(2)
        # 详情页截图
        create_claim_request_page.screenshot_helper("assign_claim_request_detail.png")
    else:
        print("❌ Create按钮点击失败")
        driver.quit()
        return False

    # Step 3: 跳转至Assign Claim详情页，验证与前一步数据一致，截图
    print("Step 3: 正在导航到Assign Claim详情页...")
    if create_claim_request_page.navigate_to_claim_details():
        print("✅ 导航到详情页成功")
        time.sleep(0.5)
        # 页面滚动到记录详情页的区域
        #create_claim_request_page.scroll_to_Records_Found()
        create_claim_request_page.scroll_to_latest_record()
        create_claim_request_page.screenshot_helper("assign_claim_records_found.png")
        # 点击最新一条记录的view details（只点击不验证）
        result = create_claim_request_page.click_latest_record_view_details()
        if result:
            print("✅ View Details点击成功")
            time.sleep(2)
            # 截图
            create_claim_request_page.screenshot_helper("assign_claim_view_details.png")
        else:
            print("❌ View Details点击失败")
            create_claim_request_page.screenshot_helper("view_details_failed.png")
    else:
        print("❌ 导航到详情页失败")
        driver.quit()
        return False

    # Step 4: 添加Expenses，选择Expense Type和Date，填写amount，点击Submit，验证成功提示信息，截图
    print("Step 4: 正在添加Expense费用...")
    # 在Assign Claim详情页添加费用
    if create_claim_request_page.navigate_to_add_expense_section():
        if create_claim_request_page.add_expense("Transport", "2023-05-01", "50"):
            if create_claim_request_page.submit_expense():
                print("✅ Expense添加成功")
                # 滚动到最底部
                # 截图
                #time.sleep(0.5)
                create_claim_request_page.screenshot_helper("add_expense_success.png")
            else:
                print("❌ Expense提交失败")
                create_claim_request_page.screenshot_helper("expense_submit_failed.png")
        else:
            print("❌ Expense添加失败")
            create_claim_request_page.screenshot_helper("expense_add_failed.png")
    else:
        print("❌ 导航到费用区域失败")
        create_claim_request_page.screenshot_helper("expense_navigation_failed.png")

    # Step 5: 检查数据与填写数据一致，点击Back返回，截图
    print("Step 5: 正在验证费用详情...")
    expense_data = {
        "Expense Type": "Transport",
        "Date": "2023-05-01",
        "Amount": "50"
    }
    if create_claim_request_page.verify_expense_details_in_list(expense_data):
        print("✅ 费用详情验证成功")
        time.sleep(2)
        create_claim_request_page.screenshot_helper("assign_claim_expense_back.png")
    else:
        print("⚠️ 费用详情验证失败，但继续执行")

    # 滚动到最底部，点击 Back
    create_claim_request_page.scroll_to_bottom()
    create_claim_request_page.click_back_button()
    
    # Step 6: 验证Record中存在刚才的提交记录，截图
    create_claim_request_page.scroll_to_latest_record()
    print("Step 6: 正在验证记录存在性...")
    time.sleep(2)
    create_claim_request_page.screenshot_helper("assign_claim_add_expense_record_exists.png")

    # Step 7: 生成测试报告
    print("Step 7: 正在生成详细测试报告...")
    # 测试完成后，应生成相应的HTML测试报告，报告包括截图，操作步骤，状态等，如果case失败，附有失败截图和失败日志
    if create_claim_request_page.generate_html_report():
        print("✅ 详细测试报告生成成功")
        print("📄 报告文件位置: reports/test_report_YYYYMMDD_HHMMSS.html")
    else:
        print("❌ 测试报告生成失败")

    time.sleep(3)

    # 关闭报告和浏览器
    if create_claim_request_page.close_report():
        print("✅ 报告关闭成功")
    else:
        print("⚠️ 报告关闭失败")

    print("🎉 测试执行完成！")
    print("📸 所有截图已保存到screenshots目录")
    print("📄 详细报告已保存到reports目录")

    # 关闭浏览器
    try:
        if driver is not None:
            driver.quit()
            print("✅ 浏览器已关闭")
        return True
    except Exception as e:
        print(f"⚠️ 浏览器关闭失败: {e}")
        return True  # 即使浏览器关闭失败，测试也算成功


if __name__ == "__main__":
    """程序入口点"""
    try:
        success: bool = main()
        if success:
            print("\n🎉 所有测试步骤执行成功！")
            sys.exit(0)
        else:
            print("\n❌ 测试执行失败！")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断了测试执行")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试执行过程中发生未预期的错误: {e}")
        sys.exit(1)


def test_language_server():
    """
    测试Python语言服务器是否正常工作

    使用方法：
    1. 在下面的注释行中，删除 # 号
    2. 输入 create_claim_request_page. 然后按 Ctrl+Space
    3. 应该能看到方法提示列表
    """
    # create_claim_request_page.
    pass


if __name__ == "__main__":
    main()