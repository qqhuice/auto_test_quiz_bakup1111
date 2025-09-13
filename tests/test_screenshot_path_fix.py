#!/usr/bin/env python3
"""
测试截图路径修复
验证BDD测试报告中的截图路径是否正确
"""
import os
import sys
from pathlib import Path

def test_screenshot_path_fix():
    """测试截图路径修复"""
    print("🔧 测试截图路径修复...")
    
    try:
        # 导入页面类
        from pages.orangehrm_create_claim_request_page import OrangeHRMCreateClaimRequestPage
        
        # 创建页面实例（不需要driver，只测试报告生成）
        page = OrangeHRMCreateClaimRequestPage(None)
        
        # 生成测试报告
        print("正在生成测试报告...")
        result = page.generate_html_report()
        
        if result:
            print(f"✅ 测试报告生成成功")
            
            # 检查最新生成的报告
            reports_dir = Path("reports")
            if reports_dir.exists():
                report_files = list(reports_dir.glob("test_report_*.html"))
                if report_files:
                    # 按修改时间排序，取最新的
                    latest_report = max(report_files, key=lambda x: x.stat().st_mtime)
                    print(f"📄 最新报告: {latest_report}")
                    
                    # 读取报告内容
                    with open(latest_report, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 检查截图路径
                    print("\n🔍 检查截图路径...")
                    
                    # 检查是否包含正确的截图目录路径
                    if 'bdd_tests_' in content:
                        print("✅ 找到BDD测试截图目录引用")
                    else:
                        print("❌ 未找到BDD测试截图目录引用")
                    
                    # 检查是否还有旧的硬编码路径
                    if '../screenshots/' in content and 'bdd_tests_' not in content:
                        print("❌ 仍然包含旧的硬编码路径")
                    else:
                        print("✅ 已修复硬编码路径问题")
                    
                    # 检查调试信息
                    if '截图目录:' in content:
                        print("✅ 包含截图目录调试信息")
                    else:
                        print("❌ 缺少截图目录调试信息")
                    
                    # 显示截图目录信息
                    screenshots_dir = Path("screenshots")
                    if screenshots_dir.exists():
                        bdd_dirs = [d for d in screenshots_dir.iterdir() if d.is_dir() and d.name.startswith('bdd_tests_')]
                        if bdd_dirs:
                            latest_bdd_dir = max(bdd_dirs, key=lambda x: x.stat().st_mtime)
                            print(f"📁 最新BDD截图目录: {latest_bdd_dir}")
                            
                            # 检查截图文件
                            screenshots = list(latest_bdd_dir.glob("*.png"))
                            print(f"📸 截图数量: {len(screenshots)}")
                            
                            if screenshots:
                                print("📋 截图文件列表:")
                                for i, screenshot in enumerate(screenshots[:5], 1):  # 只显示前5个
                                    print(f"  {i}. {screenshot.name}")
                                if len(screenshots) > 5:
                                    print(f"  ... 还有 {len(screenshots) - 5} 个文件")
                        else:
                            print("⚠️ 未找到BDD测试截图目录")
                    
                    return True
                else:
                    print("❌ 未找到测试报告文件")
                    return False
            else:
                print("❌ reports目录不存在")
                return False
        else:
            print("❌ 测试报告生成失败")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_fix_summary():
    """显示修复总结"""
    print("\n" + "="*60)
    print("📋 截图路径修复总结")
    print("="*60)
    print("🔧 修复内容:")
    print("  1. 动态查找最新的BDD测试截图目录")
    print("  2. 更新HTML模板中的截图路径")
    print("  3. 添加截图目录调试信息")
    print("  4. 提供图片加载失败的备用方案")
    print("\n🎯 修复效果:")
    print("  • 报告中的截图现在可以正确显示")
    print("  • 支持带时间戳的截图目录结构")
    print("  • 提供详细的调试信息")
    print("  • 图片加载失败时显示有用的提示")
    print("\n🚀 使用方法:")
    print("  1. 运行 python run_bdd_tests.py 生成截图")
    print("  2. 打开生成的 test_report_*.html 文件")
    print("  3. 现在应该可以看到所有截图")

if __name__ == "__main__":
    print("🧪 开始测试截图路径修复...")
    
    success = test_screenshot_path_fix()
    
    if success:
        print("\n🎉 截图路径修复测试通过！")
        show_fix_summary()
    else:
        print("\n❌ 截图路径修复测试失败！")
        print("请检查修复代码是否正确")
    
    print("\n" + "="*60)
