"""
WebDriver管理器
负责创建和管理不同浏览器的WebDriver实例
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.ie.options import Options as IEOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager
from loguru import logger
from config.config_manager import config


class DriverManager:
    """WebDriver管理器类"""
    
    def __init__(self):
        """初始化DriverManager"""
        self.driver = None
        self.browser_config = config.browser_config
    
    def create_chrome_driver(self, headless: bool = None) -> webdriver.Chrome:
        """
        创建Chrome浏览器驱动
        
        Args:
            headless: 是否无头模式，None时使用配置文件设置
            
        Returns:
            Chrome WebDriver实例
        """
        logger.info("正在创建Chrome浏览器驱动...")
        
        # 配置Chrome选项
        chrome_options = ChromeOptions()
        
        # 设置无头模式
        if headless is None:
            headless = self.browser_config.get('headless', False)
        if headless:
            chrome_options.add_argument('--headless')
        
        # 基本选项
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')

        # 网络优化选项
        chrome_options.add_argument('--disable-background-timer-throttling')
        chrome_options.add_argument('--disable-backgrounding-occluded-windows')
        chrome_options.add_argument('--disable-renderer-backgrounding')
        chrome_options.add_argument('--disable-features=TranslateUI')
        chrome_options.add_argument('--disable-ipc-flooding-protection')
        chrome_options.add_argument('--disable-background-networking')
        chrome_options.add_argument('--disable-default-apps')
        chrome_options.add_argument('--disable-sync')

        # 性能优化
        chrome_options.add_argument('--max_old_space_size=4096')
        chrome_options.add_argument('--disable-logging')
        chrome_options.add_argument('--disable-gpu-logging')
        chrome_options.add_argument('--silent')

        # 网络超时设置
        chrome_options.add_argument('--timeout=60000')
        chrome_options.add_argument('--enable-features=NetworkService,NetworkServiceLogging')
        
        # 设置窗口大小
        window_size = self.browser_config.get('window_size', '1920,1080')
        chrome_options.add_argument(f'--window-size={window_size}')
        
        # 禁用自动化检测
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # 尝试使用系统PATH中的ChromeDriver
            try:
                service = ChromeService()  # 使用系统PATH中的chromedriver
                driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("使用系统PATH中的ChromeDriver")
            except Exception as e:
                logger.warning(f"系统PATH中的ChromeDriver不可用: {e}")
                # 回退到webdriver-manager
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info("使用webdriver-manager下载的ChromeDriver")
            
            # 执行脚本隐藏webdriver属性
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # 设置超时
            self._set_timeouts(driver)
            
            self.driver = driver
            logger.info("Chrome浏览器驱动创建成功")
            return driver
            
        except Exception as e:
            logger.error(f"Chrome浏览器驱动创建失败: {e}")
            raise
    
    def create_edge_driver(self, headless: bool = None, ie_mode: bool = False) -> webdriver.Edge:
        """
        创建Edge浏览器驱动

        Args:
            headless: 是否无头模式，None时使用配置文件设置
            ie_mode: 是否启用IE兼容模式

        Returns:
            Edge WebDriver实例
        """
        logger.info(f"正在创建Edge浏览器驱动 (IE Mode: {ie_mode})...")

        # 配置Edge选项
        edge_options = EdgeOptions()

        # 设置无头模式
        if headless is None:
            headless = self.browser_config.get('headless', False)
        if headless:
            edge_options.add_argument('--headless')

        # IE Mode配置
        if ie_mode:
            # 启用IE兼容模式
            edge_options.add_argument('--ie-mode-force')
            edge_options.add_argument('--disable-features=msEdgeEnableIEMode')
            edge_options.add_experimental_option('useAutomationExtension', False)
            edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            logger.info("已启用Edge IE兼容模式")

        # 基本选项
        edge_options.add_argument('--start-maximized')
        edge_options.add_argument('--disable-blink-features=AutomationControlled')
        edge_options.add_argument('--disable-extensions')
        edge_options.add_argument('--no-sandbox')
        edge_options.add_argument('--disable-dev-shm-usage')

        # 设置窗口大小
        window_size = self.browser_config.get('window_size', '1920,1080')
        edge_options.add_argument(f'--window-size={window_size}')

        try:
            # 尝试使用系统PATH中的EdgeDriver
            try:
                service = EdgeService()  # 使用系统PATH中的msedgedriver
                driver = webdriver.Edge(service=service, options=edge_options)
                logger.info("使用系统PATH中的EdgeDriver")
            except Exception as e:
                logger.warning(f"系统PATH中的EdgeDriver不可用: {e}")
                # 回退到webdriver-manager
                service = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=service, options=edge_options)
                logger.info("使用webdriver-manager下载的EdgeDriver")

            # 设置超时
            self._set_timeouts(driver)

            self.driver = driver
            logger.info("Edge浏览器驱动创建成功")
            return driver

        except Exception as e:
            logger.error(f"Edge浏览器驱动创建失败: {e}")
            raise

    def create_edge_ie_mode_driver(self, headless: bool = None) -> webdriver.Edge:
        """
        创建Edge IE兼容模式驱动

        Args:
            headless: 是否无头模式

        Returns:
            Edge IE Mode WebDriver实例
        """
        return self.create_edge_driver(headless=headless, ie_mode=True)

    def create_edge_driver_standard(self, headless: bool = False) -> webdriver.Edge:
        """
        创建Microsoft Edge浏览器驱动（标准模式）

        Args:
            headless: 是否以无头模式运行

        Returns:
            Edge WebDriver实例
        """
        logger.info("正在创建Microsoft Edge浏览器驱动...")

        # 配置Edge选项
        edge_options = EdgeOptions()

        # Edge特定配置
        edge_options.add_argument('--disable-extensions')
        edge_options.add_argument('--disable-plugins')
        edge_options.add_argument('--disable-dev-shm-usage')
        edge_options.add_argument('--no-sandbox')
        edge_options.add_argument('--disable-gpu')
        edge_options.add_argument('--disable-web-security')
        edge_options.add_argument('--allow-running-insecure-content')
        edge_options.add_argument('--ignore-certificate-errors')
        edge_options.add_argument('--ignore-ssl-errors')
        edge_options.add_argument('--ignore-certificate-errors-spki-list')

        # 设置无头模式
        if headless:
            edge_options.add_argument('--headless')
            logger.info("Edge浏览器将以无头模式运行")

        # 设置窗口大小
        window_size = self.browser_config.get('window_size', '1920,1080')
        width, height = window_size.split(',')
        edge_options.add_argument(f'--window-size={width},{height}')

        # 设置Edge特定的实验性选项
        edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        edge_options.add_experimental_option('useAutomationExtension', False)

        try:
            # 尝试使用系统PATH中的EdgeDriver
            try:
                service = EdgeService()  # 使用系统PATH中的msedgedriver
                driver = webdriver.Edge(service=service, options=edge_options)
                logger.info("使用系统PATH中的msedgedriver")
            except Exception as e:
                logger.warning(f"系统PATH中的msedgedriver不可用: {e}")
                # 回退到webdriver-manager
                service = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=service, options=edge_options)
                logger.info("使用webdriver-manager下载的msedgedriver")

            # 设置超时
            self._set_timeouts(driver)

            # 最大化窗口
            driver.maximize_window()

            self.driver = driver
            logger.info("Microsoft Edge浏览器驱动创建成功")
            return driver

        except Exception as e:
            logger.error(f"Microsoft Edge浏览器驱动创建失败: {e}")
            logger.error("请确保：")
            logger.error("1. 已安装Microsoft Edge浏览器")
            logger.error("2. 已下载msedgedriver.exe并添加到PATH")
            logger.error("3. Edge浏览器版本与驱动版本匹配")
            logger.error("4. 或者安装webdriver-manager: pip install webdriver-manager")
            raise
    
    def create_driver(self, browser_name: str = None, headless: bool = None, ie_mode: bool = False):
        """
        根据浏览器名称创建驱动

        Args:
            browser_name: 浏览器名称 ('chrome', 'edge', 'edge_ie', 'edge_standard')
            headless: 是否无头模式
            ie_mode: 是否启用IE兼容模式

        Returns:
            WebDriver实例
        """
        if browser_name is None:
            browser_name = self.browser_config.get('default', 'chrome')

        browser_name = browser_name.lower()

        if browser_name == 'chrome':
            return self.create_chrome_driver(headless)
        elif browser_name == 'edge':
            return self.create_edge_driver(headless, ie_mode)
        elif browser_name == 'edge_ie' or browser_name == 'edge_ie_mode':
            return self.create_edge_ie_mode_driver(headless)
        elif browser_name == 'edge_standard' or browser_name == 'edge_normal':
            return self.create_edge_driver_standard(headless)
        else:
            raise ValueError(f"不支持的浏览器类型: {browser_name}")
    
    def _set_timeouts(self, driver):
        """
        设置WebDriver超时时间

        Args:
            driver: WebDriver实例
        """
        # 隐式等待
        implicit_wait = self.browser_config.get('implicit_wait', 15)  # 增加到15秒
        driver.implicitly_wait(implicit_wait)

        # 页面加载超时 - 增加到60秒以应对网络问题
        page_load_timeout = self.browser_config.get('page_load_timeout', 60)
        driver.set_page_load_timeout(page_load_timeout)

        # 脚本执行超时 - 增加到45秒
        script_timeout = self.browser_config.get('script_timeout', 45)
        driver.set_script_timeout(script_timeout)

        logger.info(f"设置超时时间 - 隐式等待: {implicit_wait}s, 页面加载: {page_load_timeout}s, 脚本执行: {script_timeout}s")
    
    def quit_driver(self):
        """关闭浏览器驱动"""
        if self.driver:
            logger.info("正在关闭浏览器驱动...")
            try:
                self.driver.quit()
                logger.info("浏览器驱动已关闭")
            except Exception as e:
                logger.error(f"关闭浏览器驱动时出错: {e}")
            finally:
                self.driver = None
    
    def get_driver(self):
        """获取当前驱动实例"""
        return self.driver
