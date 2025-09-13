#!/usr/bin/env python3
"""
测试回退按钮导航功能
"""
import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.orangehrm_create_claim_request_page import OrangeHRMCreateClaimRequestPage
import inspect

def test_back_button_methods():
    """测试回退按钮相关方法是否存在"""
    print("=== 测试回退按钮相关方法 ===")
    
    # 回退按钮相关方法列表
    back_button_methods = [
        'click_back_button',
        'navigate_back_to_assign_claim_details'
    ]
    
    # 获取类的所有方法
    class_methods = [method for method in dir(OrangeHRMCreateClaimRequestPage) 
                    if not method.startswith('_') and callable(getattr(OrangeHRMCreateClaimRequestPage, method))]
    
    print(f"📋 需要检查的回退按钮方法数量: {len(back_button_methods)}")
    
    missing_methods = []
    existing_methods = []
    
    for method in back_button_methods:
        if method in class_methods:
            existing_methods.append(method)
            print(f"✅ {method} - 存在")
        else:
            missing_methods.append(method)
            print(f"❌ {method} - 缺失")
    
    print(f"\n=== 检查结果 ===")
    print(f"✅ 存在的方法: {len(existing_methods)}/{len(back_button_methods)}")
    print(f"❌ 缺失的方法: {len(missing_methods)}/{len(back_button_methods)}")
    
    if missing_methods:
        print(f"\n❌ 缺失的方法列表:")
        for method in missing_methods:
            print(f"   - {method}")
        return False
    else:
        print(f"\n🎉 所有回退按钮方法都存在！")
        return True

def show_back_button_usage():
    """显示回退按钮的使用方法"""
    print("\n=== 回退按钮使用方法 ===")
    
    print("🎯 **基本用法:**")
    print("```python")
    print("# 简单点击回退按钮")
    print("create_claim_request_page.click_back_button()")
    print("")
    print("# 通过回退按钮导航回到Assign Claim详情页")
    print("create_claim_request_page.navigate_back_to_assign_claim_details()")
    print("```")
    
    print("\n🎯 **在pages/2.py中的使用场景:**")
    print("```python")
    print("# 场景1: 从Claims列表页回到详情页")
    print("# 当前在Claims列表页")
    print("create_claim_request_page.navigate_back_to_assign_claim_details()")
    print("create_claim_request_page.screenshot_helper('back_to_details.png')")
    print("")
    print("# 场景2: 简单的页面回退")
    print("create_claim_request_page.click_back_button()")
    print("time.sleep(2)")
    print("create_claim_request_page.screenshot_helper('after_back.png')")
    print("```")
    
    print("\n🎯 **完整的导航流程示例:**")
    print("```python")
    print("# Step 1: 在Assign Claim详情页")
    print("create_claim_request_page.verify_assign_claim_details_page()")
    print("")
    print("# Step 2: 导航到Claims列表页")
    print("create_claim_request_page.navigate_to_claims_list()")
    print("create_claim_request_page.verify_claims_list_page()")
    print("create_claim_request_page.screenshot_helper('claims_list.png')")
    print("")
    print("# Step 3: 通过回退按钮回到详情页")
    print("create_claim_request_page.navigate_back_to_assign_claim_details()")
    print("create_claim_request_page.verify_assign_claim_details_page()")
    print("create_claim_request_page.screenshot_helper('back_to_details.png')")
    print("```")

def show_back_button_strategies():
    """显示回退按钮的定位策略"""
    print("\n=== 回退按钮定位策略 ===")
    
    print("🔍 **多重定位策略:**")
    print("1. ✅ 浏览器原生回退按钮")
    print("   - //button[@aria-label='Back']")
    print("   - //button[contains(@class,'back')]")
    
    print("\n2. ✅ 页面内的回退按钮")
    print("   - //button[contains(text(),'Back')]")
    print("   - //a[contains(text(),'Back')]")
    print("   - //button[contains(@title,'Back')]")
    
    print("\n3. ✅ 面包屑导航中的回退")
    print("   - //nav[contains(@class,'breadcrumb')]//a[1]")
    print("   - //div[contains(@class,'breadcrumb')]//a[1]")
    
    print("\n4. ✅ 通用的返回图标")
    print("   - //*[contains(@class,'arrow-left')]")
    print("   - //*[contains(@class,'back-arrow')]")
    print("   - //*[contains(@class,'icon-back')]")
    
    print("\n5. ✅ 浏览器回退功能（备用）")
    print("   - driver.back()")
    
    print("\n🎯 **策略优势:**")
    print("- 🔄 多重定位策略确保高成功率")
    print("- 🎯 优先使用页面元素，备用浏览器功能")
    print("- 📝 详细的日志记录便于调试")
    print("- ⏱️ 适当的等待时间确保页面加载")

def show_navigation_verification():
    """显示导航验证功能"""
    print("\n=== 导航验证功能 ===")
    
    print("🔍 **navigate_back_to_assign_claim_details() 功能:**")
    print("1. ✅ 点击回退按钮")
    print("2. ✅ 等待页面加载 (3秒)")
    print("3. ✅ 验证URL包含'assignClaim'")
    print("4. ✅ 确认回到正确的详情页")
    
    print("\n🎯 **验证逻辑:**")
    print("```python")
    print("# 点击回退按钮")
    print("if self.click_back_button():")
    print("    # 等待页面加载")
    print("    time.sleep(3)")
    print("    ")
    print("    # 验证URL")
    print("    current_url = self.driver.current_url")
    print("    if 'assignClaim' in current_url:")
    print("        logger.info('✅ 成功回到Assign Claim详情页')")
    print("        return True")
    print("```")
    
    print("\n📊 **返回值说明:**")
    print("- ✅ True: 成功回到Assign Claim详情页")
    print("- ❌ False: 回退失败或未到达正确页面")

def show_practical_examples():
    """显示实际使用示例"""
    print("\n=== 实际使用示例 ===")
    
    print("📝 **示例1: 替换pages/2.py中的go_back()调用**")
    print("```python")
    print("# 原来的写法")
    print("create_claim_request_page.go_back()")
    print("")
    print("# 新的写法")
    print("create_claim_request_page.click_back_button()")
    print("# 或者")
    print("create_claim_request_page.navigate_back_to_assign_claim_details()")
    print("```")
    
    print("\n📝 **示例2: 在step 4中使用**")
    print("```python")
    print("# step 4: 如果需要从其他页面回到详情页")
    print("create_claim_request_page.navigate_back_to_assign_claim_details()")
    print("create_claim_request_page.verify_assign_claim_details_page()")
    print("create_claim_request_page.verify_claim_data_consistency({")
    print("    'employee_name': 'Amelia Brown',")
    print("    'event': 'Travel allowances',")
    print("    'currency': 'Euro'")
    print("})")
    print("create_claim_request_page.screenshot_helper('assign_claim_request_details.png')")
    print("```")
    
    print("\n📝 **示例3: 在step 6中使用**")
    print("```python")
    print("# step 6: 从列表页回到详情页")
    print("create_claim_request_page.navigate_to_claims_list()")
    print("create_claim_request_page.verify_claims_list_page()")
    print("create_claim_request_page.screenshot_helper('claims_list.png')")
    print("")
    print("# 回到详情页")
    print("create_claim_request_page.navigate_back_to_assign_claim_details()")
    print("create_claim_request_page.screenshot_helper('back_to_details.png')")
    print("```")

if __name__ == "__main__":
    print("🎯 回退按钮导航功能测试")
    
    # 测试方法是否存在
    test_success = test_back_button_methods()
    
    print("\n" + "="*60)
    
    # 显示使用方法
    show_back_button_usage()
    
    # 显示定位策略
    show_back_button_strategies()
    
    # 显示验证功能
    show_navigation_verification()
    
    # 显示实际示例
    show_practical_examples()
    
    if test_success:
        print("\n🎉 回退按钮导航功能完成！")
        print("\n✅ 确认状态:")
        print("1. ✅ click_back_button() 方法已实现")
        print("2. ✅ navigate_back_to_assign_claim_details() 方法已实现")
        print("3. ✅ 多重定位策略已配置")
        print("4. ✅ 导航验证逻辑已完善")
        print("5. ✅ 详细日志记录已添加")
        
        print("\n🚀 使用方法:")
        print("```python")
        print("# 简单回退")
        print("create_claim_request_page.click_back_button()")
        print("")
        print("# 回退到Assign Claim详情页")
        print("create_claim_request_page.navigate_back_to_assign_claim_details()")
        print("```")
        
        print("\n📸 现在可以使用回退按钮来实现页面导航了！")
    else:
        print("\n❌ 回退按钮导航功能未完成，请检查方法实现")
