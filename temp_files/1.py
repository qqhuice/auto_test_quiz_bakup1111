import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

class TestExceptions(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://practicetestautomation.com/practice-test-exceptions/")
        self.driver.maximize_window()
        self.driver.implicitly_wait(0)  # 禁用隐式等待确保立即查找元素
        # 将滚动代码移至setup方法
        target_header = self.driver.find_element(
            By.XPATH, "/html/body/div/div/section/section/h2")
        self.driver.execute_script("arguments[0].scrollIntoView();", target_header)
        time.sleep(1)  # 确保滚动完成

    def test_no_such_element_exception(self):
        # 步骤1: 点击Add按钮
        add_button = self.driver.find_element(By.XPATH, "//button[text()='Add']")
        self._highlight_element(add_button, "red")
        time.sleep(1)
        add_button.click()

        # 2. 直接尝试定位Row2输入框（不添加等待）
        try:
            self.driver.find_element(
                By.XPATH, "//div[text()='Row 2']/following-sibling::input")
        except NoSuchElementException as e:
            self._show_exception_panel(
                f"捕获到NoSuchElementException:\n{str(e)}\n"
                "符合预期行为：Row 2需要5秒加载时间")
            time.sleep(5)  # 错误显示停留5秒

    def _highlight_element(self, element, color, duration=1, flash_count=1):
        """动态高亮元素"""
        original_style = element.get_attribute("style")
        for _ in range(flash_count):
            self.driver.execute_script(
                f"arguments[0].style.border='3px solid {color}';"
                "arguments[0].style.transition='all 0.3s';", element)
            time.sleep(0.2)
            self.driver.execute_script(
                f"arguments[0].style.border='3px dashed {color}';", element)
            time.sleep(0.2)
        time.sleep(duration)
        self.driver.execute_script(f"arguments[0].style='{original_style}'", element)

    def _show_exception_panel(self, message):
        """专用异常显示面板"""
        js = f"""
        const panel = document.createElement('div');
        panel.style = `
            position:fixed; top:20px; right:20px;
            width:300px; padding:15px;
            background:#FFF3E0; border:2px solid #FFA000;
            z-index:9999; font-family:Arial;
        `;
        panel.innerHTML = `
            <h3 style="color:#E65100; margin-top:0;">
                  异常捕获
            </h3>
            <div style="white-space:pre-wrap;">
                {message.replace('`', '\\`')}
            </div>
        `;
        document.body.appendChild(panel);
        """
        self.driver.execute_script(js)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
