#!/usr/bin/env python3
"""
测试截图显示修复
验证HTML报告中的截图路径和位置提示是否正确
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_screenshot_path_fix():
    """测试截图路径修复"""
    print("🔧 测试截图路径修复...")
    
    try:
        from run_chrome_tests import ChromeTestRunner
        
        # 创建测试运行器实例
        runner = ChromeTestRunner()
        
        # 生成详细测试报告
        html_file, md_file = runner.generate_detailed_test_report(success=True)
        
        print(f"✅ HTML报告已生成: {html_file}")
        
        # 检查HTML内容
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查修复的内容
        fixes_to_check = [
            ('file:///', '绝对路径file协议'),
            ('完整路径:', '完整路径标签'),
            ('如图片无法显示，请直接打开上述路径查看', '查看提示'),
            ('截图目录:', '截图目录标签'),
            ('预期路径:', '预期路径标签'),
            ('💡 截图查看说明:', '查看说明'),
            ('python run_chrome_tests.py', '运行命令'),
            ('请直接打开文件夹查看', '文件夹查看提示'),
        ]
        
        print("\n检查修复内容:")
        missing_fixes = []
        for check, description in fixes_to_check:
            if check in content:
                print(f"✅ {description}")
            else:
                missing_fixes.append(description)
                print(f"❌ {description}")
        
        # 检查是否包含实际的截图路径
        screenshot_paths_found = 0
        if 'F:\\github\\auto_test_quiz' in content:
            screenshot_paths_found += 1
            print("✅ 找到绝对路径")
        
        if 'screenshots\\chrome_' in content or 'screenshots/chrome_' in content:
            screenshot_paths_found += 1
            print("✅ 找到截图目录路径")
        
        if missing_fixes:
            print(f"\n❌ 缺失的修复内容: {missing_fixes}")
            return False
        else:
            print("\n✅ 所有修复内容都已添加")
            return True
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_screenshot_locations():
    """显示截图位置信息"""
    print("\n📁 截图位置信息:")
    
    screenshots_dir = Path("../screenshots")
    if screenshots_dir.exists():
        print(f"📂 截图根目录: {screenshots_dir.resolve()}")
        
        # 列出所有截图目录
        chrome_dirs = list(screenshots_dir.glob("chrome_*"))
        print(f"📊 找到 {len(chrome_dirs)} 个Chrome截图目录:")
        
        for i, chrome_dir in enumerate(chrome_dirs, 1):
            if chrome_dir.is_dir():
                screenshot_files = list(chrome_dir.glob("*.png")) + list(chrome_dir.glob("*.jpg")) + list(chrome_dir.glob("*.jpeg"))
                print(f"  {i}. {chrome_dir.name} ({len(screenshot_files)} 个截图文件)")
                
                # 显示前3个截图文件作为示例
                for j, screenshot_file in enumerate(screenshot_files[:3]):
                    print(f"     📷 {screenshot_file.name}")
                if len(screenshot_files) > 3:
                    print(f"     ... 还有 {len(screenshot_files) - 3} 个文件")
    else:
        print("❌ screenshots目录不存在")

def show_html_report_info():
    """显示HTML报告信息"""
    print("\n📄 HTML报告信息:")
    
    reports_dir = Path("../reports")
    if reports_dir.exists():
        html_files = list(reports_dir.glob("Chrome_Detailed_Test_Report_*.html"))
        print(f"📊 找到 {len(html_files)} 个详细HTML报告:")
        
        for i, html_file in enumerate(html_files, 1):
            file_size = html_file.stat().st_size / 1024
            print(f"  {i}. {html_file.name} ({file_size:.1f} KB)")
            print(f"     📁 完整路径: {html_file.resolve()}")
            
            # 检查最新的报告
            if i == len(html_files):
                print(f"     🌟 最新报告，建议在浏览器中打开查看")
    else:
        print("❌ reports目录不存在")

def show_browser_instructions():
    """显示浏览器查看说明"""
    print("\n🌐 浏览器查看说明:")
    print("1. 📂 **直接打开HTML文件**:")
    print("   - 右键点击HTML文件 → 选择浏览器打开")
    print("   - 或者拖拽HTML文件到浏览器窗口")
    
    print("\n2. 📸 **如果截图无法显示**:")
    print("   - 报告中已显示完整的截图文件路径")
    print("   - 可以直接复制路径到文件管理器中查看")
    print("   - 或者点击报告中的路径链接（如果浏览器支持）")
    
    print("\n3. 🔧 **截图显示问题的原因**:")
    print("   - 浏览器安全策略限制本地文件访问")
    print("   - 相对路径在HTML文件中无法正确解析")
    print("   - 现在报告中提供了完整的绝对路径")
    
    print("\n4. 💡 **最佳实践**:")
    print("   - 使用本地HTTP服务器查看报告（如Python的http.server）")
    print("   - 或者将截图文件复制到reports目录下")
    print("   - 现在报告提供了详细的位置提示，方便手动查看")

def main():
    """主函数"""
    print("🔧 截图显示修复验证工具")
    print("="*60)
    
    # 1. 测试截图路径修复
    success = test_screenshot_path_fix()
    
    # 2. 显示截图位置信息
    show_screenshot_locations()
    
    # 3. 显示HTML报告信息
    show_html_report_info()
    
    # 4. 显示浏览器查看说明
    show_browser_instructions()
    
    print("\n" + "="*60)
    if success:
        print("🎉 截图路径修复验证完成！")
        
        print("\n✅ 修复总结:")
        print("1. ✅ 添加了绝对路径file://协议支持")
        print("2. ✅ 提供了完整的截图文件路径")
        print("3. ✅ 添加了详细的位置提示和查看说明")
        print("4. ✅ 包含了截图目录和预期路径信息")
        print("5. ✅ 提供了手动查看截图的指导")
        
        print("\n🚀 现在HTML报告包含了完整的截图位置信息！")
        print("💡 即使图片无法在浏览器中显示，也可以根据路径手动查看截图文件！")
        
    else:
        print("❌ 修复验证失败，请检查错误信息")

if __name__ == "__main__":
    main()
