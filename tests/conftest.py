"""
pytest配置文件
定义测试夹具和全局配置
"""
import pytest
import sys
from pathlib import Path
from loguru import logger
from utils.driver_manager import DriverManager
from utils.screenshot_utils import screenshot_utils, ScreenshotUtils
from utils.pytest_plugin import add_test_screenshot
from config.config_manager import config

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 暂时禁用自定义插件
# pytest_plugins = ["utils.pytest_plugin"]


def pytest_configure(config_obj):
    """pytest配置"""
    # 配置日志
    logger.remove()  # 移除默认处理器
    
    # 添加控制台日志处理器
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        level="INFO",
        colorize=True
    )
    
    # 添加文件日志处理器
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logger.add(
        "logs/test.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} | {message}",
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        encoding="utf-8"
    )


@pytest.fixture(scope="session")
def test_config():
    """测试配置夹具"""
    return config


@pytest.fixture(params=["chrome", "edge", "edge_ie", "ie"])
def browser_name(request):
    """浏览器名称参数化夹具"""
    return request.param


@pytest.fixture
def driver_manager():
    """WebDriver管理器夹具"""
    manager = DriverManager()
    yield manager
    manager.quit_driver()


@pytest.fixture
def chrome_driver(driver_manager):
    """Chrome浏览器驱动夹具"""
    driver = driver_manager.create_chrome_driver()
    yield driver
    driver_manager.quit_driver()


@pytest.fixture
def edge_driver(driver_manager):
    """Edge浏览器驱动夹具"""
    driver = driver_manager.create_edge_driver()
    yield driver
    driver_manager.quit_driver()


@pytest.fixture
def edge_ie_driver(driver_manager):
    """Edge IE兼容模式驱动夹具"""
    driver = driver_manager.create_edge_ie_mode_driver()
    yield driver
    driver_manager.quit_driver()


@pytest.fixture
def edge_driver(driver_manager):
    """Microsoft Edge浏览器驱动夹具"""
    driver = driver_manager.create_edge_driver_standard()
    yield driver
    driver_manager.quit_driver()


@pytest.fixture
def browser_driver(browser_name, driver_manager):
    """参数化浏览器驱动夹具"""
    driver = driver_manager.create_driver(browser_name)
    yield driver
    driver_manager.quit_driver()


@pytest.fixture(autouse=True)
def test_setup_teardown(request):
    """测试设置和清理夹具"""
    test_name = request.node.name
    logger.info(f"=== 开始测试: {test_name} ===")
    
    yield
    
    logger.info(f"=== 结束测试: {test_name} ===")


@pytest.fixture
def screenshot_helper(request):
    """截图助手夹具"""
    # 从测试名称中提取测试会话名称
    test_name = request.node.name

    # 解析测试名称，提取浏览器和测试类型
    if "chrome" in test_name.lower():
        browser = "chrome"
    elif "edge_ie" in test_name.lower():
        browser = "edge_ie"
    elif "edge" in test_name.lower():
        browser = "edge"
    elif "ie" in test_name.lower() or "internet_explorer" in test_name.lower():
        browser = "ie"
    else:
        browser = "unknown"

    # 优化测试类型识别逻辑
    if "login" in test_name.lower():
        test_type = "login"
    elif "exceptions" in test_name.lower():
        test_type = "exceptions"
    elif "complete_flow" in test_name.lower():
        test_type = "tests"  # 完整流程测试使用 "tests"
    else:
        test_type = "tests"  # 默认使用 "tests" 而不是 "unknown"

    # 创建测试会话名称
    session_name = f"{browser}_{test_type}"

    # 创建带会话名称的截图工具
    session_screenshot_utils = ScreenshotUtils(test_session_name=session_name)

    class ScreenshotHelper:
        def __init__(self, request_obj, session_utils):
            self.request = request_obj
            self.session_utils = session_utils

        def take_screenshot(self, driver, step_name, browser_name="browser"):
            """截图并添加到测试报告"""
            screenshot_path = self.session_utils.take_screenshot(driver, step_name, browser_name)
            if screenshot_path:
                add_test_screenshot(self.request, screenshot_path)
            return screenshot_path

        def take_success_screenshot(self, driver, step_name, browser_name="browser"):
            """成功截图并添加到测试报告"""
            screenshot_path = self.session_utils.take_success_screenshot(driver, step_name, browser_name)
            if screenshot_path:
                add_test_screenshot(self.request, screenshot_path)
            return screenshot_path

        def take_failure_screenshot(self, driver, test_name, error_message, browser_name="browser"):
            """失败截图并添加到测试报告"""
            screenshot_path = self.session_utils.take_failure_screenshot(driver, test_name, error_message, browser_name)
            if screenshot_path:
                add_test_screenshot(self.request, screenshot_path)
            return screenshot_path

    return ScreenshotHelper(request, session_screenshot_utils)


def pytest_runtest_makereport(item, call):
    """测试报告生成钩子"""
    if call.when == "call":
        # 获取测试结果
        if call.excinfo is not None:
            # 测试失败
            logger.error(f"测试失败: {item.name}")
            
            # 如果有driver夹具，尝试截图
            if hasattr(item, "funcargs"):
                for fixture_name in ["chrome_driver", "edge_driver", "browser_driver"]:
                    if fixture_name in item.funcargs:
                        driver = item.funcargs[fixture_name]
                        browser_name = getattr(item.funcargs.get("browser_name", "unknown"), "param", "unknown")
                        screenshot_utils.take_failure_screenshot(
                            driver, 
                            item.name, 
                            str(call.excinfo.value),
                            browser_name
                        )
                        break
        else:
            # 测试成功
            logger.info(f"测试成功: {item.name}")


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """设置测试环境"""
    logger.info("=== 开始自动化测试 ===")
    
    # 确保必要的目录存在
    Path("reports").mkdir(exist_ok=True)
    Path("screenshots").mkdir(exist_ok=True)
    
    yield
    
    # 清理旧截图
    screenshot_utils.cleanup_old_screenshots(days=7)
    
    logger.info("=== 自动化测试完成 ===")


# 自定义标记
def pytest_configure(config):
    """注册自定义标记"""
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "regression: 回归测试")
    config.addinivalue_line("markers", "login: 登录相关测试")
    config.addinivalue_line("markers", "exceptions: 异常测试")
    config.addinivalue_line("markers", "chrome: Chrome浏览器测试")
    config.addinivalue_line("markers", "edge: Edge浏览器测试")
