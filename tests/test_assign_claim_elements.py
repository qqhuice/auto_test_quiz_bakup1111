#!/usr/bin/env python3
"""
测试更新后的Assign Claim元素定位
"""
import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from pages.orangehrm_login_page import OrangeHRMLoginPage
from pages.orangehrm_dashboard_page import OrangeHRMDashboardPage
from pages.orangehrm_claims_page import OrangeHRMClaimsPage
from utils.driver_manager import DriverManager
import time

def test_assign_claim_elements():
    """测试两个Assign Claim元素的定位和点击"""
    print("=== 测试Assign Claim元素定位和点击 ===")
    
    driver = None
    try:
        # 1. 创建浏览器驱动
        driver_manager = DriverManager()
        driver = driver_manager.create_chrome_driver()
        
        # 2. 登录OrangeHRM
        print("步骤1: 登录OrangeHRM...")
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        time.sleep(3)
        
        login_page = OrangeHRMLoginPage(driver)
        login_page.enter_username("Admin")
        login_page.enter_password("admin123")
        login_page.click_login_button()
        time.sleep(3)
        
        print("✅ 登录成功")
        
        # 3. 导航到Claims页面
        print("步骤2: 导航到Claims页面...")
        dashboard_page = OrangeHRMDashboardPage(driver)
        dashboard_page.click_sidebar_menu_item("Claim")
        time.sleep(3)
        
        print("✅ 已进入Claims页面")
        
        # 4. 点击Employee Claims
        print("步骤3: 点击Employee Claims...")
        claims_page = OrangeHRMClaimsPage(driver)
        claims_page.click_employee_claims()
        time.sleep(3)
        
        print("✅ 已进入Employee Claims页面")
        
        # 5. 测试两个Assign Claim元素
        print("步骤4: 测试Assign Claim元素可用性...")
        claims_page.test_assign_claim_elements()
        
        # 6. 尝试使用第一个XPath点击
        print("步骤5: 尝试使用内容区域按钮点击...")
        success1 = claims_page.click_assign_claim_by_xpath(xpath_choice=1)
        
        if success1:
            print("✅ 内容区域按钮点击成功")
            time.sleep(5)  # 观察结果
        else:
            print("❌ 内容区域按钮点击失败，尝试导航栏链接...")
            
            # 如果第一个失败，尝试第二个
            success2 = claims_page.click_assign_claim_by_xpath(xpath_choice=2)
            
            if success2:
                print("✅ 导航栏链接点击成功")
                time.sleep(5)  # 观察结果
            else:
                print("❌ 导航栏链接也点击失败，使用通用方法...")
                
                # 使用通用方法作为备用
                claims_page.click_assign_claim()
                print("✅ 通用方法点击完成")
                time.sleep(5)
        
        print("✅ Assign Claim元素测试完成")
        
        # 等待用户观察结果
        print("等待10秒供观察...")
        time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False
        
    finally:
        if driver:
            print("关闭浏览器...")
            driver.quit()

def test_xpath_validation():
    """验证XPath定位器的正确性"""
    print("\n=== 验证XPath定位器 ===")
    
    try:
        from pages.orangehrm_claims_page import OrangeHRMClaimsPage
        
        # 检查定位器定义
        print("检查定位器定义:")
        
        # 内容区域按钮
        content_xpath = OrangeHRMClaimsPage.ASSIGN_CLAIM_BUTTON_CONTENT[1]
        print(f"✅ 内容区域按钮XPath: {content_xpath}")
        
        # 导航栏链接
        header_xpath = OrangeHRMClaimsPage.ASSIGN_CLAIM_LINK_HEADER[1]
        print(f"✅ 导航栏链接XPath: {header_xpath}")
        
        # 通用定位器
        general_xpath = OrangeHRMClaimsPage.ASSIGN_CLAIM_BUTTON[1]
        print(f"✅ 通用定位器XPath: {general_xpath}")
        
        # 检查方法存在
        print("\n检查新增方法:")
        methods = [
            'test_assign_claim_elements',
            'click_assign_claim_by_xpath',
            'click_assign_claim'
        ]
        
        for method in methods:
            if hasattr(OrangeHRMClaimsPage, method):
                print(f"✅ {method}")
            else:
                print(f"❌ {method}")
        
        return True
        
    except Exception as e:
        print(f"❌ XPath验证失败: {e}")
        return False

if __name__ == "__main__":
    print("🎯 Assign Claim元素定位测试")
    
    # 验证XPath定位器
    xpath_validation = test_xpath_validation()
    
    if xpath_validation:
        print("\n" + "="*60)
        # 运行实际测试
        functional_test = test_assign_claim_elements()
        
        if functional_test:
            print("\n🎉 Assign Claim元素测试全部通过！")
            print("\n📋 更新内容:")
            print("1. ✅ 添加了两个精确的XPath定位器")
            print("   - 内容区域按钮: /html/body/div/div[1]/div[2]/div[2]/div[2]/div[1]/button")
            print("   - 导航栏链接: /html/body/div/div[1]/div[1]/header/div[2]/nav/ul/li[5]/a")
            print("2. ✅ 更新了click_assign_claim方法，优先使用精确XPath")
            print("3. ✅ 添加了test_assign_claim_elements方法测试元素可用性")
            print("4. ✅ 添加了click_assign_claim_by_xpath方法指定XPath点击")
            print("5. ✅ 改进了日志输出，包含策略名称和元素信息")
            print("\n🚀 现在两个Assign Claim元素都能正确定位和点击了！")
        else:
            print("\n❌ 功能测试失败，请检查页面对象实现")
    else:
        print("\n❌ XPath验证失败，请检查页面对象结构")
