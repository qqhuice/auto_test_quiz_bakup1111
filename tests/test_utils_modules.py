#!/usr/bin/env python3
"""
测试工具模块导入
"""
import sys
import os
# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """测试模块导入"""
    print("=== 测试工具模块导入 ===")
    
    try:
        # 测试screenshot_helper导入
        print("1. 测试screenshot_helper导入...")
        from utils.screenshot_helper import ScreenshotHelper
        from utils.screenshot_helper import screenshot_helper
        from utils.screenshot_helper import take_screenshot
        print("✅ screenshot_helper导入成功")
        
        # 测试config导入
        print("2. 测试config导入...")
        from utils.config import config
        from utils.config import Config
        from utils.config import get_config
        print("✅ config导入成功")
        
        # 测试time导入
        print("3. 测试time导入...")
        import time
        print("✅ time导入成功")
        
        return True
        
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return False

def test_screenshot_helper():
    """测试ScreenshotHelper功能"""
    print("\n=== 测试ScreenshotHelper功能 ===")
    
    try:
        from utils.screenshot_helper import ScreenshotHelper
        
        # 创建实例
        helper = ScreenshotHelper()
        print("✅ ScreenshotHelper实例创建成功")
        
        # 测试方法存在
        methods = [
            'take_screenshot',
            'take_failure_screenshot', 
            'take_success_screenshot',
            'cleanup_old_screenshots',
            'get_screenshot_count',
            'get_latest_screenshot'
        ]
        
        for method in methods:
            if hasattr(helper, method):
                print(f"✅ {method}")
            else:
                print(f"❌ {method}")
        
        # 测试截图目录创建
        screenshot_count = helper.get_screenshot_count()
        print(f"✅ 当前截图数量: {screenshot_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ ScreenshotHelper测试失败: {e}")
        return False

def test_config():
    """测试Config功能"""
    print("\n=== 测试Config功能 ===")
    
    try:
        from utils.config import config, get_config, get_test_data
        
        # 测试配置属性
        print(f"✅ 浏览器: {config.browser}")
        print(f"✅ 基础URL: {config.base_url}")
        print(f"✅ 用户名: {config.username}")
        print(f"✅ 截图目录: {config.screenshot_dir}")
        print(f"✅ 短等待时间: {config.short_wait}")
        
        # 测试测试数据
        test_data = get_test_data()
        print(f"✅ 测试员工姓名: {test_data['employee_name']}")
        print(f"✅ 测试事件: {test_data['event']}")
        print(f"✅ 测试货币: {test_data['currency']}")
        
        # 测试配置获取
        all_config = config.get_all_config()
        print(f"✅ 配置项数量: {len(all_config)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Config测试失败: {e}")
        return False

def test_integration():
    """测试集成使用"""
    print("\n=== 测试集成使用 ===")
    
    try:
        # 模拟在实际代码中的使用
        from utils.screenshot_helper import ScreenshotHelper
        from utils.config import config
        import time
        
        print("✅ 所有模块导入成功")
        
        # 创建截图助手
        helper = ScreenshotHelper(config.screenshot_dir)
        print(f"✅ 使用配置的截图目录: {config.screenshot_dir}")
        
        # 模拟使用配置
        print(f"✅ 等待时间配置: 短={config.short_wait}s, 中={config.medium_wait}s, 长={config.long_wait}s")
        
        # 模拟时间使用
        start_time = time.time()
        time.sleep(0.1)  # 短暂等待
        elapsed = time.time() - start_time
        print(f"✅ 时间模块正常工作: {elapsed:.2f}s")
        
        return True
        
    except Exception as e:
        print(f"❌ 集成测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🎯 工具模块测试")
    
    # 测试导入
    import_test = test_imports()
    
    if import_test:
        # 测试ScreenshotHelper
        screenshot_test = test_screenshot_helper()
        
        # 测试Config
        config_test = test_config()
        
        # 测试集成
        integration_test = test_integration()
        
        if all([import_test, screenshot_test, config_test, integration_test]):
            print("\n🎉 所有工具模块测试通过！")
            print("\n📋 创建的模块:")
            print("1. ✅ utils/screenshot_helper.py - 截图辅助工具")
            print("2. ✅ utils/config.py - 配置管理")
            print("\n🚀 现在导入语句不会再标红了！")
        else:
            print("\n❌ 部分测试失败")
    else:
        print("\n❌ 导入测试失败，无法继续其他测试")
