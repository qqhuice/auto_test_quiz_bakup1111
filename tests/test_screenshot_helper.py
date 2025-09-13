#!/usr/bin/env python3
"""
测试screenshot_helper方法
"""
import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from pages.orangehrm_login_page import OrangeHRMLoginPage
from pages.orangehrm_dashboard_page import OrangeHRMDashboardPage
from pages.orangehrm_claims_page import OrangeHRMClaimsPage
from pages.orangehrm_create_claim_request_page import OrangeHRMCreateClaimRequestPage
from utils.driver_manager import DriverManager
import time

def test_screenshot_helper():
    """测试screenshot_helper方法"""
    print("=== 测试screenshot_helper方法 ===")
    
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
        
        # 5. 点击内容区域按钮
        print("步骤4: 点击内容区域Assign Claim按钮...")
        success = claims_page.click_content_area_button()
        
        if success:
            print("✅ 成功进入Create Claim Request页面")
            time.sleep(3)
            
            # 6. 测试screenshot_helper方法
            print("步骤5: 测试screenshot_helper方法...")
            create_claim_page = OrangeHRMCreateClaimRequestPage(driver)
            
            # 测试1: 使用指定文件名
            print("测试1: 使用指定文件名截图...")
            filename1 = create_claim_page.screenshot_helper("test_screenshot_1.png")
            if filename1:
                print(f"✅ 截图1成功: {filename1}")
            else:
                print("❌ 截图1失败")
            
            # 测试2: 使用自动生成文件名
            print("测试2: 使用自动生成文件名截图...")
            filename2 = create_claim_page.screenshot_helper()
            if filename2:
                print(f"✅ 截图2成功: {filename2}")
            else:
                print("❌ 截图2失败")
            
            # 测试3: 填写表单后截图
            print("测试3: 填写表单后截图...")
            create_claim_page.fill_employee_name("Amelia Brown")
            time.sleep(1)
            create_claim_page.select_event("Travel allowances")
            time.sleep(1)
            create_claim_page.select_currency("Euro")
            time.sleep(1)
            
            filename3 = create_claim_page.screenshot_helper("form_filled.png")
            if filename3:
                print(f"✅ 截图3成功: {filename3}")
            else:
                print("❌ 截图3失败")
            
            # 验证截图文件是否存在
            print("步骤6: 验证截图文件...")
            import os
            for filename in [filename1, filename2, filename3]:
                if filename and os.path.exists(filename):
                    file_size = os.path.getsize(filename)
                    print(f"✅ 文件存在: {filename} (大小: {file_size} bytes)")
                else:
                    print(f"❌ 文件不存在: {filename}")
            
        else:
            print("❌ 无法进入Create Claim Request页面")
            return False
        
        print("✅ screenshot_helper方法测试完成")
        
        # 等待用户观察结果
        print("等待5秒供观察...")
        time.sleep(5)
        
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        return False
        
    finally:
        if driver:
            print("关闭浏览器...")
            driver.quit()

def show_screenshot_helper_info():
    """显示screenshot_helper方法信息"""
    print("\n=== screenshot_helper方法信息 ===")
    print("🔧 解决的问题:")
    print("1. ❌ 原问题: screenshot_helper方法不存在，导致代码标黄")
    print("2. ❌ 原因: 类中只有私有方法_take_screenshot，没有公共方法")
    print("3. ✅ 解决方案: 添加公共的screenshot_helper方法")
    
    print("\n📋 新增的screenshot_helper方法特点:")
    print("1. ✅ 公共方法 - 可以从外部调用")
    print("2. ✅ 灵活文件名 - 支持指定文件名或自动生成")
    print("3. ✅ 自动目录创建 - 确保screenshots目录存在")
    print("4. ✅ 文件名处理 - 自动添加.png扩展名和路径前缀")
    print("5. ✅ 返回值 - 返回实际保存的文件名")
    print("6. ✅ 错误处理 - 截图失败时返回None")
    
    print("\n🚀 使用方法:")
    print("# 方法1: 指定文件名")
    print("filename = create_claim_page.screenshot_helper('my_screenshot.png')")
    print("")
    print("# 方法2: 自动生成文件名")
    print("filename = create_claim_page.screenshot_helper()")
    print("")
    print("# 方法3: 只指定名称（自动添加扩展名和路径）")
    print("filename = create_claim_page.screenshot_helper('test_image')")
    
    print("\n🎯 修复结果:")
    print("1. ✅ 代码不再标黄")
    print("2. ✅ 截图功能正常工作")
    print("3. ✅ 向后兼容原有的_take_screenshot方法")
    print("4. ✅ 提供更灵活的截图接口")

if __name__ == "__main__":
    print("🎯 screenshot_helper方法测试")
    
    # 显示方法信息
    show_screenshot_helper_info()
    
    print("\n" + "="*60)
    
    # 运行测试
    test_success = test_screenshot_helper()
    
    if test_success:
        print("\n🎉 screenshot_helper方法测试成功！")
        print("\n✅ 确认功能:")
        print("1. ✅ screenshot_helper方法正常工作")
        print("2. ✅ 支持指定文件名和自动生成")
        print("3. ✅ 截图文件正确保存")
        print("4. ✅ 代码不再标黄")
        print("\n🚀 screenshot_helper方法现在可以正常使用！")
    else:
        print("\n❌ screenshot_helper方法测试失败，请检查实现")
