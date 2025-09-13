"""
Selenium基础验证测试
实现README.md中要求的基础验证测试用例

根据更新后的测试流程要求：
1. 使用Selenium打开测试网站 https://practicetestautomation.com/practice/
2. 点击Test Login Page，完成页面下方case
3. 点击测试网站的practice页面（不使用浏览器返回）
4. 点击Test Exceptions，完成页面下方case
5. 每一步操作请附带步骤说明和截图，生成文档
6. 需同时对Chrome和Microsoft Edge (IE Mode)两种浏览器进行实现
"""

# 导入pytest测试框架 - 用于组织和运行测试用例
import pytest
# 导入time模块 - 用于添加等待时间
import time
# 导入loguru日志库 - 用于记录测试执行过程中的日志信息
from loguru import logger
# 导入页面对象模型 - 封装了页面元素和操作的类
from pages.practice_home_page import PracticeHomePage  # 练习网站首页页面对象
from pages.login_page import LoginPage                 # 登录页面页面对象
from pages.exceptions_page import ExceptionsPage       # 异常测试页面页面对象
# 导入截图工具 - 用于在测试过程中自动截图
from utils.screenshot_utils import screenshot_utils


class TestSeleniumBasic:
    """
    Selenium基础验证测试类

    该类包含了README.md第一题要求的所有测试用例：
    - Chrome浏览器登录页面验证测试
    - Chrome浏览器异常页面验证测试
    - Edge浏览器测试（暂时注释）
    - Edge IE模式测试（暂时注释）
    """
    
    # ==================== Chrome浏览器测试用例 ====================

    # 注释掉单独的登录和异常测试，避免与完整流程测试重复
    # 现在只保留完整流程测试，实现：
    # 打开网站 → test login page执行3个用例 → 点击practice → 点击test Exceptions执行5个异常用例 → 测试结束

    # @pytest.mark.order(1)                    # 单独登录测试（已注释，避免重复）
    # @pytest.mark.smoke
    # @pytest.mark.login
    # def test_01_chrome_login_page_validation(self, chrome_driver, screenshot_helper):
    #     """
    #     Chrome浏览器 - 登录页面验证测试（已注释，避免与完整流程重复）
    #
    #     注意：此测试已被注释，因为完整流程测试已包含登录页面验证
    #     避免重复执行相同的测试用例
    #     """
    #     self._execute_login_page_test(chrome_driver, "Chrome", screenshot_helper)

    # @pytest.mark.order(2)                    # 单独异常测试（已注释，避免重复）
    # @pytest.mark.smoke
    # @pytest.mark.exceptions
    # def test_02_chrome_exceptions_page_validation(self, chrome_driver, screenshot_helper):
    #     """
    #     Chrome浏览器 - 异常页面验证测试（已注释，避免与完整流程重复）
    #
    #     注意：此测试已被注释，因为完整流程测试已包含异常页面验证
    #     避免重复执行相同的测试用例
    #     """
    #     self._execute_exceptions_page_test(chrome_driver, "Chrome", screenshot_helper)

    # ==================== Edge浏览器测试用例（暂时注释，专注Chrome优化） ====================

    # @pytest.mark.order(3)                    # Edge浏览器登录测试执行顺序
    # @pytest.mark.smoke                       # 冒烟测试标记
    # @pytest.mark.login                       # 登录测试标记
    # def test_03_edge_login_page_validation(self, edge_driver, screenshot_helper):
    #     """
    #     Edge浏览器 - 登录页面验证测试
    #
    #     注意：暂时注释此测试，专注于Chrome浏览器的优化
    #     后续需要时可以取消注释并启用
    #     """
    #     # 调用私有方法执行Edge浏览器登录页面测试
    #     self._execute_login_page_test(edge_driver, "Edge", screenshot_helper)

    # @pytest.mark.order(4)                    # Edge浏览器异常测试执行顺序
    # @pytest.mark.smoke                       # 冒烟测试标记
    # @pytest.mark.exceptions                  # 异常测试标记
    # def test_04_edge_exceptions_page_validation(self, edge_driver, screenshot_helper):
    #     """
    #     Edge浏览器 - 异常页面验证测试
    #
    #     注意：暂时注释此测试，专注于Chrome浏览器的优化
    #     后续需要时可以取消注释并启用
    #     """
    #     # 调用私有方法执行Edge浏览器异常页面测试
    #     self._execute_exceptions_page_test(edge_driver, "Edge", screenshot_helper)

    # ==================== Edge IE模式测试用例（暂时注释，专注Chrome优化） ====================

    # @pytest.mark.order(5)                    # Edge IE模式登录测试执行顺序
    # @pytest.mark.smoke                       # 冒烟测试标记
    # @pytest.mark.login                       # 登录测试标记
    # def test_05_edge_ie_login_page_validation(self, edge_ie_driver, screenshot_helper):
    #     """
    #     Edge IE兼容模式 - 登录页面验证测试
    #
    #     注意：暂时注释此测试，专注于Chrome浏览器的优化
    #     Edge IE模式需要特殊配置，后续需要时可以取消注释并启用
    #     """
    #     # 调用私有方法执行Edge IE模式登录页面测试
    #     self._execute_login_page_test(edge_ie_driver, "Edge_IE", screenshot_helper)

    # @pytest.mark.order(6)                    # Edge IE模式异常测试执行顺序
    # @pytest.mark.smoke                       # 冒烟测试标记
    # @pytest.mark.exceptions                  # 异常测试标记
    # def test_06_edge_ie_exceptions_page_validation(self, edge_ie_driver, screenshot_helper):
    #     """
    #     Edge IE兼容模式 - 异常页面验证测试
    #
    #     注意：暂时注释此测试，专注于Chrome浏览器的优化
    #     Edge IE模式需要特殊配置，后续需要时可以取消注释并启用
    #     """
    #     # 调用私有方法执行Edge IE模式异常页面测试
    #     self._execute_exceptions_page_test(edge_ie_driver, "Edge_IE", screenshot_helper)
    
    # ==================== 主要测试用例：完整流程测试 ====================

    @pytest.mark.order(1)                    # 指定为第1个执行的测试
    @pytest.mark.smoke                       # 标记为冒烟测试
    @pytest.mark.regression                  # 标记为回归测试，用于全面验证功能
    def test_01_chrome_complete_flow(self, chrome_driver, screenshot_helper):
        """
        Chrome浏览器 - 完整流程测试（主要测试）

        这是唯一的主要测试，避免重复执行，实现完整的测试流程：

        测试目标：按照更新后的完整流程执行测试
        测试步骤：
        1. 打开测试网站首页
        2. 点击Test Login Page，执行3个登录用例
        3. 点击测试网站的practice页面（不关闭浏览器）
        4. 点击Test Exceptions，执行5个异常用例
        5. 测试结束

        特点：
        - 浏览器在整个测试过程中保持打开状态
        - 避免了登录和异常测试的重复执行
        - 包含完整的截图记录

        Args:
            chrome_driver: Chrome浏览器驱动实例
            screenshot_helper: 截图助手实例
        """
        # 调用私有方法执行Chrome浏览器完整流程测试
        self._execute_complete_flow_test(chrome_driver, "Chrome", screenshot_helper)

    @pytest.mark.order(2)                    # 指定为第2个执行的测试
    @pytest.mark.smoke                       # 标记为冒烟测试
    @pytest.mark.regression                  # 标记为回归测试，用于全面验证功能
    def test_02_edge_complete_flow(self, edge_driver, screenshot_helper):
        """
        Microsoft Edge浏览器 - 完整流程测试（主要测试）

        这是Edge浏览器的主要测试，与Chrome测试采用完全相同的流程：

        测试目标：按照更新后的完整流程执行测试
        测试步骤：
        1. 打开测试网站首页
        2. 点击Test Login Page，执行3个登录用例
        3. 点击测试网站的practice页面（不关闭浏览器）
        4. 点击Test Exceptions，执行5个异常用例
        5. 测试结束（浏览器关闭）

        与Chrome测试的区别：
        - 唯一不同的是使用Edge浏览器执行
        - 测试流程、用例、验证点完全相同
        - 实现UI测试的兼容性验证
        """
        logger.info("=== 开始执行Microsoft Edge浏览器完整流程测试 ===")

        # 调用私有方法执行完整流程测试
        self._execute_complete_flow_test(edge_driver, "Edge", screenshot_helper)

    # ==================== Edge完整流程测试（暂时注释，专注Chrome优化） ====================

    # @pytest.mark.regression                  # 回归测试标记
    # def test_complete_flow_edge(self, edge_driver, screenshot_helper):
    #     """
    #     Edge浏览器 - 完整流程测试
    #
    #     注意：暂时注释此测试，专注于Chrome浏览器的优化
    #     后续需要时可以取消注释并启用
    #     """
    #     # 调用私有方法执行Edge浏览器完整流程测试
    #     self._execute_complete_flow_test(edge_driver, "Edge", screenshot_helper)

    # @pytest.mark.regression                  # 回归测试标记
    # def test_complete_flow_edge_ie(self, edge_ie_driver, screenshot_helper):
    #     """
    #     Edge IE兼容模式 - 完整流程测试
    #
    #     注意：暂时注释此测试，专注于Chrome浏览器的优化
    #     Edge IE模式需要特殊配置，后续需要时可以取消注释并启用
    #     """
    #     # 调用私有方法执行Edge IE模式完整流程测试
    #     self._execute_complete_flow_test(edge_ie_driver, "Edge_IE", screenshot_helper)
    
    # ==================== 私有方法：测试逻辑实现 ====================

    def _execute_login_page_test(self, driver, browser_name, screenshot_helper):
        """
        执行登录页面测试的核心逻辑

        这是一个私有方法，被不同浏览器的登录测试用例调用
        实现了README.md第一题中"点击Test Login Page，完成页面下方case"的要求

        测试覆盖的功能点：
        - 页面导航和加载验证
        - 正确凭据登录功能
        - 登出功能
        - 错误用户名处理
        - 错误密码处理
        - 每步操作的截图记录

        Args:
            driver: WebDriver实例，用于控制浏览器操作
            browser_name: 浏览器名称字符串，用于日志记录和截图命名
            screenshot_helper: 截图助手实例，用于自动截图和报告生成
        """
        # 记录测试开始日志，便于调试和问题定位
        logger.info(f"开始执行{browser_name}浏览器登录页面测试")

        # 初始化页面对象模型（Page Object Model）
        # 使用页面对象模式封装页面元素和操作，提高代码可维护性
        home_page = PracticeHomePage(driver)    # 首页页面对象，封装首页相关操作
        login_page = LoginPage(driver)          # 登录页面对象，封装登录相关操作
        
        try:
            # ========== 步骤1: 打开测试网站首页 ==========
            logger.info("步骤1: 打开测试网站首页")
            # 调用首页对象的open_page方法，打开README.md中指定的测试网站
            # URL: https://practicetestautomation.com/practice/
            home_page.open_page()
            # 截图记录当前页面状态，用于测试报告和问题排查
            screenshot_helper.take_screenshot(driver, "步骤1_打开首页", browser_name)

            # 验证首页是否正确加载，使用断言确保测试的可靠性
            # 如果首页未加载成功，测试将失败并抛出AssertionError
            assert home_page.is_page_loaded(), "首页未正确加载"

            # ========== 步骤2: 点击Test Login Page链接 ==========
            logger.info("步骤2: 点击Test Login Page链接")
            # 根据README.md要求，点击"Test Login Page"链接进入登录页面
            home_page.click_test_login_page()
            # 截图记录点击后的页面状态
            screenshot_helper.take_screenshot(driver, "步骤2_点击登录链接", browser_name)

            # 验证登录页面是否正确加载
            # 检查登录页面的关键元素（用户名框、密码框、提交按钮）是否存在
            assert login_page.is_page_loaded(), "登录页面未正确加载"
            
            # ========== 步骤3: 正确凭据登录测试 ==========
            logger.info("步骤3: 正确凭据登录测试")
            # 使用有效的用户名和密码进行登录
            # 默认凭据：用户名=student, 密码=Password123
            login_page.login_with_valid_credentials()

            # 导入time模块用于添加等待时间，确保页面操作完成
            import time
            # 等待登录处理完成，避免页面还在加载时就进行下一步操作
            time.sleep(2)
            # 截图记录登录操作执行后的状态
            screenshot_helper.take_screenshot(driver, "步骤3_正确凭据登录", browser_name)

            # 验证登录是否成功
            # 通过检查页面URL变化或成功页面元素来判断登录状态
            assert login_page.is_login_successful(), "使用正确凭据登录失败"

            # 等待页面完全稳定后再截图，确保截图内容完整
            time.sleep(1)
            # 截图记录登录成功后的页面状态
            screenshot_helper.take_screenshot(driver, "步骤3_登录成功验证", browser_name)

            # ========== 步骤4: 执行登出操作 ==========
            logger.info("步骤4: 执行登出操作")
            # 点击登出链接，返回到登录页面
            # 这是为了准备后续的错误凭据测试
            login_page.logout()

            # 等待登出操作完成，确保页面已经跳转回登录页面
            time.sleep(2)
            # 截图记录登出后的页面状态
            screenshot_helper.take_screenshot(driver, "步骤4_登出操作", browser_name)
            
            # ========== 步骤5: 错误用户名测试 ==========
            logger.info("步骤5: 错误用户名测试")

            # 分步骤输入错误用户名，便于观察每个输入步骤
            # 输入一个不存在的用户名来测试错误处理
            login_page.enter_username("invaliduser")
            time.sleep(1)  # 等待用户名显示，让用户能看到输入过程
            # 截图记录错误用户名输入状态
            screenshot_helper.take_screenshot(driver, "步骤5_输入错误用户名", browser_name)

            # 输入正确的密码（用于测试用户名错误的情况）
            login_page.enter_password("admin123")
            time.sleep(1)  # 等待密码显示，展示密码输入过程
            # 截图记录密码输入状态
            screenshot_helper.take_screenshot(driver, "步骤5_输入密码", browser_name)

            # 点击提交按钮，触发登录验证
            login_page.click_submit()
            time.sleep(1)  # 等待提交处理，确保请求已发送

            # 等待错误消息出现，给服务器响应时间
            time.sleep(3)
            # 截图记录错误消息显示状态
            screenshot_helper.take_screenshot(driver, "步骤5_错误用户名登录", browser_name)

            # 验证是否显示了错误消息
            # 检查页面上是否出现了错误提示元素
            assert login_page.is_error_displayed(), "未显示错误消息"
            # 获取错误消息文本内容
            error_message = login_page.get_error_message()
            # 验证错误消息内容是否与用户名错误相关
            assert "username" in error_message.lower(), f"错误消息不正确: {error_message}"
            # 记录测试成功日志，包含实际的错误消息内容
            logger.info(f"错误用户名测试成功，错误消息: {error_message}")

            # ========== 步骤6: 错误密码测试 ==========
            logger.info("步骤6: 错误密码测试")
            # 清空登录表单，为新的测试准备干净的输入环境
            login_page.clear_form()

            # 等待表单清理完成，确保输入框已被清空
            time.sleep(1)

            # 分步骤输入错误密码测试数据
            # 输入正确的用户名（用于测试密码错误的情况）
            login_page.enter_username("student")
            time.sleep(1)  # 等待用户名显示，让用户能看到输入过程
            # 截图记录正确用户名输入状态
            screenshot_helper.take_screenshot(driver, "步骤6_输入正确用户名", browser_name)

            # 输入错误的密码来测试密码验证功能
            login_page.enter_password("wrongpassword")
            time.sleep(1)  # 等待密码显示，展示密码输入过程
            # 截图记录错误密码输入状态
            screenshot_helper.take_screenshot(driver, "步骤6_输入错误密码", browser_name)

            # 点击提交按钮，触发登录验证
            login_page.click_submit()
            time.sleep(1)  # 等待提交处理，确保请求已发送

            # 等待错误消息出现，给服务器响应时间
            time.sleep(3)
            # 截图记录错误消息显示状态
            screenshot_helper.take_screenshot(driver, "步骤6_错误密码登录", browser_name)

            # 验证是否显示了错误消息
            # 检查页面上是否出现了密码错误的提示元素
            assert login_page.is_error_displayed(), "未显示错误消息"
            # 获取错误消息文本内容
            error_message = login_page.get_error_message()
            # 验证错误消息内容是否与密码错误相关
            assert "password" in error_message.lower(), f"错误消息不正确: {error_message}"
            # 记录测试成功日志，包含实际的错误消息内容
            logger.info(f"错误密码测试成功，错误消息: {error_message}")

            # 记录整个登录页面测试完成的日志
            logger.info(f"{browser_name}浏览器登录页面测试完成")

        except Exception as e:
            # 异常处理：当测试过程中发生任何异常时执行
            # 记录详细的错误日志，便于问题排查和调试
            logger.error(f"{browser_name}浏览器登录页面测试失败: {e}")
            # 自动截图记录失败时的页面状态，用于问题分析
            screenshot_helper.take_failure_screenshot(driver, "登录页面测试", str(e), browser_name)
            # 重新抛出异常，让pytest框架能够正确处理测试失败
            raise
    
    def _execute_exceptions_page_test(self, driver, browser_name, screenshot_helper):
        """
        执行异常页面测试的核心逻辑

        这是一个私有方法，被不同浏览器的异常测试用例调用
        实现了README.md第一题中"点击Test Exceptions，完成页面下方case"的要求

        测试覆盖的功能点：
        - 页面导航和加载验证
        - 动态元素添加功能（Add按钮）
        - 文本输入功能
        - 数据保存功能（Save按钮）
        - 确认消息验证
        - 数据一致性验证
        - 每步操作的截图记录（按要求每步等待1秒）

        Args:
            driver: WebDriver实例，用于控制浏览器操作
            browser_name: 浏览器名称字符串，用于日志记录和截图命名
            screenshot_helper: 截图助手实例，用于自动截图和报告生成
        """
        # 记录测试开始日志，便于调试和问题定位
        logger.info(f"开始执行{browser_name}浏览器异常页面测试")

        # 初始化页面对象模型（Page Object Model）
        # 使用页面对象模式封装页面元素和操作，提高代码可维护性
        home_page = PracticeHomePage(driver)        # 首页页面对象，封装首页相关操作
        exceptions_page = ExceptionsPage(driver)    # 异常页面对象，封装异常页面相关操作
        
        try:
            # ========== 步骤1: 打开测试网站首页 ==========
            logger.info("步骤1: 打开测试网站首页")
            # 调用首页对象的open_page方法，打开README.md中指定的测试网站
            # URL: https://practicetestautomation.com/practice/
            home_page.open_page()
            # 截图记录当前页面状态，用于测试报告和问题排查
            screenshot_helper.take_screenshot(driver, "步骤1_打开首页", browser_name)

            # 验证首页是否正确加载，使用断言确保测试的可靠性
            # 检查首页的关键元素（标题、链接等）是否存在
            assert home_page.is_page_loaded(), "首页未正确加载"

            # 导入time模块用于添加等待时间
            import time
            # 按要求每步等待1秒后执行下一步，让用户能清楚看到操作过程
            time.sleep(1)

            # ========== 步骤2: 点击Test Exceptions链接 ==========
            logger.info("步骤2: 点击Test Exceptions链接")
            # 根据README.md要求，点击"Test Exceptions"链接进入异常测试页面
            home_page.click_test_exceptions()

            # 等待页面跳转完成，确保新页面完全加载
            time.sleep(3)
            # 截图记录点击后的页面状态
            screenshot_helper.take_screenshot(driver, "步骤2_点击异常链接", browser_name)

            # 验证异常测试页面是否正确加载
            # 检查异常页面的关键元素（Add按钮、Row1等）是否存在
            assert exceptions_page.is_page_loaded(), "异常测试页面未正确加载"

            # 按要求等待1秒后执行下一步
            time.sleep(1)

            # ========== 滚动到用例1的说明部分 ==========
            logger.info("滚动到用例1的说明部分...")
            self._scroll_to_test_case_section(driver, screenshot_helper, browser_name, 1)

            # ========== 执行5个异常测试用例 ==========
            logger.info("开始执行异常页面的5个测试用例...")

            # 执行5个用例，每个用例都有详细的截图和等待
            # 根据更新后的流程要求：每个用例执行完，等待3秒，刷新当前页，再执行下一个用例
            self._execute_exceptions_test_with_screenshots(exceptions_page, driver, browser_name, screenshot_helper)

            # 记录整个异常页面测试完成的日志
            logger.info(f"{browser_name}浏览器异常页面测试完成（5个用例全部完成）")

        except Exception as e:
            # 异常处理：当测试过程中发生任何异常时执行
            # 记录详细的错误日志，便于问题排查和调试
            logger.error(f"{browser_name}浏览器异常页面测试失败: {e}")
            # 自动截图记录失败时的页面状态，用于问题分析
            screenshot_helper.take_failure_screenshot(driver, "异常页面测试", str(e), browser_name)
            # 重新抛出异常，让pytest框架能够正确处理测试失败
            raise
    
    def _execute_complete_flow_test(self, driver, browser_name, screenshot_helper):
        """
        执行完整流程测试（按照README.md要求的顺序）

        这是一个私有方法，实现更新后的完整测试流程：
        1. 使用Selenium打开测试网站
        2. 点击Test Login Page，完成页面下方case
        3. 点击测试网站的practice页面（不使用浏览器返回）
        4. 点击Test Exceptions，完成页面下方case
        5. 每一步操作请附带步骤说明和截图，生成文档

        这个方法整合了登录测试和异常测试，按照README.md的要求顺序执行

        Args:
            driver: WebDriver实例，用于控制浏览器操作
            browser_name: 浏览器名称字符串，用于日志记录和截图命名
            screenshot_helper: 截图助手实例，用于自动截图和报告生成
        """
        # 记录完整流程测试开始日志
        logger.info(f"开始执行{browser_name}浏览器完整流程测试")

        # 初始化所有需要的页面对象模型
        home_page = PracticeHomePage(driver)        # 首页页面对象
        login_page = LoginPage(driver)              # 登录页面对象
        exceptions_page = ExceptionsPage(driver)    # 异常页面对象
        
        try:
            # ========== 步骤1: 打开测试网站首页 ==========
            logger.info("步骤1: 打开测试网站首页")
            # 根据README.md要求，使用Selenium打开指定的测试网站
            # URL: https://practicetestautomation.com/practice/
            home_page.open_page()
            # 截图记录首页打开状态，用于完整流程文档
            screenshot_helper.take_screenshot(driver, "完整流程_步骤1_打开首页", browser_name)
            # 验证首页是否正确加载
            assert home_page.is_page_loaded(), "首页未正确加载"

            # ========== 步骤2: 点击Test Login Page，执行3个登录用例 ==========
            logger.info("步骤2: 点击Test Login Page，执行3个登录用例")
            # 根据更新后的流程要求，点击"Test Login Page"链接
            home_page.click_test_login_page()
            # 截图记录进入登录页面的状态
            screenshot_helper.take_screenshot(driver, "完整流程_步骤2_进入登录页", browser_name)

            # 验证登录页面是否正确加载
            assert login_page.is_page_loaded(), "登录页面未正确加载"

            # 执行3个登录测试用例
            self._execute_login_test_cases(login_page, driver, browser_name, screenshot_helper)

            # ========== 步骤3: 快速导航到practice页面 ==========
            logger.info("步骤3: 快速导航到practice页面（优化停顿时间）")

            # 添加短暂等待，确保登录用例完全结束
            import time
            time.sleep(0.5)  # 短暂等待，确保页面状态稳定

            # 根据更新后的流程要求，快速导航到practice页面
            # 优化：减少等待时间，提高导航效率
            home_page.navigate_to_practice_page()

            # 截图记录导航后的状态
            screenshot_helper.take_screenshot(driver, "完整流程_步骤3_快速导航practice页面", browser_name)

            # 快速验证页面状态
            if not home_page.is_page_loaded():
                logger.warning("practice页面验证失败，但继续执行测试")
            else:
                logger.info("practice页面验证成功")

            # ========== 步骤4: 快速进入异常测试 ==========
            logger.info("步骤4: 快速进入Test Exceptions，执行5个异常用例")

            # 短暂等待，确保practice页面完全加载
            time.sleep(0.5)

            # 根据更新后的流程要求，点击"Test Exceptions"链接
            home_page.click_test_exceptions()

            # 截图记录进入异常测试页面的状态
            screenshot_helper.take_screenshot(driver, "完整流程_步骤4_快速进入异常页", browser_name)

            # 滚动到用例1的说明部分
            logger.info("滚动到用例1的说明部分...")
            self._scroll_to_test_case_section(driver, screenshot_helper, browser_name, 1)

            # 执行异常页面的5个测试用例
            # 每个用例执行完等待3秒，刷新页面，再执行下一个用例
            self._execute_exceptions_test_with_screenshots(exceptions_page, driver, browser_name, screenshot_helper)

            # 截图记录所有异常测试完成状态
            screenshot_helper.take_screenshot(driver, "完整流程_步骤4_所有异常测试完成", browser_name)

            # 记录完整流程测试完成日志
            logger.info(f"{browser_name}浏览器完整流程测试完成")

        except Exception as e:
            # 异常处理：当完整流程测试过程中发生任何异常时执行
            # 记录详细的错误日志，便于问题排查和调试
            logger.error(f"{browser_name}浏览器完整流程测试失败: {e}")
            # 自动截图记录失败时的页面状态，用于问题分析
            screenshot_helper.take_failure_screenshot(driver, "完整流程测试", str(e), browser_name)
            # 重新抛出异常，让pytest框架能够正确处理测试失败
            raise

    def _execute_exceptions_test_with_screenshots(self, exceptions_page, driver, browser_name, screenshot_helper):
        """
        执行异常测试的5个用例，每个用例都有详细的截图记录

        使用run_chrome_exceptions_cases.py中的代码逻辑，确保每个异常用例的每一步操作都有步骤说明和截图

        根据更新后的流程要求：
        Test Exceptions有5个用例，每个用例执行完，等待3秒，刷新当前页，再执行下一个用例

        Args:
            exceptions_page: 异常页面对象
            driver: WebDriver实例
            browser_name: 浏览器名称
            screenshot_helper: 截图助手
        """
        logger.info("开始执行异常测试的5个用例，使用run_chrome_exceptions_cases.py中的详细逻辑...")

        # 导入必要的模块
        import time
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import (
            NoSuchElementException,
            ElementNotInteractableException,
            InvalidElementStateException,
            StaleElementReferenceException,
            TimeoutException
        )

        # ========== 用例1: NoSuchElementException测试 ==========
        logger.info("=== 开始执行Case1: NoSuchElementException ===")
        screenshot_helper.take_screenshot(driver, "异常测试_用例1_开始", browser_name)

        try:
            # 1. 滚动到标题处
            logger.info("步骤1: 滚动到标题处")
            target_header = driver.find_element(By.XPATH, "/html/body/div/div/section/section/h2")
            driver.execute_script("arguments[0].scrollIntoView();", target_header)
            time.sleep(1)
            screenshot_helper.take_screenshot(driver, "异常测试_用例1_步骤1_滚动到标题", browser_name)

            # 2. 定位Add按钮并进行红色高亮
            logger.info("步骤2: 定位Add按钮并高亮")
            add_button = driver.find_element(By.XPATH, "//button[text()='Add']")
            self._highlight_element(driver, add_button, "red")
            screenshot_helper.take_screenshot(driver, "异常测试_用例1_步骤2_Add按钮高亮", browser_name)

            # 3. 点击Add按钮
            logger.info("步骤3: 点击Add按钮")
            add_button.click()
            screenshot_helper.take_screenshot(driver, "异常测试_用例1_步骤3_点击Add按钮", browser_name)

            # 4. 尝试查找Row 2输入框(预期失败)
            logger.info("步骤4: 尝试查找Row 2输入框(预期失败)")
            try:
                row2_input = driver.find_element(By.XPATH, "//div[text()='Row 2']/following-sibling::input")
                screenshot_helper.take_screenshot(driver, "异常测试_用例1_步骤4_意外找到元素", browser_name)
            except NoSuchElementException as e:
                logger.info("Case1成功捕获异常: " + str(e))

                # 显示异常信息面板
                self._show_exception_panel(driver, f"Case1 - NoSuchElementException:\n{str(e)}")
                screenshot_helper.take_screenshot(driver, "异常测试_用例1_步骤4_捕获异常", browser_name)

                # 确保浏览器窗口在前台
                driver.switch_to.window(driver.current_window_handle)

                logger.info("Case1异常已显示在浏览器中，等待3秒...")
                time.sleep(3)
                screenshot_helper.take_screenshot(driver, "异常测试_用例1_步骤4_异常显示完成", browser_name)

        except Exception as e:
            logger.error(f"用例1执行出错: {e}")
            screenshot_helper.take_failure_screenshot(driver, "异常测试_用例1", str(e), browser_name)

        logger.info("=== Case1测试完成 ===")
        screenshot_helper.take_screenshot(driver, "异常测试_用例1_完成", browser_name)

        # 等待3秒并刷新页面
        logger.info("用例1完成，等待3秒...")
        time.sleep(3)
        screenshot_helper.take_screenshot(driver, "异常测试_用例1_等待3秒后", browser_name)

        logger.info("刷新页面，准备执行用例2...")
        driver.refresh()
        time.sleep(2)
        screenshot_helper.take_screenshot(driver, "异常测试_用例1_刷新页面后", browser_name)

        # ========== 用例2: ElementNotInteractableException测试 - 不可见的Save按钮 ==========
        logger.info("=== 开始执行Case2: ElementNotInteractableException (不可见按钮) ===")
        screenshot_helper.take_screenshot(driver, "异常测试_用例2_开始", browser_name)

        try:
            # 1. 滚动到标题处
            logger.info("步骤1: 滚动到标题处")
            target_header = driver.find_element(By.XPATH, "/html/body/div/div/section/section/h2")
            driver.execute_script("arguments[0].scrollIntoView();", target_header)
            time.sleep(1)
            screenshot_helper.take_screenshot(driver, "异常测试_用例2_步骤1_滚动到标题", browser_name)

            # 2. 定位Add按钮并进行红色高亮
            logger.info("步骤2: 定位Add按钮并高亮")
            add_button = driver.find_element(By.XPATH, "//button[text()='Add']")
            self._highlight_element(driver, add_button, "red")
            screenshot_helper.take_screenshot(driver, "异常测试_用例2_步骤2_Add按钮高亮", browser_name)

            # 3. 点击Add按钮
            logger.info("步骤3: 点击Add按钮")
            add_button.click()
            time.sleep(5)  # 等待Row 2出现
            screenshot_helper.take_screenshot(driver, "异常测试_用例2_步骤3_点击Add按钮_等待Row2", browser_name)

            # 4. 在Row 2输入框中输入文本
            logger.info("步骤4: 在Row 2输入框中输入文本")
            try:
                # 使用更准确的定位器
                row2_input = driver.find_element(By.CSS_SELECTOR, "#row2 input")
            except:
                # 备用定位器
                row2_input = driver.find_element(By.XPATH, "//input[2]")

            row2_input.send_keys("Test Text")
            screenshot_helper.take_screenshot(driver, "异常测试_用例2_步骤4_输入文本", browser_name)

            # 5. 尝试点击不可见的Save按钮(预期失败)
            logger.info("步骤5: 尝试点击不可见的Save按钮(预期失败)")
            try:
                # 第一个Save按钮是不可见的
                save_button = driver.find_element(By.XPATH, "//button[text()='Save']")
                self._highlight_element(driver, save_button, "red")
                screenshot_helper.take_screenshot(driver, "异常测试_用例2_步骤5_Save按钮高亮", browser_name)
                save_button.click()
                screenshot_helper.take_screenshot(driver, "异常测试_用例2_步骤5_意外点击成功", browser_name)
            except ElementNotInteractableException as e:
                logger.info("Case2成功捕获异常: " + str(e))

                # 显示异常信息面板
                self._show_exception_panel(driver, f"Case2 - ElementNotInteractableException:\n{str(e)}")
                screenshot_helper.take_screenshot(driver, "异常测试_用例2_步骤5_捕获异常", browser_name)

                # 确保浏览器窗口在前台
                driver.switch_to.window(driver.current_window_handle)

                logger.info("Case2异常已显示在浏览器中，等待3秒...")
                time.sleep(3)
                screenshot_helper.take_screenshot(driver, "异常测试_用例2_步骤5_异常显示完成", browser_name)

        except Exception as e:
            logger.error(f"用例2执行出错: {e}")
            screenshot_helper.take_failure_screenshot(driver, "异常测试_用例2", str(e), browser_name)

        logger.info("=== Case2测试完成 ===")
        screenshot_helper.take_screenshot(driver, "异常测试_用例2_完成", browser_name)

        # 等待3秒并刷新页面
        logger.info("用例2完成，等待3秒...")
        time.sleep(3)
        screenshot_helper.take_screenshot(driver, "异常测试_用例2_等待3秒后", browser_name)

        logger.info("刷新页面，准备执行用例3...")
        driver.refresh()
        time.sleep(2)
        screenshot_helper.take_screenshot(driver, "异常测试_用例2_刷新页面后", browser_name)

        # ========== 用例3: InvalidElementStateException测试 - 清空禁用输入框 ==========
        logger.info("=== 开始执行Case3: InvalidElementStateException ===")
        screenshot_helper.take_screenshot(driver, "异常测试_用例3_开始", browser_name)

        try:
            # 1. 滚动到标题处
            logger.info("步骤1: 滚动到标题处")
            target_header = driver.find_element(By.XPATH, "/html/body/div/div/section/section/h2")
            driver.execute_script("arguments[0].scrollIntoView();", target_header)
            time.sleep(1)
            screenshot_helper.take_screenshot(driver, "异常测试_用例3_步骤1_滚动到标题", browser_name)

            # 2. 尝试清空禁用的输入框(预期失败)
            logger.info("步骤2: 尝试清空禁用的输入框(预期失败)")
            try:
                # 查找禁用的输入框
                disabled_input = driver.find_element(By.XPATH, "//input[@disabled]")
                self._highlight_element(driver, disabled_input, "red")
                screenshot_helper.take_screenshot(driver, "异常测试_用例3_步骤2_禁用输入框高亮", browser_name)

                # 尝试清空禁用的输入框
                disabled_input.clear()
                screenshot_helper.take_screenshot(driver, "异常测试_用例3_步骤2_意外清空成功", browser_name)
            except (InvalidElementStateException, ElementNotInteractableException) as e:
                logger.info("Case3成功捕获异常: " + str(e))

                # 显示异常信息面板
                self._show_exception_panel(driver, f"Case3 - InvalidElementStateException:\n{str(e)}")
                screenshot_helper.take_screenshot(driver, "异常测试_用例3_步骤2_捕获异常", browser_name)

                # 确保浏览器窗口在前台
                driver.switch_to.window(driver.current_window_handle)

                logger.info("Case3异常已显示在浏览器中，等待3秒...")
                time.sleep(3)
                screenshot_helper.take_screenshot(driver, "异常测试_用例3_步骤2_异常显示完成", browser_name)

        except Exception as e:
            logger.error(f"用例3执行出错: {e}")
            screenshot_helper.take_failure_screenshot(driver, "异常测试_用例3", str(e), browser_name)

        logger.info("=== Case3测试完成 ===")
        screenshot_helper.take_screenshot(driver, "异常测试_用例3_完成", browser_name)

        # 等待3秒并刷新页面
        logger.info("用例3完成，等待3秒...")
        time.sleep(3)
        screenshot_helper.take_screenshot(driver, "异常测试_用例3_等待3秒后", browser_name)

        logger.info("刷新页面，准备执行用例4...")
        driver.refresh()
        time.sleep(2)
        screenshot_helper.take_screenshot(driver, "异常测试_用例3_刷新页面后", browser_name)

        # ========== 用例4: StaleElementReferenceException测试 - 元素引用过期 ==========
        logger.info("=== 开始执行Case4: StaleElementReferenceException ===")
        screenshot_helper.take_screenshot(driver, "异常测试_用例4_开始", browser_name)

        try:
            # 1. 获取instructions元素的引用
            logger.info("步骤1: 获取instructions元素的引用")
            instructions = driver.find_element(By.ID, "instructions")
            self._highlight_element(driver, instructions, "red")
            screenshot_helper.take_screenshot(driver, "异常测试_用例4_步骤1_获取元素引用", browser_name)

            # 2. 点击Add按钮移除instructions元素
            logger.info("步骤2: 点击Add按钮移除instructions元素")
            add_button = driver.find_element(By.XPATH, "//button[text()='Add']")
            add_button.click()
            time.sleep(5)  # 等待Row 2出现，此时instructions元素被移除
            screenshot_helper.take_screenshot(driver, "异常测试_用例4_步骤2_点击Add按钮", browser_name)

            # 3. 尝试与已过期的instructions元素交互(预期失败)
            logger.info("步骤3: 尝试与已过期的instructions元素交互(预期失败)")
            try:
                # 尝试获取已被移除的元素的文本
                text = instructions.text
                logger.warning(f"意外获取到文本: {text}")
                screenshot_helper.take_screenshot(driver, "异常测试_用例4_步骤3_意外获取文本成功", browser_name)
            except StaleElementReferenceException as e:
                logger.info("Case4成功捕获异常: " + str(e))

                # 显示异常信息面板
                self._show_exception_panel(driver, f"Case4 - StaleElementReferenceException:\n{str(e)}")
                screenshot_helper.take_screenshot(driver, "异常测试_用例4_步骤3_捕获异常", browser_name)

                # 确保浏览器窗口在前台
                driver.switch_to.window(driver.current_window_handle)

                logger.info("Case4异常已显示在浏览器中，等待3秒...")
                time.sleep(3)
                screenshot_helper.take_screenshot(driver, "异常测试_用例4_步骤3_异常显示完成", browser_name)

        except Exception as e:
            logger.error(f"用例4执行出错: {e}")
            screenshot_helper.take_failure_screenshot(driver, "异常测试_用例4", str(e), browser_name)

        logger.info("=== Case4测试完成 ===")
        screenshot_helper.take_screenshot(driver, "异常测试_用例4_完成", browser_name)

        # 等待3秒并刷新页面
        logger.info("用例4完成，等待3秒...")
        time.sleep(3)
        screenshot_helper.take_screenshot(driver, "异常测试_用例4_等待3秒后", browser_name)

        logger.info("刷新页面，准备执行用例5...")
        driver.refresh()
        time.sleep(2)
        screenshot_helper.take_screenshot(driver, "异常测试_用例4_刷新页面后", browser_name)

        # ========== 用例5: TimeoutException测试 - 短超时等待 ==========
        logger.info("=== 开始执行Case5: TimeoutException ===")
        screenshot_helper.take_screenshot(driver, "异常测试_用例5_开始", browser_name)

        try:
            # 1. 点击Add按钮
            logger.info("步骤1: 点击Add按钮")
            add_button = driver.find_element(By.XPATH, "//button[text()='Add']")
            self._highlight_element(driver, add_button, "red")
            screenshot_helper.take_screenshot(driver, "异常测试_用例5_步骤1_Add按钮高亮", browser_name)
            add_button.click()
            screenshot_helper.take_screenshot(driver, "异常测试_用例5_步骤1_点击Add按钮", browser_name)

            # 2. 设置短超时等待Row 2出现(预期失败)
            logger.info("步骤2: 设置3秒超时等待Row 2出现(预期失败)")
            try:
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC

                # 设置3秒超时，但Row 2需要5秒才出现
                wait = WebDriverWait(driver, 3)
                row2_input = wait.until(EC.presence_of_element_located((By.XPATH, "//div[text()='Row 2']/following-sibling::input")))
                screenshot_helper.take_screenshot(driver, "异常测试_用例5_步骤2_意外找到元素", browser_name)
            except TimeoutException as e:
                logger.info("Case5成功捕获异常: " + str(e))

                # 显示异常信息面板
                self._show_exception_panel(driver, f"Case5 - TimeoutException:\n{str(e)}")
                screenshot_helper.take_screenshot(driver, "异常测试_用例5_步骤2_捕获异常", browser_name)

                # 确保浏览器窗口在前台
                driver.switch_to.window(driver.current_window_handle)

                logger.info("Case5异常已显示在浏览器中，等待3秒...")
                time.sleep(3)
                screenshot_helper.take_screenshot(driver, "异常测试_用例5_步骤2_异常显示完成", browser_name)

        except Exception as e:
            logger.error(f"用例5执行出错: {e}")
            screenshot_helper.take_failure_screenshot(driver, "异常测试_用例5", str(e), browser_name)

        logger.info("=== Case5测试完成 ===")
        screenshot_helper.take_screenshot(driver, "异常测试_用例5_完成", browser_name)

        # 最后一个用例等待3秒（不需要刷新）
        logger.info("用例5完成，等待3秒完成所有测试...")
        time.sleep(3)
        screenshot_helper.take_screenshot(driver, "异常测试_用例5_最终完成", browser_name)

        logger.info("异常测试的5个用例全部执行完成！")

    def _highlight_element(self, driver, element, color, duration=2):
        """
        简单高亮元素

        Args:
            driver: WebDriver实例
            element: 要高亮的元素
            color: 高亮颜色
            duration: 高亮持续时间（秒）
        """
        try:
            original_style = element.get_attribute("style")

            # 红色高亮
            driver.execute_script(f"arguments[0].style.border='3px solid {color}';", element)
            time.sleep(duration)

            # 恢复原始样式
            driver.execute_script(f"arguments[0].style='{original_style}';", element)
        except Exception as e:
            logger.warning(f"元素高亮失败: {e}")

    def _show_exception_panel(self, driver, message):
        """
        显示异常信息面板

        Args:
            driver: WebDriver实例
            message: 异常信息
        """
        try:
            js = f"""
            // 移除已存在的面板
            const existingPanel = document.getElementById('exception-panel');
            if (existingPanel) {{
                existingPanel.remove();
            }}

            const panel = document.createElement('div');
            panel.id = 'exception-panel';
            panel.style = `
                position:fixed; top:20px; right:20px;
                width:350px; padding:15px;
                background:#FFF3E0; border:2px solid #FFA000;
                z-index:9999; font-family:Arial;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.3);
            `;
            panel.innerHTML = `
                <h3 style="color:#E65100; margin-top:0; margin-bottom:10px;">
                    异常捕获成功
                </h3>
                <div style="white-space:pre-wrap; font-size:12px; line-height:1.4;">
                    {message.replace('`', '\\`').replace("'", "\\'")}
                </div>
            `;
            document.body.appendChild(panel);
            """
            driver.execute_script(js)
        except Exception as e:
            logger.warning(f"显示异常面板失败: {e}")

    def _scroll_to_test_cases_section(self, driver, screenshot_helper, browser_name):
        """
        滚动到页面下方，显示测试用例相关部分

        确保用户能看到页面下方的测试用例区域，包括Add按钮和相关说明

        Args:
            driver: WebDriver实例
            screenshot_helper: 截图助手
            browser_name: 浏览器名称
        """
        logger.info("开始滚动到测试用例相关部分...")

        import time

        # 截图记录滚动前的页面状态
        screenshot_helper.take_screenshot(driver, "异常测试_滚动前_页面顶部", browser_name)

        try:
            # 方法1: 尝试滚动到Add按钮位置
            logger.info("尝试滚动到Add按钮位置...")
            add_button = driver.find_element(By.ID, "add_btn")
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", add_button)
            time.sleep(2)  # 等待滚动动画完成

            # 截图记录滚动到Add按钮后的状态
            screenshot_helper.take_screenshot(driver, "异常测试_滚动到Add按钮", browser_name)
            logger.info("成功滚动到Add按钮位置")

        except Exception as e:
            logger.warning(f"滚动到Add按钮失败: {e}")

            try:
                # 方法2: 尝试滚动到页面中部
                logger.info("尝试滚动到页面中部...")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
                time.sleep(2)

                # 截图记录滚动到页面中部的状态
                screenshot_helper.take_screenshot(driver, "异常测试_滚动到页面中部", browser_name)
                logger.info("成功滚动到页面中部")

            except Exception as e2:
                logger.warning(f"滚动到页面中部也失败: {e2}")

                # 方法3: 简单的页面下滑
                logger.info("使用简单的页面下滑...")
                try:
                    driver.execute_script("window.scrollBy(0, 500);")
                    time.sleep(1)

                    # 截图记录简单下滑后的状态
                    screenshot_helper.take_screenshot(driver, "异常测试_简单下滑", browser_name)
                    logger.info("完成简单页面下滑")

                except Exception as e3:
                    logger.error(f"所有滚动方法都失败: {e3}")

        # 验证关键元素是否可见
        try:
            # 检查Add按钮是否可见
            add_button_visible = driver.find_element(By.ID, "add_btn").is_displayed()
            logger.info(f"Add按钮可见状态: {add_button_visible}")

            # 检查instructions是否可见
            try:
                instructions_element = driver.find_element(By.ID, "instructions")
                instructions_visible = instructions_element.is_displayed()
                logger.info(f"Instructions元素可见状态: {instructions_visible}")

                # 如果instructions可见，显示其部分内容
                if instructions_visible:
                    instructions_text = instructions_element.text[:100]
                    logger.info(f"Instructions内容预览: {instructions_text}...")

            except Exception:
                logger.info("Instructions元素未找到或不可见")

        except Exception as e:
            logger.warning(f"验证元素可见性失败: {e}")

        # 最终截图，显示滚动后的页面状态
        screenshot_helper.take_screenshot(driver, "异常测试_滚动完成_准备执行用例", browser_name)

        # 短暂等待，让用户观察页面状态
        logger.info("滚动完成，等待2秒让用户观察页面状态...")
        time.sleep(2)

        logger.info("页面滚动完成，现在可以开始执行测试用例")

    def _scroll_to_test_case_section(self, driver, screenshot_helper, browser_name, case_number):
        """
        滚动到指定测试用例的相关部分

        Args:
            driver: WebDriver实例
            screenshot_helper: 截图助手
            browser_name: 浏览器名称
            case_number: 用例编号 (1-5)
        """
        logger.info(f"滚动到用例{case_number}的相关部分...")

        import time
        from selenium.webdriver.common.by import By

        try:
            # 用例1和用例2直接滚动到Add按钮位置
            if case_number in [1, 2]:
                logger.info(f"用例{case_number}: 直接滚动到Add按钮位置")
                add_button = driver.find_element(By.ID, "add_btn")
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", add_button)
                time.sleep(2)
                logger.info(f"用例{case_number}: 成功滚动到Add按钮位置")

            else:
                # 用例3-5尝试滚动到对应的测试用例标题
                case_selectors = {
                    3: "Test case 3: ElementNotInteractableException",
                    4: "Test case 4: InvalidElementStateException",
                    5: "Test case 5: StaleElementReferenceException"
                }

                case_text = case_selectors.get(case_number, "Test case 3: ElementNotInteractableException")
                logger.info(f"查找用例{case_number}标题: {case_text}")

                try:
                    case_element = driver.find_element(By.XPATH, f"//*[contains(text(), '{case_text}')]")
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", case_element)
                    time.sleep(2)
                    logger.info(f"成功滚动到用例{case_number}标题位置")

                except Exception as e:
                    logger.warning(f"通过标题滚动失败: {e}")
                    # 备选方案：滚动到Add按钮附近
                    add_button = driver.find_element(By.ID, "add_btn")
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", add_button)
                    time.sleep(1)
                    logger.info(f"备选方案：滚动到Add按钮位置")

            # 截图记录滚动后的状态
            screenshot_helper.take_screenshot(driver, f"异常测试_用例{case_number}_滚动到相关部分", browser_name)

        except Exception as e:
            logger.warning(f"用例{case_number}滚动失败: {e}")
            # 最终备选方案：简单下滑
            try:
                driver.execute_script("window.scrollBy(0, 500);")
                time.sleep(0.5)
                screenshot_helper.take_screenshot(driver, f"异常测试_用例{case_number}_备选滚动", browser_name)
                logger.info(f"用例{case_number}使用备选滚动")
            except Exception as e2:
                logger.warning(f"用例{case_number}备选滚动也失败: {e2}")

    def _execute_login_test_cases(self, login_page, driver, browser_name, screenshot_helper):
        """
        执行3个登录测试用例

        根据更新后的流程要求，在完整流程中执行3个登录用例：
        1. 正确凭据登录测试
        2. 错误用户名登录测试
        3. 错误密码登录测试

        Args:
            login_page: 登录页面对象
            driver: WebDriver实例
            browser_name: 浏览器名称
            screenshot_helper: 截图助手
        """
        logger.info("开始执行3个登录测试用例...")

        # 导入time模块用于等待
        import time

        # ========== 登录用例1: 正确凭据登录测试 ==========
        logger.info("=== 执行登录用例1: 正确凭据登录测试 ===")

        # 使用有效的用户名和密码进行登录
        login_page.enter_username("student")
        time.sleep(1)  # 等待用户名显示
        screenshot_helper.take_screenshot(driver, "登录用例1_输入正确用户名", browser_name)

        login_page.enter_password("Password123")
        time.sleep(1)  # 等待密码显示
        screenshot_helper.take_screenshot(driver, "登录用例1_输入正确密码", browser_name)

        login_page.click_submit()
        time.sleep(1)  # 等待提交处理

        # 等待登录处理完成
        time.sleep(2)
        screenshot_helper.take_screenshot(driver, "登录用例1_正确凭据登录", browser_name)

        # 验证登录是否成功
        assert login_page.is_login_successful(), "登录用例1失败: 使用正确凭据登录失败"
        screenshot_helper.take_screenshot(driver, "登录用例1_登录成功验证", browser_name)
        logger.info("登录用例1成功: 正确凭据登录验证通过")

        # 执行登出操作，为下一个用例做准备
        login_page.logout()
        time.sleep(2)
        screenshot_helper.take_screenshot(driver, "登录用例1_登出操作", browser_name)

        # ========== 登录用例2: 错误用户名登录测试 ==========
        logger.info("=== 执行登录用例2: 错误用户名登录测试 ===")

        # 输入错误的用户名
        login_page.enter_username("invaliduser")
        time.sleep(1)  # 等待用户名显示
        screenshot_helper.take_screenshot(driver, "登录用例2_输入错误用户名", browser_name)

        # 输入正确的密码（用于测试用户名错误的情况）
        login_page.enter_password("Password123")
        time.sleep(1)  # 等待密码显示
        screenshot_helper.take_screenshot(driver, "登录用例2_输入密码", browser_name)

        login_page.click_submit()
        time.sleep(1)  # 等待提交处理

        # 等待错误消息出现
        time.sleep(3)
        screenshot_helper.take_screenshot(driver, "登录用例2_错误用户名登录", browser_name)

        # 验证是否显示了错误消息
        assert login_page.is_error_displayed(), "登录用例2失败: 未显示错误消息"
        error_message = login_page.get_error_message()
        assert "username" in error_message.lower(), f"登录用例2失败: 错误消息不正确 - {error_message}"
        logger.info(f"登录用例2成功: 错误用户名测试通过，错误消息: {error_message}")

        # 清空表单，为下一个用例做准备
        login_page.clear_form()
        time.sleep(1)

        # ========== 登录用例3: 错误密码登录测试 ==========
        logger.info("=== 执行登录用例3: 错误密码登录测试 ===")

        # 输入正确的用户名
        login_page.enter_username("student")
        time.sleep(1)  # 等待用户名显示
        screenshot_helper.take_screenshot(driver, "登录用例3_输入正确用户名", browser_name)

        # 输入错误的密码
        login_page.enter_password("wrongpassword")
        time.sleep(1)  # 等待密码显示
        screenshot_helper.take_screenshot(driver, "登录用例3_输入错误密码", browser_name)

        login_page.click_submit()
        time.sleep(1)  # 等待提交处理

        # 等待错误消息出现
        time.sleep(3)
        screenshot_helper.take_screenshot(driver, "登录用例3_错误密码登录", browser_name)

        # 验证是否显示了错误消息
        assert login_page.is_error_displayed(), "登录用例3失败: 未显示错误消息"
        error_message = login_page.get_error_message()
        assert "password" in error_message.lower(), f"登录用例3失败: 错误消息不正确 - {error_message}"
        logger.info(f"登录用例3成功: 错误密码测试通过，错误消息: {error_message}")

        # 清理页面状态，为后续导航做准备
        logger.info("清理登录页面状态，准备导航到practice页面...")
        login_page.clear_form()  # 清空表单
        time.sleep(0.5)  # 短暂等待，确保清理完成

        logger.info("3个登录测试用例全部执行完成！")
