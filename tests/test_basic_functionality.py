"""
基础功能测试
验证项目的基本组件是否正常工作
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from config.config_manager import config
from utils.screenshot_utils import screenshot_utils
from utils.report_manager import report_manager


class TestBasicFunctionality:
    """基础功能测试类"""
    
    def test_config_manager(self):
        """测试配置管理器"""
        # 测试配置读取
        browser_config = config.browser_config
        assert browser_config is not None
        assert 'default' in browser_config
        
        # 测试URL配置
        urls = config.urls
        assert urls is not None
        assert 'practice_home' in urls
        
        # 测试登录数据
        login_data = config.login_data
        assert login_data is not None
        assert 'valid_username' in login_data
        assert 'valid_password' in login_data
        
        print("✅ 配置管理器测试通过")
    
    def test_screenshot_utils(self):
        """测试截图工具"""
        # 测试截图目录创建
        screenshot_dir = Path("screenshots")
        assert screenshot_dir.exists()
        
        # 测试文件名清理功能
        clean_name = screenshot_utils._sanitize_filename("测试<>文件名:?*")
        assert "<" not in clean_name
        assert ">" not in clean_name
        assert ":" not in clean_name
        
        print("✅ 截图工具测试通过")
    
    def test_report_manager(self):
        """测试报告管理器"""
        # 测试报告目录创建
        report_dir = Path("reports")
        assert report_dir.exists()
        
        # 测试添加测试结果
        report_manager.start_test_session()
        report_manager.add_test_result(
            test_name="test_example",
            status="PASSED",
            duration=1.5,
            error_message=None,
            screenshots=[]
        )
        report_manager.end_test_session()
        
        # 验证测试结果
        assert len(report_manager.test_results) > 0
        assert report_manager.test_results[0]['name'] == "test_example"
        assert report_manager.test_results[0]['status'] == "PASSED"
        
        print("✅ 报告管理器测试通过")
    
    def test_project_structure(self):
        """测试项目结构"""
        # 获取项目根目录
        project_root = Path(__file__).parent.parent

        # 验证必要的目录存在
        required_dirs = [
            "config",
            "pages",
            "tests",
            "utils",
            "reports",
            "screenshots"
        ]

        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            assert dir_path.exists(), f"目录 {dir_name} 不存在，路径: {dir_path}"

        # 验证必要的文件存在
        required_files = [
            "requirements.txt",
            "pytest.ini",
            "run_tests.py",
            "config/config.yaml"
        ]

        for file_name in required_files:
            file_path = project_root / file_name
            assert file_path.exists(), f"文件 {file_name} 不存在，路径: {file_path}"

        print("✅ 项目结构测试通过")
    
    def test_page_objects_import(self):
        """测试页面对象导入"""
        try:
            from pages.base_page import BasePage
            from pages.practice_home_page import PracticeHomePage
            from pages.login_page import LoginPage
            from pages.exceptions_page import ExceptionsPage
            
            # 验证类定义
            assert BasePage is not None
            assert PracticeHomePage is not None
            assert LoginPage is not None
            assert ExceptionsPage is not None
            
            print("✅ 页面对象导入测试通过")
            
        except ImportError as e:
            pytest.fail(f"页面对象导入失败: {e}")
    
    def test_utils_import(self):
        """测试工具类导入"""
        try:
            from utils.driver_manager import DriverManager
            from utils.screenshot_utils import ScreenshotUtils
            from utils.report_manager import ReportManager
            
            # 验证类定义
            assert DriverManager is not None
            assert ScreenshotUtils is not None
            assert ReportManager is not None
            
            print("✅ 工具类导入测试通过")
            
        except ImportError as e:
            pytest.fail(f"工具类导入失败: {e}")
    
    def test_config_values(self):
        """测试配置值"""
        # 测试浏览器配置
        assert config.get('browser.default') in ['chrome', 'edge']
        assert isinstance(config.get('browser.implicit_wait'), int)
        assert isinstance(config.get('browser.explicit_wait'), int)
        
        # 测试URL配置
        practice_url = config.get('urls.practice_home')
        assert practice_url.startswith('https://')
        assert 'practicetestautomation.com' in practice_url
        
        # 测试登录数据
        username = config.get('test_data.login.valid_username')
        password = config.get('test_data.login.valid_password')
        assert username is not None
        assert password is not None
        assert len(username) > 0
        assert len(password) > 0
        
        print("✅ 配置值测试通过")
    
    def test_documentation_files(self):
        """测试文档文件"""
        # 获取项目根目录
        project_root = Path(__file__).parent.parent

        doc_files = [
            "Python_Selenium_项目使用指南.md",
            "README_Python.md",
            "Python项目完成总结.md"
        ]

        for doc_file in doc_files:
            file_path = project_root / doc_file
            assert file_path.exists(), f"文档文件 {doc_file} 不存在，路径: {file_path}"

            # 检查文件不为空
            content = file_path.read_text(encoding='utf-8')
            assert len(content) > 100, f"文档文件 {doc_file} 内容太少"

        print("✅ 文档文件测试通过")
    
    def test_run_scripts(self):
        """测试运行脚本"""
        # 获取项目根目录
        project_root = Path(__file__).parent.parent

        scripts = [
            "run_tests.py",
            "run_tests.bat"
        ]

        for script in scripts:
            script_path = project_root / script
            assert script_path.exists(), f"运行脚本 {script} 不存在，路径: {script_path}"

            # 检查文件不为空
            content = script_path.read_text(encoding='utf-8')
            assert len(content) > 50, f"运行脚本 {script} 内容太少"

        print("✅ 运行脚本测试通过")


if __name__ == "__main__":
    # 直接运行测试
    pytest.main([__file__, "-v"])
