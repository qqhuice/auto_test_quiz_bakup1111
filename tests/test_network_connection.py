#!/usr/bin/env python3
"""
网络连接测试脚本
用于诊断和解决OrangeHRM网站访问问题
"""
import sys
import os
import time
import requests
from urllib.parse import urlparse

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.driver_manager import DriverManager

def test_network_connectivity():
    """测试网络连接性"""
    print("=== 网络连接测试 ===")
    
    target_url = "https://opensource-demo.orangehrmlive.com"
    
    print(f"🔧 测试目标: {target_url}")
    
    # 1. 基本网络连接测试
    print("\n1. 基本网络连接测试...")
    try:
        response = requests.get(target_url, timeout=30)
        print(f"✅ HTTP状态码: {response.status_code}")
        print(f"✅ 响应时间: {response.elapsed.total_seconds():.2f}秒")
        if response.status_code == 200:
            print("✅ 网站可正常访问")
        else:
            print(f"⚠️ 网站返回状态码: {response.status_code}")
    except requests.exceptions.Timeout:
        print("❌ 连接超时 - 网络可能较慢")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误 - 请检查网络连接")
        return False
    except Exception as e:
        print(f"❌ 网络测试失败: {e}")
        return False
    
    # 2. DNS解析测试
    print("\n2. DNS解析测试...")
    try:
        import socket
        hostname = urlparse(target_url).hostname
        ip_address = socket.gethostbyname(hostname)
        print(f"✅ DNS解析成功: {hostname} -> {ip_address}")
    except Exception as e:
        print(f"❌ DNS解析失败: {e}")
        return False
    
    # 3. 登录页面特定测试
    print("\n3. 登录页面访问测试...")
    login_url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    try:
        response = requests.get(login_url, timeout=30)
        print(f"✅ 登录页面状态码: {response.status_code}")
        print(f"✅ 登录页面响应时间: {response.elapsed.total_seconds():.2f}秒")
        
        # 检查页面内容
        if "OrangeHRM" in response.text:
            print("✅ 登录页面内容正常")
        else:
            print("⚠️ 登录页面内容异常")
            
    except Exception as e:
        print(f"❌ 登录页面访问失败: {e}")
        return False
    
    return True

def test_browser_access():
    """测试浏览器访问"""
    print("\n=== 浏览器访问测试 ===")
    
    driver = None
    try:
        print("1. 创建浏览器驱动...")
        driver_manager = DriverManager()
        driver = driver_manager.create_chrome_driver()
        print("✅ 浏览器驱动创建成功")
        
        print("2. 设置超时时间...")
        driver.set_page_load_timeout(60)  # 60秒超时
        print("✅ 超时时间设置完成")
        
        print("3. 访问OrangeHRM登录页面...")
        start_time = time.time()
        driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        load_time = time.time() - start_time
        print(f"✅ 页面加载成功，耗时: {load_time:.2f}秒")
        
        print("4. 验证页面标题...")
        title = driver.title
        print(f"✅ 页面标题: {title}")
        
        if "OrangeHRM" in title:
            print("✅ 页面标题验证成功")
        else:
            print("⚠️ 页面标题异常")
        
        print("5. 检查页面元素...")
        time.sleep(3)  # 等待页面完全加载
        
        # 检查登录表单
        try:
            username_field = driver.find_element("name", "username")
            password_field = driver.find_element("name", "password")
            login_button = driver.find_element("xpath", "//button[@type='submit']")
            print("✅ 登录表单元素检查成功")
        except Exception as e:
            print(f"⚠️ 登录表单元素检查失败: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ 浏览器访问测试失败: {e}")
        return False
    finally:
        if driver:
            try:
                driver.quit()
                print("✅ 浏览器已关闭")
            except:
                pass

def test_with_retry():
    """带重试机制的测试"""
    print("\n=== 重试机制测试 ===")
    
    max_retries = 3
    for attempt in range(max_retries):
        print(f"\n第{attempt + 1}次尝试...")
        
        driver = None
        try:
            # 创建驱动
            driver_manager = DriverManager()
            driver = driver_manager.create_chrome_driver()
            
            # 设置超时
            driver.set_page_load_timeout(60)
            
            # 访问页面
            print("正在访问OrangeHRM...")
            driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
            
            # 验证成功
            print("✅ 访问成功！")
            time.sleep(2)
            return True
            
        except Exception as e:
            print(f"❌ 第{attempt + 1}次尝试失败: {e}")
            
            if driver:
                try:
                    driver.quit()
                except:
                    pass
            
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 5  # 递增等待时间
                print(f"等待{wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                print("❌ 所有重试都失败")
                return False
        finally:
            if driver:
                try:
                    driver.quit()
                except:
                    pass
    
    return False

def show_network_troubleshooting():
    """显示网络故障排除建议"""
    print("\n=== 网络故障排除建议 ===")
    
    print("🔧 **常见问题和解决方案**:")
    print("1. ✅ **网络连接慢**")
    print("   - 增加页面加载超时时间到60秒")
    print("   - 使用重试机制")
    print("   - 检查网络稳定性")
    
    print("\n2. ✅ **DNS解析问题**")
    print("   - 更换DNS服务器 (8.8.8.8, 114.114.114.114)")
    print("   - 清除DNS缓存: ipconfig /flushdns")
    print("   - 检查hosts文件")
    
    print("\n3. ✅ **防火墙/代理问题**")
    print("   - 检查防火墙设置")
    print("   - 配置代理设置")
    print("   - 临时关闭安全软件测试")
    
    print("\n4. ✅ **浏览器配置问题**")
    print("   - 增加Chrome启动参数")
    print("   - 禁用扩展和插件")
    print("   - 使用无头模式测试")
    
    print("\n🎯 **推荐的解决步骤**:")
    print("```python")
    print("# 1. 使用带重试的浏览器打开")
    print("def open_browser_with_retry(max_retries=3):")
    print("    for attempt in range(max_retries):")
    print("        try:")
    print("            driver = DriverManager().create_chrome_driver()")
    print("            driver.set_page_load_timeout(60)  # 60秒超时")
    print("            driver.get(url)")
    print("            return driver")
    print("        except Exception as e:")
    print("            if attempt < max_retries - 1:")
    print("                time.sleep(5 * (attempt + 1))  # 递增等待")
    print("            else:")
    print("                raise")
    print("```")

def show_optimized_script():
    """显示优化后的脚本"""
    print("\n=== 优化后的脚本示例 ===")
    
    print("🚀 **pages/2.py 优化版本**:")
    print("```python")
    print("# 1. 带重试机制的浏览器打开")
    print("def open_browser_with_retry(max_retries=3):")
    print("    for attempt in range(max_retries):")
    print("        try:")
    print("            print(f'正在尝试打开浏览器，第{attempt + 1}次...')")
    print("            driver = DriverManager().create_chrome_driver()")
    print("            driver.set_page_load_timeout(60)  # 60秒超时")
    print("            ")
    print("            print('正在访问OrangeHRM登录页面...')")
    print("            driver.get('https://opensource-demo.orangehrmlive.com/web/index.php/auth/login')")
    print("            driver.maximize_window()")
    print("            print('✅ 浏览器打开成功，页面加载完成')")
    print("            time.sleep(2)")
    print("            return driver")
    print("            ")
    print("        except Exception as e:")
    print("            print(f'❌ 第{attempt + 1}次尝试失败: {e}')")
    print("            if 'driver' in locals():")
    print("                try:")
    print("                    driver.quit()")
    print("                except:")
    print("                    pass")
    print("            ")
    print("            if attempt < max_retries - 1:")
    print("                print(f'等待5秒后重试...')")
    print("                time.sleep(5)")
    print("            else:")
    print("                print('❌ 所有重试都失败，请检查网络连接')")
    print("                raise")
    print("")
    print("# 使用优化后的浏览器打开")
    print("driver = open_browser_with_retry()")
    print("```")

if __name__ == "__main__":
    print("🌐 OrangeHRM网络连接诊断工具")
    print("="*50)
    
    # 1. 网络连接测试
    network_ok = test_network_connectivity()
    
    if network_ok:
        # 2. 浏览器访问测试
        browser_ok = test_browser_access()
        
        if not browser_ok:
            # 3. 重试机制测试
            retry_ok = test_with_retry()
            
            if not retry_ok:
                print("\n❌ 所有测试都失败，请检查网络环境")
            else:
                print("\n✅ 重试机制测试成功")
        else:
            print("\n✅ 浏览器访问测试成功")
    else:
        print("\n❌ 基础网络连接失败")
    
    # 显示故障排除建议
    show_network_troubleshooting()
    
    # 显示优化脚本
    show_optimized_script()
    
    print("\n" + "="*50)
    print("🎯 诊断完成")
    
    print("\n✅ 解决方案总结:")
    print("1. ✅ 增加页面加载超时到60秒")
    print("2. ✅ 添加重试机制，最多重试3次")
    print("3. ✅ 优化Chrome启动参数")
    print("4. ✅ 添加网络连接检查")
    print("5. ✅ 递增等待时间策略")
    
    print("\n🚀 现在可以重新运行pages/2.py脚本！")
