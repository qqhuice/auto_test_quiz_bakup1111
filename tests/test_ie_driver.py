#!/usr/bin/env python3
"""
Internet Explorer驱动测试脚本
验证IE驱动是否正常工作
"""
import sys
from pathlib import Path
from loguru import logger
from utils.driver_manager import DriverManager


def test_ie_driver():
    """测试IE驱动是否正常工作"""
    logger.info("=== 测试Internet Explorer驱动 ===")
    
    driver_manager = DriverManager()
    driver = None
    
    try:
        # 创建IE驱动
        logger.info("正在创建IE驱动...")
        driver = driver_manager.create_ie_driver()
        logger.info("✅ IE驱动创建成功")
        
        # 测试基本功能
        logger.info("测试基本功能...")
        driver.get("https://www.baidu.com")
        logger.info(f"页面标题: {driver.title}")
        logger.info("✅ 页面访问成功")
        
        # 获取浏览器信息
        logger.info(f"浏览器名称: {driver.name}")
        logger.info(f"当前URL: {driver.current_url}")
        
        logger.info("✅ IE驱动测试成功")
        return True
        
    except Exception as e:
        logger.error(f"❌ IE驱动测试失败: {e}")
        logger.error("可能的原因:")
        logger.error("1. 未安装Internet Explorer")
        logger.error("2. 未下载IEDriverServer.exe")
        logger.error("3. IEDriverServer.exe未添加到PATH")
        logger.error("4. IE浏览器安全设置不正确")
        logger.error("5. 保护模式设置不统一")
        return False
        
    finally:
        if driver:
            try:
                driver.quit()
                logger.info("IE驱动已关闭")
            except:
                pass


def main():
    """主函数"""
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                Internet Explorer驱动测试                     ║")
    print("║                                                              ║")
    print("║  测试目的:                                                   ║")
    print("║  1. 验证IE驱动是否正确安装                                   ║")
    print("║  2. 验证IE浏览器是否可以正常启动                             ║")
    print("║  3. 验证基本的页面访问功能                                   ║")
    print("║                                                              ║")
    print("║  如果测试失败，请检查:                                       ║")
    print("║  - Internet Explorer是否已安装                               ║")
    print("║  - IEDriverServer.exe是否已下载并添加到PATH                  ║")
    print("║  - IE浏览器的安全设置是否正确配置                            ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()
    
    success = test_ie_driver()
    
    if success:
        print("\n🎉 IE驱动测试成功！可以运行完整的IE测试流程。")
        print("运行命令: python run_ie_tests.py")
    else:
        print("\n❌ IE驱动测试失败！请检查IE浏览器和驱动配置。")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
