#!/usr/bin/env python3
"""
快速测试优化后的scroll_to_Records_Found方法
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

def test_optimized_scroll():
    """快速测试优化后的滚动方法"""
    print("=== 快速测试优化后的scroll_to_Records_Found方法 ===")
    
    driver = None
    try:
        # 启动浏览器并登录
        print("启动浏览器并登录...")
        driver_manager = DriverManager()
        driver = driver_manager.create_chrome_driver()
        driver.maximize_window()
        
        # 登录
        login_page = OrangeHRMLoginPage(driver)
        login_page.open_page()
        time.sleep(2)
        login_page.login_with_default_credentials()
        time.sleep(3)
        
        # 导航到Employee Claims页面
        dashboard_page = OrangeHRMDashboardPage(driver)
        dashboard_page.click_claims_menu()
        time.sleep(3)
        
        claims_page = OrangeHRMClaimsPage(driver)
        claims_page.click_employee_claims()
        time.sleep(3)
        
        # 创建页面对象
        create_claim_page = OrangeHRMCreateClaimRequestPage(driver)
        
        # 获取页面信息
        page_height = driver.execute_script("return document.body.scrollHeight;")
        window_height = driver.execute_script("return window.innerHeight;")
        print(f"页面高度: {page_height}px, 窗口高度: {window_height}px")
        
        # 先滚动到底部
        print("先滚动到页面底部...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        bottom_position = driver.execute_script("return window.pageYOffset;")
        print(f"底部位置: {bottom_position}px")
        
        # 截图底部状态
        create_claim_page.screenshot_helper("optimized_test_bottom.png")
        
        # 测试优化后的滚动方法
        print("测试优化后的scroll_to_Records_Found方法...")
        result = create_claim_page.scroll_to_Records_Found()
        
        if result:
            # 获取滚动后位置
            final_position = driver.execute_script("return window.pageYOffset;")
            relative_position = (final_position / page_height) * 100 if page_height > 0 else 0
            
            print(f"✅ 滚动成功!")
            print(f"滚动后位置: {final_position}px")
            print(f"相对位置: {relative_position:.1f}%")
            
            if relative_position <= 30:
                print("✅ 位置理想 - Records Found应该显示在页面中上部")
            elif relative_position <= 50:
                print("✅ 位置良好 - Records Found应该可见")
            else:
                print("⚠️ 位置仍需优化")
            
            # 截图滚动后状态
            create_claim_page.screenshot_helper("optimized_test_after.png")
            
        else:
            print("❌ 滚动失败")
            create_claim_page.screenshot_helper("optimized_test_failed.png")
        
        print("测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试出错: {e}")
        return False
        
    finally:
        if driver:
            time.sleep(2)
            driver.quit()

if __name__ == "__main__":
    test_optimized_scroll()
