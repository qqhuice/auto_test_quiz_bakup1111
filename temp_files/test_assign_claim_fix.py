#!/usr/bin/env python3
"""
测试修复后的Assign Claim按钮定位
"""
import sys
sys.path.append('..')
from pages.orangehrm_claims_page import OrangeHRMClaimsPage
from pages.orangehrm_login_page import OrangeHRMLoginPage
from pages.orangehrm_dashboard_page import OrangeHRMDashboardPage
from utils.driver_manager import DriverManager
import time

def test_assign_claim_button():
    """测试Assign Claim按钮定位修复"""
    print("=== 测试修复后的Assign Claim按钮定位 ===")
    
    # 创建驱动和页面对象
    driver_manager = DriverManager()
    driver = driver_manager.create_chrome_driver()

    try:
        # 登录流程
        print("1. 正在登录OrangeHRM...")
        login_page = OrangeHRMLoginPage(driver)
        login_page.open_page()
        time.sleep(3)
        
        login_page.enter_username('Admin')
        login_page.enter_password('admin123')
        login_page.click_login_button()
        time.sleep(5)
        print("✅ 登录成功")
        
        # 进入Claims页面
        print("2. 正在进入Claims页面...")
        dashboard_page = OrangeHRMDashboardPage(driver)
        dashboard_page.click_sidebar_menu_item('Claim')
        time.sleep(3)
        print("✅ 进入Claims页面成功")
        
        # 进入Employee Claims
        print("3. 正在进入Employee Claims...")
        claims_page = OrangeHRMClaimsPage(driver)
        claims_page.click_employee_claims()
        time.sleep(3)
        print("✅ 进入Employee Claims页面成功")
        
        # 测试Assign Claim按钮定位
        print("4. 正在测试Assign Claim按钮定位...")
        try:
            claims_page.click_assign_claim()
            print("🎉 Assign Claim按钮定位和点击成功！")
            
            # 验证是否进入了Create Claim Request页面
            time.sleep(3)
            current_url = driver.current_url
            print(f"当前页面URL: {current_url}")
            
            if "assignClaim" in current_url or "create" in current_url.lower():
                print("✅ 成功进入Create Claim Request页面")
                
                # 截图成功页面
                driver.save_screenshot("assign_claim_success.png")
                print("✅ 成功页面截图已保存: assign_claim_success.png")
                
                return True
            else:
                print("❌ 未能正确跳转到Create Claim Request页面")
                return False
                
        except Exception as e:
            print(f"❌ Assign Claim按钮定位失败: {e}")
            
            # 截图失败页面
            driver.save_screenshot("assign_claim_failed.png")
            print("❌ 失败页面截图已保存: assign_claim_failed.png")
            
            return False
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False
        
    finally:
        print("5. 正在关闭浏览器...")
        driver.quit()
        print("✅ 测试完成")

if __name__ == "__main__":
    success = test_assign_claim_button()
    if success:
        print("\n🎉 Assign Claim按钮定位修复成功！")
    else:
        print("\n❌ Assign Claim按钮定位仍需进一步修复")
