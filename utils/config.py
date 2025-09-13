"""
配置管理模块
"""
import os
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class TestConfig:
    """测试配置类"""
    
    # 浏览器配置
    browser: str = "chrome"
    headless: bool = False
    window_size: tuple = (1920, 1080)
    implicit_wait: int = 10
    page_load_timeout: int = 30
    
    # 测试环境配置
    base_url: str = "https://opensource-demo.orangehrmlive.com"
    login_url: str = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    
    # 登录凭据
    username: str = "Admin"
    password: str = "admin123"
    
    # 截图配置
    screenshot_dir: str = "screenshots"
    screenshot_on_failure: bool = True
    screenshot_on_success: bool = False
    
    # 报告配置
    report_dir: str = "reports"
    html_report: bool = True
    json_report: bool = True
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/test.log"
    
    # 等待时间配置
    short_wait: int = 3
    medium_wait: int = 5
    long_wait: int = 10
    
    # 重试配置
    max_retries: int = 3
    retry_delay: int = 1
    
    # BDD配置
    bdd_tags: str = "@smoke"
    bdd_format: str = "pretty"
    
    # Claims测试数据
    test_employee_name: str = "Amelia Brown"
    test_event: str = "Travel allowances"
    test_currency: str = "Euro"
    test_remarks: str = "Automated test claim request"

class Config:
    """配置管理类"""
    
    def __init__(self):
        self._config = TestConfig()
        self._load_from_env()
    
    def _load_from_env(self):
        """从环境变量加载配置"""
        # 浏览器配置
        if os.getenv("BROWSER"):
            self._config.browser = os.getenv("BROWSER").lower()
        
        if os.getenv("HEADLESS"):
            self._config.headless = os.getenv("HEADLESS").lower() == "true"
        
        # URL配置
        if os.getenv("BASE_URL"):
            self._config.base_url = os.getenv("BASE_URL")
        
        if os.getenv("LOGIN_URL"):
            self._config.login_url = os.getenv("LOGIN_URL")
        
        # 登录凭据
        if os.getenv("USERNAME"):
            self._config.username = os.getenv("USERNAME")
        
        if os.getenv("PASSWORD"):
            self._config.password = os.getenv("PASSWORD")
        
        # 等待时间
        if os.getenv("IMPLICIT_WAIT"):
            self._config.implicit_wait = int(os.getenv("IMPLICIT_WAIT"))
        
        if os.getenv("PAGE_LOAD_TIMEOUT"):
            self._config.page_load_timeout = int(os.getenv("PAGE_LOAD_TIMEOUT"))
        
        # 截图配置
        if os.getenv("SCREENSHOT_DIR"):
            self._config.screenshot_dir = os.getenv("SCREENSHOT_DIR")
        
        if os.getenv("SCREENSHOT_ON_FAILURE"):
            self._config.screenshot_on_failure = os.getenv("SCREENSHOT_ON_FAILURE").lower() == "true"
        
        # 报告配置
        if os.getenv("REPORT_DIR"):
            self._config.report_dir = os.getenv("REPORT_DIR")
        
        # 日志配置
        if os.getenv("LOG_LEVEL"):
            self._config.log_level = os.getenv("LOG_LEVEL").upper()
        
        if os.getenv("LOG_FILE"):
            self._config.log_file = os.getenv("LOG_FILE")
    
    @property
    def browser(self) -> str:
        return self._config.browser
    
    @property
    def headless(self) -> bool:
        return self._config.headless
    
    @property
    def window_size(self) -> tuple:
        return self._config.window_size
    
    @property
    def implicit_wait(self) -> int:
        return self._config.implicit_wait
    
    @property
    def page_load_timeout(self) -> int:
        return self._config.page_load_timeout
    
    @property
    def base_url(self) -> str:
        return self._config.base_url
    
    @property
    def login_url(self) -> str:
        return self._config.login_url
    
    @property
    def username(self) -> str:
        return self._config.username
    
    @property
    def password(self) -> str:
        return self._config.password
    
    @property
    def screenshot_dir(self) -> str:
        return self._config.screenshot_dir
    
    @property
    def screenshot_on_failure(self) -> bool:
        return self._config.screenshot_on_failure
    
    @property
    def screenshot_on_success(self) -> bool:
        return self._config.screenshot_on_success
    
    @property
    def report_dir(self) -> str:
        return self._config.report_dir
    
    @property
    def html_report(self) -> bool:
        return self._config.html_report
    
    @property
    def json_report(self) -> bool:
        return self._config.json_report
    
    @property
    def log_level(self) -> str:
        return self._config.log_level
    
    @property
    def log_file(self) -> str:
        return self._config.log_file
    
    @property
    def short_wait(self) -> int:
        return self._config.short_wait
    
    @property
    def medium_wait(self) -> int:
        return self._config.medium_wait
    
    @property
    def long_wait(self) -> int:
        return self._config.long_wait
    
    @property
    def max_retries(self) -> int:
        return self._config.max_retries
    
    @property
    def retry_delay(self) -> int:
        return self._config.retry_delay
    
    @property
    def bdd_tags(self) -> str:
        return self._config.bdd_tags
    
    @property
    def bdd_format(self) -> str:
        return self._config.bdd_format
    
    @property
    def test_employee_name(self) -> str:
        return self._config.test_employee_name
    
    @property
    def test_event(self) -> str:
        return self._config.test_event
    
    @property
    def test_currency(self) -> str:
        return self._config.test_currency
    
    @property
    def test_remarks(self) -> str:
        return self._config.test_remarks
    
    def get_all_config(self) -> Dict[str, Any]:
        """获取所有配置"""
        return {
            "browser": self.browser,
            "headless": self.headless,
            "window_size": self.window_size,
            "implicit_wait": self.implicit_wait,
            "page_load_timeout": self.page_load_timeout,
            "base_url": self.base_url,
            "login_url": self.login_url,
            "username": self.username,
            "screenshot_dir": self.screenshot_dir,
            "screenshot_on_failure": self.screenshot_on_failure,
            "report_dir": self.report_dir,
            "log_level": self.log_level,
            "short_wait": self.short_wait,
            "medium_wait": self.medium_wait,
            "long_wait": self.long_wait,
            "max_retries": self.max_retries,
            "test_employee_name": self.test_employee_name,
            "test_event": self.test_event,
            "test_currency": self.test_currency,
            "test_remarks": self.test_remarks
        }
    
    def update_config(self, **kwargs):
        """更新配置"""
        for key, value in kwargs.items():
            if hasattr(self._config, key):
                setattr(self._config, key, value)

# 创建全局配置实例
config = Config()

# 便捷函数
def get_config() -> Config:
    """获取配置实例"""
    return config

def get_browser_config() -> Dict[str, Any]:
    """获取浏览器配置"""
    return {
        "browser": config.browser,
        "headless": config.headless,
        "window_size": config.window_size,
        "implicit_wait": config.implicit_wait,
        "page_load_timeout": config.page_load_timeout
    }

def get_test_data() -> Dict[str, str]:
    """获取测试数据"""
    return {
        "employee_name": config.test_employee_name,
        "event": config.test_event,
        "currency": config.test_currency,
        "remarks": config.test_remarks
    }
