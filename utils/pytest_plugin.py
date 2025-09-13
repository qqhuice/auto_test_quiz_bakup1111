"""
pytest插件
集成截图和报告功能到pytest测试框架中
"""
import time
from pathlib import Path
import pytest
from loguru import logger
from utils.report_manager import report_manager
from utils.screenshot_utils import screenshot_utils


class TestReportPlugin:
    """测试报告插件类"""
    
    def __init__(self):
        """初始化插件"""
        self.test_start_time = {}
        self.test_screenshots = {}
    
    @pytest.hookimpl(tryfirst=True)
    def pytest_sessionstart(self, session):
        """测试会话开始"""
        logger.info("=== 开始自动化测试会话 ===")
        report_manager.start_test_session()
    
    @pytest.hookimpl(trylast=True)
    def pytest_sessionfinish(self, session, exitstatus):
        """测试会话结束"""
        report_manager.end_test_session()
        
        # 生成报告
        html_report = report_manager.generate_html_report()
        json_report = report_manager.generate_json_report()
        
        if html_report:
            logger.info(f"HTML测试报告已生成: {html_report}")
        if json_report:
            logger.info(f"JSON测试报告已生成: {json_report}")
        
        logger.info("=== 自动化测试会话结束 ===")
    
    @pytest.hookimpl(tryfirst=True)
    def pytest_runtest_setup(self, item):
        """测试用例开始前的设置"""
        test_name = item.nodeid
        self.test_start_time[test_name] = time.time()
        self.test_screenshots[test_name] = []
        logger.info(f"开始测试: {test_name}")
    
    @pytest.hookimpl(trylast=True)
    def pytest_runtest_teardown(self, item, nextitem):
        """测试用例结束后的清理"""
        test_name = item.nodeid
        logger.info(f"结束测试: {test_name}")
    
    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        """生成测试报告"""
        outcome = yield
        report = outcome.get_result()

        test_name = item.nodeid

        if call.when == "call":
            # 计算执行时间
            start_time = self.test_start_time.get(test_name, time.time())
            duration = time.time() - start_time

            # 获取测试状态
            if report.passed:
                status = "PASSED"
                error_message = None
            elif report.failed:
                status = "FAILED"
                error_message = str(report.longrepr) if report.longrepr else "测试失败"

                # 失败时自动截图
                self._take_failure_screenshot(item, error_message)
            elif report.skipped:
                status = "SKIPPED"
                error_message = str(report.longrepr) if report.longrepr else "测试跳过"
            else:
                status = "UNKNOWN"
                error_message = "未知状态"

            # 获取截图列表
            screenshots = self.test_screenshots.get(test_name, [])

            # 添加测试结果到报告管理器
            report_manager.add_test_result(
                test_name=test_name,
                status=status,
                duration=duration,
                error_message=error_message,
                screenshots=screenshots
            )

            logger.info(f"测试结果: {test_name} - {status} ({duration:.2f}s)")

        return report
    
    def _take_failure_screenshot(self, item, error_message):
        """
        测试失败时自动截图
        
        Args:
            item: pytest测试项
            error_message: 错误信息
        """
        try:
            # 尝试从测试夹具中获取driver
            driver = None
            browser_name = "unknown"
            
            if hasattr(item, "funcargs"):
                # 查找driver夹具
                for fixture_name in ["chrome_driver", "edge_driver", "browser_driver"]:
                    if fixture_name in item.funcargs:
                        driver = item.funcargs[fixture_name]
                        browser_name = fixture_name.replace("_driver", "")
                        break
                
                # 查找browser_name夹具
                if "browser_name" in item.funcargs:
                    browser_name = item.funcargs["browser_name"]
            
            if driver:
                screenshot_path = screenshot_utils.take_failure_screenshot(
                    driver, 
                    item.name, 
                    error_message,
                    browser_name
                )
                
                if screenshot_path:
                    test_name = item.nodeid
                    if test_name not in self.test_screenshots:
                        self.test_screenshots[test_name] = []
                    self.test_screenshots[test_name].append(screenshot_path)
                    
        except Exception as e:
            logger.error(f"自动截图失败: {e}")
    
    def add_screenshot(self, test_name: str, screenshot_path: str):
        """
        添加截图到测试结果
        
        Args:
            test_name: 测试名称
            screenshot_path: 截图路径
        """
        if test_name not in self.test_screenshots:
            self.test_screenshots[test_name] = []
        self.test_screenshots[test_name].append(screenshot_path)


# 创建插件实例
test_report_plugin = TestReportPlugin()


# pytest钩子函数
def pytest_sessionstart(session):
    """测试会话开始钩子"""
    test_report_plugin.pytest_sessionstart(session)


def pytest_sessionfinish(session, exitstatus):
    """测试会话结束钩子"""
    test_report_plugin.pytest_sessionfinish(session, exitstatus)


def pytest_runtest_setup(item):
    """测试设置钩子"""
    test_report_plugin.pytest_runtest_setup(item)


def pytest_runtest_teardown(item, nextitem):
    """测试清理钩子"""
    test_report_plugin.pytest_runtest_teardown(item, nextitem)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """测试报告生成钩子"""
    yield from test_report_plugin.pytest_runtest_makereport(item, call)


# 提供给测试用例使用的截图函数
def add_test_screenshot(request, screenshot_path: str):
    """
    在测试用例中添加截图
    
    Args:
        request: pytest request对象
        screenshot_path: 截图路径
    """
    test_name = request.node.nodeid
    test_report_plugin.add_screenshot(test_name, screenshot_path)
