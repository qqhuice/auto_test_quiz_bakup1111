#!/usr/bin/env python3
"""
测试修改后的报告生成，验证7个步骤显示
"""
import sys
import os
import time

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pages.orangehrm_create_claim_request_page import OrangeHRMCreateClaimRequestPage
from selenium import webdriver
from utils.driver_manager import DriverManager

def test_report_generation():
    """测试报告生成功能"""
    print("=== 测试修改后的报告生成功能 ===")
    
    driver = None
    try:
        # 1. 启动浏览器（仅用于创建页面对象）
        print("步骤1: 启动Chrome浏览器...")
        driver_manager = DriverManager()
        driver = driver_manager.create_chrome_driver()
        print("✅ 浏览器启动成功")
        
        # 2. 创建页面对象
        print("步骤2: 创建Create Claim Request页面对象...")
        create_claim_page = OrangeHRMCreateClaimRequestPage(driver)
        print("✅ 页面对象创建成功")
        
        # 3. 模拟设置有效员工姓名
        print("步骤3: 设置测试数据...")
        create_claim_page._valid_employee_name = "Timothy Amiano"
        print("✅ 测试数据设置完成")
        
        # 4. 生成HTML报告
        print("步骤4: 生成HTML测试报告...")
        result = create_claim_page.generate_html_report()
        
        if result:
            print("✅ HTML报告生成成功")
            
            # 5. 检查报告文件
            if hasattr(create_claim_page, '_report_file'):
                report_file = create_claim_page._report_file
                print(f"📄 报告文件位置: {report_file}")
                
                # 检查文件是否存在
                if os.path.exists(report_file):
                    file_size = os.path.getsize(report_file)
                    print(f"📊 报告文件大小: {file_size / 1024:.1f} KB")
                    
                    # 读取报告内容并验证7个步骤
                    print("步骤5: 验证报告内容...")
                    with open(report_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 检查是否包含7个步骤
                    step_count = 0
                    expected_steps = [
                        "Step 1: 点击Employee Claims，添加一条Assign Claims记录",
                        "Step 2: 点击Create后验证成功提示信息", 
                        "Step 3: 跳转至Assign Claim详情页，验证与前一步数据一致",
                        "Step 4: 添加Expenses，选择Expense Type和Date，填写amount，点击Submit，验证成功提示信息",
                        "Step 5: 检查数据与填写数据一致，点击Back返回",
                        "Step 6: 验证Record中存在刚才的提交记录",
                        "Step 7: 测试完成，生成详细报告"
                    ]
                    
                    for i, expected_step in enumerate(expected_steps, 1):
                        if expected_step in content:
                            step_count += 1
                            print(f"✅ 找到步骤{i}: {expected_step}")
                        else:
                            print(f"❌ 未找到步骤{i}: {expected_step}")
                    
                    # 检查总结部分
                    if "全部7个步骤均执行成功" in content:
                        print("✅ 找到正确的步骤总数描述")
                    else:
                        print("❌ 未找到正确的步骤总数描述")
                    
                    # 检查截图数量描述
                    if "7张，每步骤对应一张截图" in content:
                        print("✅ 找到正确的截图数量描述")
                    else:
                        print("❌ 未找到正确的截图数量描述")
                    
                    print(f"\n📊 验证结果:")
                    print(f"• 期望步骤数: 7")
                    print(f"• 实际找到步骤数: {step_count}")
                    print(f"• 验证结果: {'✅ 通过' if step_count == 7 else '❌ 失败'}")
                    
                    if step_count == 7:
                        print("\n🎉 报告步骤修改成功！现在显示正确的7个步骤")
                        return True
                    else:
                        print("\n❌ 报告步骤修改失败，请检查代码")
                        return False
                        
                else:
                    print("❌ 报告文件不存在")
                    return False
            else:
                print("❌ 未获取到报告文件路径")
                return False
        else:
            print("❌ HTML报告生成失败")
            return False
        
    except Exception as e:
        print(f"❌ 测试过程中发生错误: {e}")
        return False
        
    finally:
        # 关闭浏览器
        if driver:
            try:
                driver.quit()
                print("✅ 浏览器已关闭")
            except Exception as e:
                print(f"⚠️ 关闭浏览器时出错: {e}")

if __name__ == "__main__":
    """程序入口点"""
    try:
        success = test_report_generation()
        if success:
            print("\n🎉 报告步骤修改验证成功！")
            print("📋 现在报告将显示正确的7个步骤：")
            print("1. 点击Employee Claims，添加一条Assign Claims记录")
            print("2. 点击Create后验证成功提示信息")
            print("3. 跳转至Assign Claim详情页，验证与前一步数据一致")
            print("4. 添加Expenses，选择Expense Type和Date，填写amount，点击Submit，验证成功提示信息")
            print("5. 检查数据与填写数据一致，点击Back返回")
            print("6. 验证Record中存在刚才的提交记录")
            print("7. 测试完成，生成详细报告")
            sys.exit(0)
        else:
            print("\n❌ 报告步骤修改验证失败！")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断了测试")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试执行过程中发生未预期的错误: {e}")
        sys.exit(1)
