#!/usr/bin/env python3
"""
测试代码导航功能
用于验证VSCode的Python代码跳转是否正常工作
"""
import sys
import os

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入项目模块
from pages.orangehrm_create_claim_request_page import OrangeHRMCreateClaimRequestPage
from pages.base_page import BasePage
from utils.driver_manager import DriverManager

def test_code_navigation():
    """测试代码导航功能"""
    print("=== 测试代码导航功能 ===")
    
    # 创建页面对象实例
    # 尝试Ctrl+点击下面的类名和方法名
    driver_manager = DriverManager()
    
    # 这里应该能够跳转到OrangeHRMCreateClaimRequestPage类定义
    create_claim_page = OrangeHRMCreateClaimRequestPage(None)
    
    # 这里应该能够跳转到click_latest_record_view_details_and_verify方法定义
    # create_claim_page.click_latest_record_view_details_and_verify()
    
    # 这里应该能够跳转到scroll_to_Records_Found方法定义  
    # create_claim_page.scroll_to_Records_Found()
    
    print("✅ 如果您能看到这个输出，说明Python导入正常")
    print("✅ 现在尝试Ctrl+点击上面的类名和方法名")
    print("✅ 或者右键选择'Go to Definition'")

if __name__ == "__main__":
    test_code_navigation()
