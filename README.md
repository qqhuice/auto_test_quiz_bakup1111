# Auto Test Quiz - Python Selenium 自动化测试项目

## 📋 项目概述

这是一个基于Python的Web自动化测试项目，使用Selenium WebDriver实现了完整的浏览器自动化测试框架。项目支持Chrome和Edge浏览器，包含登录功能测试、异常处理测试和BDD行为驱动测试。

### 🎯 主要功能

- ✅ **多浏览器支持**: Chrome 和 Microsoft Edge
- ✅ **完整的登录测试**: 正确凭据、错误用户名、错误密码
- ✅ **异常处理测试**: NoSuchElement、ElementNotInteractable、Timeout等
- ✅ **BDD行为驱动测试**: 基于Behave框架的Gherkin语法
- ✅ **详细的HTML报告**: 包含截图、步骤说明和测试状态
- ✅ **自动截图功能**: 每个测试步骤都有对应截图
- ✅ **日志记录**: 完整的测试执行日志

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- Chrome 浏览器 (最新版本)
- Microsoft Edge 浏览器 (最新版本)
- Git (用于克隆项目)

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/qqhuice/auto_test_quiz.git
cd auto_test_quiz
```

2. **创建虚拟环境并安装依赖**
```bash
# Windows
python -m venv venv
venv\Scripts\activate
pip install -r config/requirements.txt

# Linux/Mac
python -m venv venv
source venv/bin/activate
pip install -r config/requirements.txt
```

3. **验证安装并运行测试**
```bash
# 查看帮助
python run_all_tests.py --help

# 运行所有测试
python run_all_tests.py
```

> **💡 提示**: 项目已配置完整的依赖环境，按照上述步骤即可直接运行，无需额外配置。

## 📖 使用指南

### 🔧 执行测试

#### 1. Chrome浏览器测试
```bash
# 执行完整的Chrome测试流程
python run_chrome_tests.py
```

#### 2. Edge浏览器测试
```bash
# 执行完整的Edge测试流程
python run_edge_tests.py
```

#### 3. BDD行为驱动测试
```bash
# 执行BDD测试
python run_bdd_tests.py

# 或使用behave命令（需要在虚拟环境中）
behave features/
```

#### 4. 执行所有测试
```bash
# 一键执行所有测试（Chrome + Edge + BDD）
python run_all_tests.py
```

### 📊 查看测试结果

#### 1. HTML测试报告
测试执行完成后，会在 `reports/` 目录下生成详细的HTML报告：

```
reports/
├── Chrome_Detailed_Test_Report_YYYYMMDD_HHMMSS.html  # Chrome测试报告
├── Edge_Detailed_Test_Report_YYYYMMDD_HHMMSS.html    # Edge测试报告
└── test_report_YYYYMMDD_HHMMSS.html                  # BDD测试报告
```

**报告内容包括**:
- 📋 测试用例详细信息
- 📸 每个步骤的截图
- ✅ 测试状态和结果
- 🔧 详细的测试步骤说明
- ⚠️ 错误信息和异常处理

#### 2. 截图文件
所有测试截图保存在 `screenshots/` 目录下：

```
screenshots/
├── chrome_tests_YYYYMMDD_HHMMSS/     # Chrome测试截图
├── edge_tests_YYYYMMDD_HHMMSS/       # Edge测试截图
└── bdd_tests_YYYYMMDD_HHMMSS/        # BDD测试截图
```

#### 3. 日志文件
详细的执行日志保存在 `logs/` 目录下，便于问题排查和调试。

## 🏗️ 项目结构

```
auto_test_quiz/
├── 📁 config/                    # 配置文件
│   ├── config.yaml              # 主配置文件
│   ├── requirements.txt         # Python依赖
│   └── pytest.ini              # Pytest配置
├── 📁 pages/                     # 页面对象模型
│   ├── base_page.py             # 基础页面类
│   ├── login_page.py            # 登录页面
│   ├── exceptions_page.py       # 异常测试页面
│   └── orangehrm_*.py           # OrangeHRM相关页面
├── 📁 tests/                     # 测试用例
│   ├── test_selenium_basic.py   # 基础Selenium测试
│   └── conftest.py              # Pytest配置
├── 📁 features/                  # BDD特性文件
│   ├── employee_claims.feature  # 员工申请特性
│   ├── environment.py           # BDD环境配置
│   └── steps/                   # 步骤定义
├── 📁 utils/                     # 工具类
│   ├── driver_manager.py        # 浏览器驱动管理
│   ├── screenshot_helper.py     # 截图工具
│   └── config.py                # 配置管理
├── 📁 reports/                   # 测试报告
├── 📁 screenshots/               # 测试截图
├── 📁 logs/                      # 日志文件
├── run_chrome_tests.py          # Chrome测试执行器
├── run_edge_tests.py            # Edge测试执行器
├── run_bdd_tests.py             # BDD测试执行器
├── run_all_tests.py             # 全量测试执行器
└── README.md                    # 项目说明文档
```

## 🔧 API接口调用

### 1. 作为Python模块调用

```python
# 导入测试运行器
from run_chrome_tests import ChromeTestRunner
from run_edge_tests import EdgeTestRunner

# 执行Chrome测试
chrome_runner = ChromeTestRunner()
chrome_result = chrome_runner.run_tests()
chrome_report = chrome_runner.generate_detailed_test_report(chrome_result)

# 执行Edge测试
edge_runner = EdgeTestRunner()
edge_result = edge_runner.run_tests()
edge_runner._generate_detailed_report()  # Edge使用内部方法生成报告

# 执行BDD测试
import subprocess
bdd_result = subprocess.run(['python', 'run_bdd_tests.py'], capture_output=True)
```

### 2. 命令行接口

```bash
# 直接执行脚本（推荐方式）
python run_chrome_tests.py
python run_edge_tests.py
python run_bdd_tests.py
python run_all_tests.py
```

### 3. 集成到CI/CD流水线

```yaml
# GitHub Actions 示例
name: Automated Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.8'
    - name: Install dependencies
      run: pip install -r config/requirements.txt
    - name: Run tests
      run: python run_all_tests.py
    - name: Upload reports
      uses: actions/upload-artifact@v2
      with:
        name: test-reports
        path: reports/
```

## 📝 测试用例详情

### 🔐 登录功能测试 (TC001-TC003)

| 测试用例 | 描述 | 预期结果 |
|---------|------|----------|
| **TC001** | 正确凭据登录测试 | 成功登录并显示欢迎页面 |
| **TC002** | 错误用户名登录测试 | 显示"Your username is invalid!"错误信息 |
| **TC003** | 错误密码登录测试 | 显示"Your password is invalid!"错误信息 |

### ⚠️ 异常处理测试 (TC004-TC008)

| 测试用例 | 异常类型 | 测试场景 |
|---------|----------|----------|
| **TC004** | `NoSuchElementException` | 查找不存在的页面元素 |
| **TC005** | `ElementNotInteractableException` | 与不可交互元素进行操作 |
| **TC006** | `InvalidElementStateException` | 清空禁用状态的输入框 |
| **TC007** | `StaleElementReferenceException` | 使用已失效的元素引用 |
| **TC008** | `TimeoutException` | 等待元素超时 |

### 🏢 BDD员工申请测试

基于Gherkin语法的行为驱动测试，涵盖：
- 员工申请创建流程
- 费用添加和验证
- 数据一致性检查
- 页面导航测试

## ⚙️ 配置选项

### 浏览器配置

在 `config/config.yaml` 中可以配置：

```yaml
browsers:
  chrome:
    headless: false          # 是否无头模式
    window_size: "1920,1080" # 窗口大小
    timeout: 10              # 默认等待时间
  edge:
    headless: false
    window_size: "1920,1080"
    timeout: 10

test_urls:
  practice_site: "https://practicetestautomation.com/practice/"
  orangehrm_site: "https://opensource-demo.orangehrmlive.com/"

screenshots:
  enabled: true              # 是否启用截图
  on_failure: true          # 失败时截图
  quality: 90               # 截图质量
```

### 日志配置

```yaml
logging:
  level: "INFO"             # 日志级别
  format: "%(asctime)s | %(levelname)s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
  file_enabled: true        # 是否保存到文件
```

## 🔍 故障排除

### 常见问题

#### 1. 浏览器驱动问题
```bash
# 错误: WebDriver executable needs to be in PATH
# 解决: 项目会自动下载和管理驱动，确保网络连接正常
```

#### 2. 元素定位失败
```bash
# 错误: NoSuchElementException
# 解决: 检查页面加载是否完成，增加等待时间
```

#### 3. 权限问题
```bash
# 错误: Permission denied
# 解决: 确保有写入reports和screenshots目录的权限
```

### 调试模式

启用详细日志进行调试：

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 或在配置文件中设置
# logging.level: "DEBUG"
```

## 📈 性能优化

### 并行执行

```bash
# 使用pytest并行执行（在虚拟环境中）
pip install pytest-xdist
pytest -n auto tests/
```

### 无头模式

```yaml
# 在config.yaml中启用无头模式以提高执行速度
browsers:
  chrome:
    headless: true
  edge:
    headless: true
```

## 🤝 贡献指南

### 开发环境设置

1. **Fork项目并克隆**
```bash
git clone https://github.com/your-username/auto_test_quiz.git
cd auto_test_quiz
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

3. **安装开发依赖**
```bash
pip install -r config/requirements.txt
pip install pytest-cov black flake8  # 开发工具
```

### 代码规范

- 使用 **Black** 进行代码格式化
- 使用 **Flake8** 进行代码检查
- 遵循 **PEP 8** 编码规范
- 添加适当的注释和文档字符串

```bash
# 代码格式化
black .

# 代码检查
flake8 .

# 运行测试覆盖率
pytest --cov=. tests/
```

### 提交规范

```bash
# 提交信息格式
git commit -m "类型(范围): 简短描述

详细描述（可选）

关闭的Issue: #123"

# 示例
git commit -m "feat(login): 添加记住密码功能

- 增加记住密码复选框
- 实现本地存储功能
- 添加相关测试用例

关闭的Issue: #45"
```

## 📋 更新日志

### v1.0.0 (2025-09-13)
- ✅ 完成Chrome和Edge浏览器测试
- ✅ 实现完整的登录功能测试
- ✅ 添加异常处理测试用例
- ✅ 集成BDD行为驱动测试
- ✅ 生成详细的HTML测试报告
- ✅ 实现自动截图功能

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可证。

## 📞 联系信息

- **项目维护者**: qqhuice
- **GitHub**: [https://github.com/qqhuice/auto_test_quiz](https://github.com/qqhuice/auto_test_quiz)
- **问题反馈**: [GitHub Issues](https://github.com/qqhuice/auto_test_quiz/issues)

## 🙏 致谢

感谢以下开源项目的支持：

- [Selenium](https://selenium.dev/) - Web自动化测试框架
- [Pytest](https://pytest.org/) - Python测试框架
- [Behave](https://behave.readthedocs.io/) - BDD测试框架
- [Loguru](https://loguru.readthedocs.io/) - 日志记录库

---

## 📚 附录

### 原始任务要求

> 本项目基于以下原始任务要求实现：

#### 1. 基础验证(Selenium)
使用Selenium打开[测试网站](https://practicetestautomation.com/practice/)
- 点击**Test Login Page**，完成页面下方case
- 返回并点击**Test Exceptions**，完成页面下方case
- 每步操作附带步骤说明和截图

#### 2. 表单验证(BDD)
基于BDD形式实现[OrangeHRM网站](https://opensource-demo.orangehrmlive.com/)的员工申请流程测试
- 完成Employee Claims的Assign Claims记录创建
- 验证数据一致性和成功提示信息
- 生成包含截图和操作步骤的HTML测试报告

**项目已完全实现上述要求，并在此基础上进行了功能扩展和优化。**

---

*最后更新时间: 2025-09-13*
