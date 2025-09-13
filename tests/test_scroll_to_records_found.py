#!/usr/bin/env python3
"""
测试scroll_to_Records_Found方法
"""
import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from selenium import webdriver
from pages.orangehrm_login_page import OrangeHRMLoginPage
from pages.orangehrm_dashboard_page import OrangeHRMDashboardPage
from pages.orangehrm_claims_page import OrangeHRMClaimsPage
from pages.orangehrm_create_claim_request_page import OrangeHRMCreateClaimRequestPage
from utils.driver_manager import DriverManager

def test_scroll_to_records_found():
    """测试scroll_to_Records_Found方法"""
    print("=== 测试scroll_to_Records_Found方法 ===")
    
    driver = None
    try:
        # 1. 启动浏览器
        print("步骤1: 启动Chrome浏览器...")
        driver_manager = DriverManager()
        driver = driver_manager.create_chrome_driver()
        driver.maximize_window()
        print("✅ 浏览器启动成功")
        
        # 2. 登录
        print("步骤2: 登录OrangeHRM...")
        login_page = OrangeHRMLoginPage(driver)
        login_page.open_page()
        time.sleep(2)

        login_page.login_with_default_credentials()
        time.sleep(3)
        print("✅ 登录成功")
        
        # 3. 导航到Claims页面
        print("步骤3: 导航到Claims页面...")
        dashboard_page = OrangeHRMDashboardPage(driver)
        dashboard_page.click_claims_menu()
        time.sleep(3)
        print("✅ 已进入Claims页面")
        
        # 4. 进入Employee Claims
        print("步骤4: 进入Employee Claims...")
        claims_page = OrangeHRMClaimsPage(driver)
        claims_page.click_employee_claims()
        time.sleep(3)
        print("✅ 已进入Employee Claims页面")
        
        # 5. 创建Create Claim Request页面对象
        print("步骤5: 创建Create Claim Request页面对象...")
        create_claim_page = OrangeHRMCreateClaimRequestPage(driver)
        
        # 6. 测试scroll_to_Records_Found方法
        print("步骤6: 测试scroll_to_Records_Found方法...")
        
        # 先截图当前页面状态
        create_claim_page.screenshot_helper("before_scroll_to_records_found.png")
        print("📸 已保存滚动前截图")
        
        # 执行滚动到Records Found区域
        result = create_claim_page.scroll_to_Records_Found()
        
        if result:
            print("✅ scroll_to_Records_Found方法执行成功")
            time.sleep(2)
            
            # 截图滚动后的状态
            create_claim_page.screenshot_helper("after_scroll_to_records_found.png")
            print("📸 已保存滚动后截图")
            
        else:
            print("❌ scroll_to_Records_Found方法执行失败")
            create_claim_page.screenshot_helper("scroll_to_records_found_failed.png")
            print("📸 已保存失败截图")
        
        # 7. 测试多次滚动
        print("步骤7: 测试多次滚动...")
        for i in range(3):
            print(f"第{i+1}次滚动...")
            result = create_claim_page.scroll_to_Records_Found()
            if result:
                print(f"✅ 第{i+1}次滚动成功")
            else:
                print(f"❌ 第{i+1}次滚动失败")
            time.sleep(1)
        
        # 8. 验证页面元素
        print("步骤8: 验证页面元素...")
        try:
            # 检查是否能找到表格或记录相关元素
            from selenium.webdriver.common.by import By
            
            table_elements = driver.find_elements(By.TAG_NAME, "table")
            if table_elements:
                print(f"✅ 找到 {len(table_elements)} 个表格元素")
            else:
                print("⚠️ 未找到表格元素")
            
            record_elements = driver.find_elements(By.XPATH, "//*[contains(text(),'record')]")
            if record_elements:
                print(f"✅ 找到 {len(record_elements)} 个包含'record'的元素")
            else:
                print("⚠️ 未找到包含'record'的元素")
                
        except Exception as e:
            print(f"⚠️ 验证页面元素时出错: {e}")
        
        print("✅ 测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        if driver:
            try:
                create_claim_page = OrangeHRMCreateClaimRequestPage(driver)
                create_claim_page.screenshot_helper("test_error.png")
                print("📸 已保存错误截图")
            except:
                pass
        return False
        
    finally:
        # 关闭浏览器
        if driver:
            try:
                time.sleep(2)
                driver.quit()
                print("✅ 浏览器已关闭")
            except Exception as e:
                print(f"⚠️ 关闭浏览器时出错: {e}")

if __name__ == "__main__":
    """程序入口点"""
    try:
        success = test_scroll_to_records_found()
        if success:
            print("\n🎉 scroll_to_Records_Found方法测试成功！")
            sys.exit(0)
        else:
            print("\n❌ scroll_to_Records_Found方法测试失败！")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断了测试")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试执行过程中发生未预期的错误: {e}")
        sys.exit(1)
