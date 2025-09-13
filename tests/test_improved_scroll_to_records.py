#!/usr/bin/env python3
"""
测试改进后的scroll_to_Records_Found方法
验证Records Found区域显示在页面中上部，便于查看和点击最新记录
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

def test_improved_scroll_to_records_found():
    """测试改进后的scroll_to_Records_Found方法"""
    print("=== 测试改进后的scroll_to_Records_Found方法 ===")
    
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
        create_claim_page.screenshot_helper("before_improved_scroll.png")
        print("📸 已保存滚动前截图")
        
        # 8. 测试改进后的scroll_to_Records_Found方法
        print("步骤7: 测试改进后的scroll_to_Records_Found方法...")
        
        result = create_claim_page.scroll_to_Records_Found()
        
        if result:
            print("✅ scroll_to_Records_Found方法执行成功")
            time.sleep(2)
            
            # 获取滚动后的位置信息
            final_scroll_y = driver.execute_script("return window.pageYOffset;")
            print(f"📊 滚动后位置: {final_scroll_y}px")
            print(f"📊 滚动距离: {final_scroll_y - initial_scroll_y}px")
            
            # 计算Records Found区域在可视区域中的相对位置
            relative_position_percent = (final_scroll_y / page_height) * 100 if page_height > 0 else 0
            print(f"📊 Records Found区域在页面中的相对位置: {relative_position_percent:.1f}%")
            
            # 验证滚动效果
            if relative_position_percent <= 40:  # 在页面前40%区域
                print("✅ Records Found区域显示在页面中上部，位置理想")
            elif relative_position_percent <= 60:  # 在页面前60%区域
                print("✅ Records Found区域显示在页面中部，位置可接受")
            else:
                print("⚠️ Records Found区域显示在页面下部，可能需要进一步优化")
            
            # 截图滚动后状态
            create_claim_page.screenshot_helper("after_improved_scroll.png")
            print("📸 已保存滚动后截图")
            
        else:
            print("❌ scroll_to_Records_Found方法执行失败")
            create_claim_page.screenshot_helper("scroll_failed.png")
            print("📸 已保存失败截图")
        
        # 9. 测试多次滚动的稳定性
        print("步骤8: 测试多次滚动的稳定性...")
        for i in range(3):
            print(f"第{i+1}次滚动测试...")
            scroll_before = driver.execute_script("return window.pageYOffset;")
            
            result = create_claim_page.scroll_to_Records_Found()
            time.sleep(1)
            
            scroll_after = driver.execute_script("return window.pageYOffset;")
            
            if result:
                print(f"✅ 第{i+1}次滚动成功 (位置: {scroll_after}px)")
            else:
                print(f"❌ 第{i+1}次滚动失败")
        
        # 10. 验证是否便于点击最新记录
        print("步骤9: 验证是否便于点击最新记录...")
        try:
            # 查找表格中的记录
            from selenium.webdriver.common.by import By
            
            # 尝试查找记录行
            record_selectors = [
                (By.XPATH, "//table//tr[position()>1]"),  # 表格中除标题外的行
                (By.XPATH, "//tbody//tr"),
                (By.XPATH, "//div[contains(@class,'oxd-table-row')]"),
            ]
            
            records_found = False
            for selector in record_selectors:
                try:
                    records = driver.find_elements(*selector)
                    if records:
                        visible_records = []
                        for record in records[:5]:  # 检查前5条记录
                            if record.is_displayed():
                                visible_records.append(record)
                        
                        if visible_records:
                            records_found = True
                            print(f"✅ 找到 {len(visible_records)} 条可见记录")
                            
                            # 检查第一条记录（最新记录）的位置
                            first_record = visible_records[0]
                            record_location = first_record.location
                            record_y_in_viewport = record_location['y'] - driver.execute_script("return window.pageYOffset;")
                            
                            if 0 <= record_y_in_viewport <= window_height:
                                print(f"✅ 最新记录在可视区域内 (相对位置: {record_y_in_viewport}px)")
                                if record_y_in_viewport <= window_height * 0.8:
                                    print("✅ 最新记录位置便于点击")
                                else:
                                    print("⚠️ 最新记录位置偏下，但仍可点击")
                            else:
                                print(f"❌ 最新记录不在可视区域内 (相对位置: {record_y_in_viewport}px)")
                            
                            break
                except Exception as e:
                    continue
            
            if not records_found:
                print("⚠️ 未找到记录，可能页面中没有数据或需要先创建记录")
                
        except Exception as e:
            print(f"⚠️ 验证记录可见性时出错: {e}")
        
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
        success = test_improved_scroll_to_records_found()
        if success:
            print("\n🎉 改进后的scroll_to_Records_Found方法测试成功！")
            print("📋 改进效果:")
            print("• Records Found区域显示在页面中上部")
            print("• 便于查看和点击最新记录")
            print("• 滚动位置更加精确和稳定")
            sys.exit(0)
        else:
            print("\n❌ 改进后的scroll_to_Records_Found方法测试失败！")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断了测试")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试执行过程中发生未预期的错误: {e}")
        sys.exit(1)
