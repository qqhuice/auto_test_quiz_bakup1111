#!/usr/bin/env python3
"""
调试Assign Claim按钮定位问题
"""
import sys
sys.path.append('..')
from pages.orangehrm_claims_page import OrangeHRMClaimsPage
from pages.orangehrm_login_page import OrangeHRMLoginPage
from pages.orangehrm_dashboard_page import OrangeHRMDashboardPage
from utils.driver_manager import DriverManager
from selenium.webdriver.common.by import By
import time

def debug_assign_claim_button():
    """调试Assign Claim按钮定位"""
    # 创建驱动和页面对象
    driver_manager = DriverManager()
    driver = driver_manager.create_chrome_driver()

    try:
        print("=== 开始调试Assign Claim按钮定位 ===")
        
        # 登录流程
        print("1. 正在登录...")
        login_page = OrangeHRMLoginPage(driver)
        login_page.open_page()
        time.sleep(3)
        
        login_page.enter_username('Admin')
        login_page.enter_password('admin123')
        login_page.click_login_button()
        time.sleep(5)
        
        # 进入Claims页面
        print("2. 正在进入Claims页面...")
        dashboard_page = OrangeHRMDashboardPage(driver)
        dashboard_page.click_sidebar_menu_item('Claim')
        time.sleep(3)
        
        # 进入Employee Claims
        print("3. 正在进入Employee Claims...")
        claims_page = OrangeHRMClaimsPage(driver)
        claims_page.click_employee_claims()
        time.sleep(3)
        
        print(f"当前页面URL: {driver.current_url}")
        
        print("\n=== 查找页面中所有包含Assign的元素 ===")
        
        # 查找所有包含'Assign'文本的元素
        assign_elements = driver.find_elements(By.XPATH, '//*[contains(text(), "Assign")]')
        print(f"找到 {len(assign_elements)} 个包含'Assign'文本的元素")
        
        for i, elem in enumerate(assign_elements):
            try:
                tag_name = elem.tag_name
                text = elem.text.strip()
                is_displayed = elem.is_displayed()
                is_enabled = elem.is_enabled()
                classes = elem.get_attribute('class') or ''
                print(f"{i+1}. <{tag_name}> 文本:'{text}' 显示:{is_displayed} 启用:{is_enabled} class:'{classes}'")
            except Exception as e:
                print(f"{i+1}. 元素获取信息失败: {e}")
        
        print("\n=== 查找所有按钮元素 ===")
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        print(f"找到 {len(buttons)} 个按钮元素")
        
        assign_buttons = []
        for i, btn in enumerate(buttons):
            try:
                text = btn.text.strip()
                is_displayed = btn.is_displayed()
                classes = btn.get_attribute('class') or ''
                if 'Assign' in text or 'assign' in text.lower():
                    assign_buttons.append(btn)
                    print(f"按钮 {i+1}: 文本:'{text}' 显示:{is_displayed} class:'{classes}'")
            except:
                pass
        
        print("\n=== 查找所有链接元素 ===")
        links = driver.find_elements(By.TAG_NAME, 'a')
        print(f"找到 {len(links)} 个链接元素")
        
        assign_links = []
        for i, link in enumerate(links):
            try:
                text = link.text.strip()
                href = link.get_attribute('href') or ''
                is_displayed = link.is_displayed()
                if 'Assign' in text or 'assign' in text.lower():
                    assign_links.append(link)
                    print(f"链接 {i+1}: 文本:'{text}' 显示:{is_displayed} href:'{href}'")
            except:
                pass
        
        # 尝试更广泛的搜索
        print("\n=== 尝试更广泛的搜索策略 ===")
        
        # 搜索包含"Add"的元素（可能是Add Claim而不是Assign Claim）
        add_elements = driver.find_elements(By.XPATH, '//*[contains(text(), "Add")]')
        print(f"找到 {len(add_elements)} 个包含'Add'文本的元素")
        
        for i, elem in enumerate(add_elements):
            try:
                tag_name = elem.tag_name
                text = elem.text.strip()
                is_displayed = elem.is_displayed()
                if 'Claim' in text:
                    print(f"Add相关 {i+1}. <{tag_name}> 文本:'{text}' 显示:{is_displayed}")
            except:
                pass
        
        # 搜索包含"Create"的元素
        create_elements = driver.find_elements(By.XPATH, '//*[contains(text(), "Create")]')
        print(f"找到 {len(create_elements)} 个包含'Create'文本的元素")
        
        for i, elem in enumerate(create_elements):
            try:
                tag_name = elem.tag_name
                text = elem.text.strip()
                is_displayed = elem.is_displayed()
                if 'Claim' in text:
                    print(f"Create相关 {i+1}. <{tag_name}> 文本:'{text}' 显示:{is_displayed}")
            except:
                pass
        
        # 搜索所有可能的按钮文本
        possible_texts = ["Assign Claim", "Add Claim", "Create Claim", "New Claim", "+ Assign Claim"]
        print(f"\n=== 搜索可能的按钮文本 ===")
        
        for text in possible_texts:
            elements = driver.find_elements(By.XPATH, f'//*[contains(text(), "{text}")]')
            if elements:
                print(f"找到包含'{text}'的元素: {len(elements)}个")
                for elem in elements:
                    try:
                        print(f"  - <{elem.tag_name}> 显示:{elem.is_displayed()} 启用:{elem.is_enabled()}")
                    except:
                        pass
        
        # 保存页面源码和截图
        print("\n=== 保存调试信息 ===")
        with open('employee_claims_debug.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("页面源码已保存到: employee_claims_debug.html")
        
        driver.save_screenshot('employee_claims_debug.png')
        print("页面截图已保存到: employee_claims_debug.png")
        
        return assign_buttons, assign_links
        
    finally:
        driver.quit()

if __name__ == "__main__":
    debug_assign_claim_button()
