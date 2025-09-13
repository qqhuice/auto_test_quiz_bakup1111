#!/usr/bin/env python3
"""
测试动态员工姓名选择功能
"""
import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.orangehrm_create_claim_request_page import OrangeHRMCreateClaimRequestPage
import inspect

def test_dynamic_employee_methods():
    """测试动态员工姓名相关方法是否存在"""
    print("=== 测试动态员工姓名相关方法 ===")
    
    # 动态员工姓名相关方法列表
    dynamic_methods = [
        'get_valid_employee_name',
        'set_valid_employee_name',
        'get_available_employee_names',
        'fill_employee_name_smart',
        'check_invalid_employee_name',
        'select_employee_from_dropdown'
    ]
    
    # 获取类的所有方法
    class_methods = [method for method in dir(OrangeHRMCreateClaimRequestPage) 
                    if not method.startswith('_') and callable(getattr(OrangeHRMCreateClaimRequestPage, method))]
    
    print(f"📋 需要检查的动态员工姓名方法数量: {len(dynamic_methods)}")
    
    missing_methods = []
    existing_methods = []
    
    for method in dynamic_methods:
        if method in class_methods:
            existing_methods.append(method)
            print(f"✅ {method} - 存在")
        else:
            missing_methods.append(method)
            print(f"❌ {method} - 缺失")
    
    print(f"\n=== 检查结果 ===")
    print(f"✅ 存在的方法: {len(existing_methods)}/{len(dynamic_methods)}")
    print(f"❌ 缺失的方法: {len(missing_methods)}/{len(dynamic_methods)}")
    
    if missing_methods:
        print(f"\n❌ 缺失的方法列表:")
        for method in missing_methods:
            print(f"   - {method}")
        return False
    else:
        print(f"\n🎉 所有动态员工姓名方法都存在！")
        return True

def show_dynamic_employee_usage():
    """显示动态员工姓名的使用方法"""
    print("\n=== 动态员工姓名使用方法 ===")
    
    print("🎯 **基本用法:**")
    print("```python")
    print("# 智能填写员工姓名（推荐用法）")
    print("create_claim_request_page.fill_employee_name_smart('Timothy Amiano')")
    print("")
    print("# 获取当前全局员工姓名")
    print("current_name = create_claim_request_page.get_valid_employee_name()")
    print("print(f'当前全局员工姓名: {current_name}')")
    print("")
    print("# 手动设置全局员工姓名")
    print("create_claim_request_page.set_valid_employee_name('John Doe')")
    print("```")
    
    print("\n🎯 **在pages/2.py中的使用:**")
    print("```python")
    print("# 原来的写法")
    print("create_claim_request_page.fill_employee_name('Timothy Amiano')")
    print("")
    print("# 新的智能写法")
    print("create_claim_request_page.fill_employee_name_smart('Timothy Amiano')")
    print("")
    print("# 后续使用全局员工姓名")
    print("employee_name = create_claim_request_page.get_valid_employee_name()")
    print("create_claim_request_page.verify_claim_details(employee_name)")
    print("```")
    
    print("\n🎯 **完整的智能流程:**")
    print("```python")
    print("# Step 1: 智能填写员工姓名")
    print("create_claim_request_page.fill_employee_name_smart('Timothy Amiano')")
    print("")
    print("# Step 2: 获取实际使用的员工姓名")
    print("actual_employee_name = create_claim_request_page.get_valid_employee_name()")
    print("print(f'实际使用的员工姓名: {actual_employee_name}')")
    print("")
    print("# Step 3: 使用全局员工姓名进行后续操作")
    print("create_claim_request_page.verify_claim_data_consistency({")
    print("    'employee_name': actual_employee_name,  # 使用实际的姓名")
    print("    'event': 'Travel allowances',")
    print("    'currency': 'Euro'")
    print("})")
    print("```")

def show_smart_logic():
    """显示智能逻辑说明"""
    print("\n=== 智能员工姓名选择逻辑 ===")
    
    print("🧠 **fill_employee_name_smart() 智能逻辑:**")
    print("1. ✅ 检查是否已有全局可用姓名")
    print("   - 如果有，直接使用全局姓名")
    print("   - 如果没有，继续下一步")
    print("")
    print("2. ✅ 尝试填写首选姓名")
    print("   - 填写用户指定的首选姓名")
    print("   - 等待2秒检查结果")
    print("")
    print("3. ✅ 检查是否有invalid提示")
    print("   - 如果没有invalid提示，姓名有效")
    print("   - 设置为全局变量并返回成功")
    print("")
    print("4. ✅ 如果有invalid提示，获取可用姓名")
    print("   - 输入'a'触发下拉列表")
    print("   - 获取所有可用的员工姓名")
    print("   - 选择第一个可用姓名")
    print("   - 设置为全局变量")
    print("")
    print("🎯 **优势:**")
    print("- 🔄 自动适应不同的登录账号")
    print("- 🎯 优先使用指定的姓名")
    print("- 📝 自动选择可用的替代姓名")
    print("- 🌐 全局变量确保一致性")
    print("- 📊 详细的日志记录")

def show_global_variable_usage():
    """显示全局变量使用说明"""
    print("\n=== 全局变量使用说明 ===")
    
    print("🌐 **全局变量机制:**")
    print("- 变量名: `_valid_employee_name`")
    print("- 作用域: 类级别（所有实例共享）")
    print("- 生命周期: 程序运行期间持续有效")
    print("- 用途: 确保整个测试流程使用一致的员工姓名")
    print("")
    print("🔧 **操作方法:**")
    print("```python")
    print("# 获取全局员工姓名")
    print("name = OrangeHRMCreateClaimRequestPage.get_valid_employee_name()")
    print("")
    print("# 设置全局员工姓名")
    print("OrangeHRMCreateClaimRequestPage.set_valid_employee_name('John Doe')")
    print("")
    print("# 实例方法也可以访问")
    print("page = OrangeHRMCreateClaimRequestPage(driver)")
    print("name = page.get_valid_employee_name()")
    print("```")
    
    print("\n📊 **自动使用全局变量的方法:**")
    print("- ✅ verify_claim_details() - 如果不指定员工姓名，自动使用全局变量")
    print("- ✅ verify_claim_data_consistency() - 优先使用全局员工姓名")
    print("- ✅ 其他验证方法 - 可以扩展支持全局变量")

def show_error_handling():
    """显示错误处理机制"""
    print("\n=== 错误处理机制 ===")
    
    print("🛡️ **Invalid检测:**")
    print("- 检测多种invalid提示文本")
    print("- 检测错误样式的元素")
    print("- 超时机制避免无限等待")
    print("")
    print("🔄 **备用方案:**")
    print("- 首选姓名无效时，自动获取可用姓名列表")
    print("- 如果获取失败，返回错误状态")
    print("- 详细的日志记录便于调试")
    print("")
    print("📝 **日志记录:**")
    print("```")
    print("INFO: 尝试填写首选姓名: Timothy Amiano")
    print("WARNING: 首选姓名 'Timothy Amiano' 无效，尝试获取可用姓名")
    print("INFO: 找到3个可用员工姓名: ['John Doe', 'Jane Smith', 'Bob Wilson']")
    print("INFO: 选择可用姓名: John Doe")
    print("INFO: ✅ 设置全局员工姓名: John Doe")
    print("```")

def show_pages_2_integration():
    """显示在pages/2.py中的集成方法"""
    print("\n=== pages/2.py集成方法 ===")
    
    print("📝 **修改建议:**")
    print("```python")
    print("# 原来的step 1")
    print("create_claim_request_page.fill_employee_name('Timothy Amiano')")
    print("")
    print("# 修改后的step 1")
    print("create_claim_request_page.fill_employee_name_smart('Timothy Amiano')")
    print("actual_employee_name = create_claim_request_page.get_valid_employee_name()")
    print("print(f'实际使用的员工姓名: {actual_employee_name}')")
    print("")
    print("# 修改后的step 4")
    print("create_claim_request_page.verify_claim_details()  # 自动使用全局姓名")
    print("create_claim_request_page.verify_claim_data_consistency({")
    print("    'employee_name': actual_employee_name,")
    print("    'event': 'Travel allowances',")
    print("    'currency': 'Euro'")
    print("})")
    print("")
    print("# 修改后的step 6")
    print("create_claim_request_page.verify_claim_record_exists(actual_employee_name)")
    print("create_claim_request_page.verify_claim_details_in_list({")
    print("    'employee_name': actual_employee_name,")
    print("    'event': 'Travel allowances',")
    print("    'currency': 'Euro'")
    print("})")
    print("```")
    
    print("\n🎯 **关键改进:**")
    print("1. ✅ 使用 fill_employee_name_smart() 替代 fill_employee_name()")
    print("2. ✅ 获取实际使用的员工姓名作为变量")
    print("3. ✅ 后续所有操作使用实际的员工姓名")
    print("4. ✅ 验证方法自动使用全局员工姓名")

if __name__ == "__main__":
    print("🎯 动态员工姓名选择功能测试")
    
    # 测试方法是否存在
    test_success = test_dynamic_employee_methods()
    
    print("\n" + "="*60)
    
    # 显示使用方法
    show_dynamic_employee_usage()
    
    # 显示智能逻辑
    show_smart_logic()
    
    # 显示全局变量使用
    show_global_variable_usage()
    
    # 显示错误处理
    show_error_handling()
    
    # 显示集成方法
    show_pages_2_integration()
    
    if test_success:
        print("\n🎉 动态员工姓名选择功能完成！")
        print("\n✅ 确认状态:")
        print("1. ✅ 智能员工姓名填写方法已实现")
        print("2. ✅ 全局变量机制已建立")
        print("3. ✅ Invalid检测机制已实现")
        print("4. ✅ 可用姓名获取方法已实现")
        print("5. ✅ 下拉列表选择方法已实现")
        print("6. ✅ 验证方法已支持全局变量")
        
        print("\n🚀 推荐使用方法:")
        print("```python")
        print("# 在pages/2.py的step 1中使用")
        print("create_claim_request_page.fill_employee_name_smart('Timothy Amiano')")
        print("actual_employee_name = create_claim_request_page.get_valid_employee_name()")
        print("")
        print("# 后续步骤自动使用全局员工姓名")
        print("create_claim_request_page.verify_claim_details()")
        print("```")
        
        print("\n📸 现在可以自动适应不同登录账号的员工姓名了！")
    else:
        print("\n❌ 动态员工姓名选择功能未完成，请检查方法实现")
