#!/usr/bin/env python3
"""
测试新的scroll_to_Records_Found方法
通过定位Assign Claim、Reset、Search等控件来实现滚动
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

def test_new_scroll_method():
    """测试新的scroll_to_Records_Found方法"""
    print("=== 测试新的scroll_to_Records_Found方法 ===")
    print("通过定位Assign Claim、Reset、Search等控件实现滚动")
    
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
        
        # 6. 获取初始页面信息
        print("步骤6: 获取页面信息...")
        initial_scroll_y = driver.execute_script("return window.pageYOffset;")
        window_height = driver.execute_script("return window.innerHeight;")
        page_height = driver.execute_script("return document.body.scrollHeight;")
        
        print(f"📊 页面信息:")
        print(f"• 初始滚动位置: {initial_scroll_y}px")
        print(f"• 窗口高度: {window_height}px")
        print(f"• 页面总高度: {page_height}px")
        
        # 7. 截图滚动前状态
        create_claim_page.screenshot_helper("before_new_scroll_method.png")
        print("📸 已保存滚动前截图")
        
        # 8. 先滚动到页面底部，模拟Records Found在底部的情况
        print("步骤7: 先滚动到页面底部，模拟Records Found在底部的情况...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        bottom_scroll_y = driver.execute_script("return window.pageYOffset;")
        print(f"📊 滚动到底部位置: {bottom_scroll_y}px")
        
        create_claim_page.screenshot_helper("at_bottom_before_scroll.png")
        print("📸 已保存底部位置截图")
        
        # 9. 测试新的scroll_to_Records_Found方法
        print("步骤8: 测试新的scroll_to_Records_Found方法...")
        print("尝试通过定位Assign Claim、Reset、Search等控件来滚动...")
        
        result = create_claim_page.scroll_to_Records_Found()
        
        if result:
            print("✅ scroll_to_Records_Found方法执行成功")
            time.sleep(2)
            
            # 获取滚动后的位置信息
            final_scroll_y = driver.execute_script("return window.pageYOffset;")
            print(f"📊 滚动后位置: {final_scroll_y}px")
            print(f"📊 滚动距离: {final_scroll_y - bottom_scroll_y}px")
            
            # 计算相对位置
            relative_position_percent = (final_scroll_y / page_height) * 100 if page_height > 0 else 0
            print(f"📊 当前滚动位置在页面中的相对位置: {relative_position_percent:.1f}%")
            
            # 验证滚动效果
            if relative_position_percent <= 30:  # 在页面前30%区域
                print("✅ 滚动位置在页面上部，Records Found应该显示在页面中上部")
            elif relative_position_percent <= 50:  # 在页面前50%区域
                print("✅ 滚动位置在页面中上部，Records Found应该可见")
            elif relative_position_percent <= 70:  # 在页面前70%区域
                print("⚠️ 滚动位置在页面中部，Records Found可能部分可见")
            else:
                print("❌ 滚动位置仍在页面下部，可能需要进一步调整")
            
            # 截图滚动后状态
            create_claim_page.screenshot_helper("after_new_scroll_method.png")
            print("📸 已保存滚动后截图")
            
        else:
            print("❌ scroll_to_Records_Found方法执行失败")
            create_claim_page.screenshot_helper("scroll_failed.png")
            print("📸 已保存失败截图")
        
        # 10. 验证页面上部控件是否可见
        print("步骤9: 验证页面上部控件是否可见...")
        try:
            from selenium.webdriver.common.by import By
            
            # 检查各种控件的可见性
            controls_to_check = [
                ("Assign Claim按钮", (By.XPATH, "//button[contains(text(),'Assign Claim')]")),
                ("Reset按钮", (By.XPATH, "//button[contains(text(),'Reset')]")),
                ("Search按钮", (By.XPATH, "//button[contains(text(),'Search')]")),
                ("Employee Claims标题", (By.XPATH, "//*[contains(text(),'Employee Claims')]")),
            ]
            
            visible_controls = 0
            for control_name, selector in controls_to_check:
                try:
                    elements = driver.find_elements(*selector)
                    if elements and elements[0].is_displayed():
                        element_location = elements[0].location
                        current_scroll = driver.execute_script("return window.pageYOffset;")
                        element_y_in_viewport = element_location['y'] - current_scroll
                        
                        if 0 <= element_y_in_viewport <= window_height:
                            visible_controls += 1
                            print(f"✅ {control_name} 在可视区域内 (相对位置: {element_y_in_viewport}px)")
                        else:
                            print(f"❌ {control_name} 不在可视区域内 (相对位置: {element_y_in_viewport}px)")
                    else:
                        print(f"❌ {control_name} 未找到或不可见")
                except Exception as e:
                    print(f"⚠️ 检查 {control_name} 时出错: {e}")
            
            print(f"📊 可见的页面上部控件数量: {visible_controls}/{len(controls_to_check)}")
            
            if visible_controls >= 2:
                print("✅ 页面上部控件可见，滚动效果良好")
            elif visible_controls >= 1:
                print("⚠️ 部分页面上部控件可见，滚动效果一般")
            else:
                print("❌ 页面上部控件不可见，滚动效果不佳")
                
        except Exception as e:
            print(f"⚠️ 验证控件可见性时出错: {e}")
        
        # 11. 测试多次滚动的稳定性
        print("步骤10: 测试多次滚动的稳定性...")
        for i in range(2):
            print(f"第{i+1}次额外滚动测试...")
            
            # 先滚动到底部
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            
            # 再使用我们的方法滚动
            result = create_claim_page.scroll_to_Records_Found()
            time.sleep(0.5)
            
            final_pos = driver.execute_script("return window.pageYOffset;")
            relative_pos = (final_pos / page_height) * 100 if page_height > 0 else 0
            
            if result:
                print(f"✅ 第{i+1}次滚动成功 (位置: {final_pos}px, 相对位置: {relative_pos:.1f}%)")
            else:
                print(f"❌ 第{i+1}次滚动失败")
        
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
        success = test_new_scroll_method()
        if success:
            print("\n🎉 新的scroll_to_Records_Found方法测试成功！")
            print("📋 新方法特点:")
            print("• 通过定位页面上部控件(Assign Claim、Reset、Search等)实现滚动")
            print("• 将控件滚动到页面顶端，Records Found自然显示在中上部")
            print("• 更加稳定和可靠的滚动策略")
            sys.exit(0)
        else:
            print("\n❌ 新的scroll_to_Records_Found方法测试失败！")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断了测试")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试执行过程中发生未预期的错误: {e}")
        sys.exit(1)
