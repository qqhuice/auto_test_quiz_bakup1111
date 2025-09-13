#!/usr/bin/env python3
"""
测试截图集成功能
验证HTML报告中是否正确显示截图信息和截图文件
"""
import sys
import os
import tempfile
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_screenshot_methods():
    """测试截图相关方法"""
    print("=== 测试截图相关方法 ===")
    
    try:
        from run_chrome_tests import ChromeTestRunner
        
        # 创建测试实例
        runner = ChromeTestRunner()
        
        # 检查新增的截图方法
        methods_to_check = [
            ('_get_test_case_screenshots', '获取测试用例截图方法'),
            ('_get_expected_screenshot_names', '获取预期截图名称方法'),
        ]
        
        missing_methods = []
        for method_name, description in methods_to_check:
            if hasattr(runner, method_name):
                print(f"✅ {description}")
            else:
                missing_methods.append(description)
                print(f"❌ {description}")
        
        if missing_methods:
            print(f"❌ 缺失的方法: {missing_methods}")
            return False
        else:
            print("✅ 所有截图相关方法都存在")
            return True
            
    except Exception as e:
        print(f"❌ 方法检查失败: {e}")
        return False

def test_screenshot_patterns():
    """测试截图模式定义"""
    print("\n=== 测试截图模式定义 ===")
    
    try:
        from run_chrome_tests import ChromeTestRunner
        
        runner = ChromeTestRunner()
        
        # 测试每个测试用例的截图模式
        test_cases = ["TC001", "TC002", "TC003", "TC004", "TC005", "TC006", "TC007", "TC008"]
        
        all_patterns_valid = True
        for test_case_id in test_cases:
            expected_names = runner._get_expected_screenshot_names(test_case_id)
            if expected_names:
                print(f"✅ {test_case_id}: {len(expected_names)}个预期截图")
                for name in expected_names:
                    print(f"    📷 {name}")
            else:
                print(f"❌ {test_case_id}: 没有定义预期截图")
                all_patterns_valid = False
        
        if all_patterns_valid:
            print("✅ 所有测试用例都有预期截图定义")
            return True
        else:
            print("❌ 部分测试用例缺少截图定义")
            return False
            
    except Exception as e:
        print(f"❌ 截图模式测试失败: {e}")
        return False

def test_screenshot_html_generation():
    """测试带截图的HTML报告生成"""
    print("\n=== 测试带截图的HTML报告生成 ===")
    
    try:
        from run_chrome_tests import ChromeTestRunner
        
        # 创建临时目录用于测试
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # 创建测试实例
            runner = ChromeTestRunner()
            runner.reports_dir = temp_path / "reports"
            runner.screenshots_dir = temp_path / "screenshots"
            runner.reports_dir.mkdir(parents=True, exist_ok=True)
            runner.screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建模拟的截图文件
            screenshot_dir = runner.screenshots_dir / "chrome_test_20250912"
            screenshot_dir.mkdir()
            
            # 创建一些模拟截图文件（故意不创建所有文件来测试"不存在"的情况）
            test_screenshots = [
                "异常测试_用例1_步骤1_滚动到标题.png",
                "异常测试_用例1_步骤2_Add按钮高亮.png",
                "网站访问_初始页面.png",
                # 故意不创建TC007的第4个截图，用来测试"不存在"的情况
            ]

            for screenshot_name in test_screenshots:
                screenshot_file = screenshot_dir / screenshot_name
                screenshot_file.write_text("fake image content")
            
            # 生成HTML报告
            html_file, md_file = runner.generate_detailed_test_report(success=True)
            
            # 验证HTML报告内容
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # 检查截图相关的HTML内容
            screenshot_checks = [
                ('screenshots-section', '截图部分CSS类'),
                ('screenshot-grid', '截图网格CSS类'),
                ('screenshot-item', '截图项CSS类'),
                ('screenshot-placeholder', '截图占位符CSS类'),
                ('📸 测试截图', '截图标题'),
                ('screenshot-info-only', '截图信息CSS类'),
                ('截图文件不存在', '截图不存在提示'),
                ('onerror=', '图片加载错误处理'),
            ]
            
            print("检查HTML报告中的截图功能:")
            missing_features = []
            for check, description in screenshot_checks:
                if check in html_content:
                    print(f"✅ {description}")
                else:
                    missing_features.append(description)
                    print(f"❌ {description}")
            
            # 检查是否包含实际的截图路径
            screenshot_path_found = False
            for screenshot_name in test_screenshots:
                if screenshot_name in html_content:
                    print(f"✅ 找到截图路径: {screenshot_name}")
                    screenshot_path_found = True
                    break
            
            if not screenshot_path_found:
                print("❌ 未找到任何截图路径")
                missing_features.append("截图路径")
            
            if missing_features:
                print(f"❌ 缺失的截图功能: {missing_features}")
                return False
            else:
                print("✅ 所有截图功能都正常")
                return True
                
    except Exception as e:
        print(f"❌ HTML截图生成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_screenshot_file_detection():
    """测试截图文件检测功能"""
    print("\n=== 测试截图文件检测功能 ===")
    
    try:
        from run_chrome_tests import ChromeTestRunner
        
        # 创建临时目录用于测试
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # 创建测试实例
            runner = ChromeTestRunner()
            runner.screenshots_dir = temp_path / "screenshots"
            runner.screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            # 创建模拟的截图目录和文件
            screenshot_dir = runner.screenshots_dir / "chrome_test_20250912"
            screenshot_dir.mkdir()
            
            # 创建TC007的截图文件
            tc007_screenshots = [
                "异常测试_用例1_步骤1_滚动到标题.png",
                "异常测试_用例1_步骤2_Add按钮高亮.png",
                "异常测试_用例1_步骤3_点击Add按钮.png"
            ]
            
            for screenshot_name in tc007_screenshots:
                screenshot_file = screenshot_dir / screenshot_name
                screenshot_file.write_text("fake image content")
            
            # 测试截图检测
            screenshots = runner._get_test_case_screenshots("TC007")
            
            print(f"TC007检测到的截图数量: {len(screenshots)}")
            for screenshot in screenshots:
                status = "存在" if screenshot['exists'] else "不存在"
                print(f"  📷 {screenshot['title']} - {status}")
                print(f"     路径: {screenshot['path']}")
            
            # 测试不存在截图的用例
            screenshots_tc001 = runner._get_test_case_screenshots("TC001")
            print(f"\nTC001检测到的截图数量: {len(screenshots_tc001)}")
            
            if len(screenshots) > 0:
                print("✅ 截图文件检测功能正常")
                return True
            else:
                print("❌ 截图文件检测功能异常")
                return False
                
    except Exception as e:
        print(f"❌ 截图文件检测测试失败: {e}")
        return False

def show_screenshot_features():
    """显示截图功能特性"""
    print("\n=== 截图功能特性 ===")
    
    print("🎯 **新增的截图功能**:")
    print("1. ✅ **自动截图检测**")
    print("   - 自动搜索screenshots/目录下的截图文件")
    print("   - 支持PNG、JPG、JPEG格式")
    print("   - 智能匹配测试用例和截图文件名")
    
    print("\n2. ✅ **截图显示功能**")
    print("   - 在HTML报告中直接显示截图")
    print("   - 网格布局，美观展示")
    print("   - 图片加载失败时显示占位符")
    print("   - 显示截图文件路径和状态")
    
    print("\n3. ✅ **截图信息提示**")
    print("   - 当截图文件不存在时，显示预期截图列表")
    print("   - 提供截图文件的预期命名规范")
    print("   - 显示截图生成状态（已生成/待生成）")
    
    print("\n4. ✅ **每个测试用例的截图规划**")
    print("   - TC001: 3张截图 (网站访问流程)")
    print("   - TC002: 3张截图 (登录页面导航)")
    print("   - TC003: 4张截图 (正确凭据登录)")
    print("   - TC004: 4张截图 (错误用户名登录)")
    print("   - TC005: 4张截图 (错误密码登录)")
    print("   - TC006: 3张截图 (异常页面导航)")
    print("   - TC007: 4张截图 (NoSuchElementException)")
    print("   - TC008: 4张截图 (ElementNotInteractableException)")
    
    print("\n5. ✅ **响应式截图布局**")
    print("   - 自适应网格布局")
    print("   - 截图缩略图显示")
    print("   - 点击查看大图功能")
    print("   - 移动设备友好")

def show_usage_instructions():
    """显示使用说明"""
    print("\n=== 使用说明 ===")
    
    print("🚀 **如何在报告中显示截图**:")
    print("1. 运行测试: `python run_chrome_tests.py`")
    print("2. 截图会自动保存到 `screenshots/chrome_*` 目录")
    print("3. 生成的HTML报告会自动检测并显示截图")
    
    print("\n📁 **截图文件命名规范**:")
    print("   - 网站访问: 网站访问_*.png")
    print("   - 登录测试: *登录_*.png")
    print("   - 异常测试: 异常测试_用例*_步骤*_*.png")
    
    print("\n📊 **报告中的截图显示**:")
    print("   - 存在的截图: 直接显示图片")
    print("   - 不存在的截图: 显示占位符和文件路径")
    print("   - 预期截图: 显示待生成的截图列表")
    
    print("\n💡 **截图优化建议**:")
    print("   - 确保截图文件名包含测试用例关键词")
    print("   - 使用PNG格式获得最佳质量")
    print("   - 截图尺寸建议: 1920x1080或1366x768")

if __name__ == "__main__":
    print("🔧 截图集成功能验证工具")
    print("="*60)
    
    # 执行所有测试
    tests = [
        test_screenshot_methods,
        test_screenshot_patterns,
        test_screenshot_file_detection,
        test_screenshot_html_generation,
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
    
    if all_passed:
        print("\n🎉 所有截图功能测试都通过！")
        
        # 显示截图功能特性
        show_screenshot_features()
        
        # 显示使用说明
        show_usage_instructions()
        
        print("\n" + "="*60)
        print("🎉 截图集成功能验证完成！")
        
        print("\n✅ 验证总结:")
        print("1. ✅ 截图检测方法已正确实现")
        print("2. ✅ 8个测试用例都有截图规划")
        print("3. ✅ HTML报告支持截图显示")
        print("4. ✅ 截图文件自动检测功能")
        print("5. ✅ 截图信息和路径显示")
        
        print("\n🚀 现在HTML报告将显示每个测试用例的截图！")
        
    else:
        print("\n❌ 发现问题，需要进一步修复")
        print("💡 请检查上述测试结果并修复相应问题")
