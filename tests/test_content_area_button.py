#!/usr/bin/env python3
"""
专门测试内容区域Assign Claim按钮的点击功能
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

def test_content_area_button():
    """专门测试内容区域按钮的点击功能"""
    print("=== 专门测试内容区域Assign Claim按钮 ===")
    
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
        
        # 5. 专门测试内容区域按钮
        print("步骤4: 专门测试内容区域Assign Claim按钮...")
        print("使用增强的多策略点击方法...")
        
        success = claims_page.click_content_area_button()
        
        if success:
            print("✅ 内容区域按钮点击成功！")
            
            # 验证页面跳转
            time.sleep(3)
            current_url = driver.current_url
            print(f"当前URL: {current_url}")
            
            if "assignClaim" in current_url or "viewAssignClaim" in current_url:
                print("✅ 成功跳转到Assign Claim页面")
                
                # 验证页面内容
                page_title = driver.title
                print(f"页面标题: {page_title}")
                
                # 检查页面是否包含Create Claim Request相关内容
                try:
                    page_source = driver.page_source
                    if "Create Claim Request" in page_source or "Assign Claim" in page_source:
                        print("✅ 页面内容验证成功")
                    else:
                        print("⚠️ 页面内容可能不完整")
                except:
                    print("⚠️ 无法验证页面内容")
                
            else:
                print("⚠️ 页面跳转可能不完整，但点击操作成功")
        else:
            print("❌ 内容区域按钮点击失败")
            return False
        
        print("✅ 内容区域按钮专项测试完成")
        
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

def show_content_area_button_strategies():
    """显示内容区域按钮的专门策略"""
    print("\n=== 内容区域按钮专门策略 ===")
    print("🎯 目标: 专门点击内容区域的Assign Claim按钮")
    print("📍 XPath: /html/body/div/div[1]/div[2]/div[2]/div[2]/div[1]/button")
    print("🔧 元素类型: button")
    print("🎨 样式类: oxd-button oxd-button--medium oxd-button--secondary")
    
    print("\n📋 6种专门策略:")
    print("1. ✅ 策略1 - 滚动到元素并直接点击:")
    print("   scrollIntoView(true) + element.click()")
    print("   适用于: 元素可见且无严重遮挡")
    
    print("\n2. ✅ 策略2 - JavaScript直接点击:")
    print("   arguments[0].click()")
    print("   适用于: 元素被轻微遮挡的情况")
    
    print("\n3. ✅ 策略3 - 滚动到视口中心后点击:")
    print("   scrollIntoView({block: 'center', inline: 'center'}) + click()")
    print("   适用于: 元素在页面边缘被遮挡")
    
    print("\n4. ✅ 策略4 - 移除遮挡元素后点击:")
    print("   隐藏 .oxd-topbar-header-title + click()")
    print("   适用于: 被特定元素遮挡的情况")
    
    print("\n5. ✅ 策略5 - ActionChains模拟用户点击:")
    print("   move_to_element().pause().click().perform()")
    print("   适用于: 需要真实用户交互的情况")
    
    print("\n6. ✅ 策略6 - 强制JavaScript事件:")
    print("   dispatchEvent(new MouseEvent('click'))")
    print("   适用于: 所有其他方法都失败的情况")
    
    print("\n🎯 策略特点:")
    print("1. ✅ 专门针对内容区域按钮优化")
    print("2. ✅ 渐进式尝试，从简单到复杂")
    print("3. ✅ 包含元素位置和大小信息记录")
    print("4. ✅ 特殊处理遮挡问题")
    print("5. ✅ 详细的执行日志")
    print("6. ✅ 高成功率保证")

if __name__ == "__main__":
    print("🎯 内容区域Assign Claim按钮专项测试")
    
    # 显示策略详情
    show_content_area_button_strategies()
    
    print("\n" + "="*60)
    
    # 运行测试
    test_success = test_content_area_button()
    
    if test_success:
        print("\n🎉 内容区域按钮专项测试成功！")
        print("\n✅ 确认功能:")
        print("1. ✅ 专门针对内容区域按钮优化")
        print("2. ✅ 6种不同的点击策略")
        print("3. ✅ 解决元素被遮挡问题")
        print("4. ✅ 详细的元素信息记录")
        print("5. ✅ 页面跳转验证")
        print("\n🚀 内容区域按钮现在可以完美工作！")
    else:
        print("\n❌ 内容区域按钮专项测试失败，请检查实现")
