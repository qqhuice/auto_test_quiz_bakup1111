# Python Selenium 项目使用指南

## 📋 项目概述

这是一个基于Python和Selenium的自动化测试项目，支持多种测试框架和模式：

- **传统pytest测试**
- **BDD Cucumber测试** (使用behave)
- **页面对象模式** (Page Object Model)
- **多浏览器支持** (Chrome, Firefox, Edge)
- **截图和报告生成**

## 🚀 快速开始

### 1. 环境准备

```bash
# 安装依赖
pip install -r requirements.txt

# 确保浏览器驱动已安装
# ChromeDriver, GeckoDriver, EdgeDriver
```

### 2. 运行测试

```bash
# 运行基础功能测试
python run_tests.py --mode basic

# 运行所有测试
python run_tests.py --mode all

# 运行BDD测试
python run_tests.py --mode bdd

# 生成测试报告
python run_tests.py --mode report
```

### 3. 使用批处理脚本 (Windows)

```cmd
# 运行基础测试
run_tests.bat basic

# 运行所有测试
run_tests.bat all

# 运行BDD测试
run_tests.bat bdd
```

## 📁 项目结构

```
├── config/                 # 配置文件
│   ├── config.yaml        # 主配置文件
│   └── config_manager.py  # 配置管理器
├── pages/                  # 页面对象
│   ├── base_page.py       # 基础页面类
│   ├── orangehrm_*.py     # OrangeHRM页面对象
│   └── exceptions_page.py # 异常演示页面
├── tests/                  # 测试文件
│   ├── conftest.py        # pytest配置
│   └── test_*.py          # 测试用例
├── features/               # BDD特性文件
│   ├── *.feature          # Gherkin特性文件
│   └── steps/             # 步骤定义
├── utils/                  # 工具类
│   ├── driver_manager.py  # 浏览器驱动管理
│   ├── screenshot_utils.py # 截图工具
│   └── report_manager.py  # 报告管理
├── reports/                # 测试报告
├── screenshots/            # 截图文件
├── run_tests.py           # Python运行脚本
├── run_tests.bat          # Windows批处理脚本
├── run_bdd_tests.py       # BDD测试运行脚本
└── pytest.ini            # pytest配置
```

## 🔧 配置说明

### config.yaml 主要配置项

```yaml
browser:
  default: chrome
  headless: false
  window_size: "1920,1080"

timeouts:
  implicit_wait: 10
  explicit_wait: 20
  page_load: 30

urls:
  orangehrm: "https://opensource-demo.orangehrmlive.com"
  exceptions_demo: "file:///path/to/exceptions_demo.html"
```

## 📊 测试报告

项目支持多种报告格式：

- **HTML报告** (pytest-html)
- **JSON报告** (BDD测试)
- **截图报告** (自动截图)
- **控制台输出** (实时日志)

## 🎯 最佳实践

1. **页面对象模式**：所有页面元素和操作封装在页面类中
2. **等待策略**：使用显式等待而非固定延时
3. **错误处理**：完善的异常处理和日志记录
4. **截图机制**：测试失败时自动截图
5. **配置管理**：统一的配置文件管理

## 🐛 故障排除

### 常见问题

1. **浏览器驱动问题**
   - 确保驱动版本与浏览器版本匹配
   - 检查PATH环境变量

2. **元素定位失败**
   - 检查页面加载状态
   - 使用显式等待
   - 验证定位器准确性

3. **网络超时**
   - 调整超时配置
   - 检查网络连接
   - 使用本地测试页面

## 📞 技术支持

如有问题，请查看：
- 项目README.md
- 测试报告和日志
- 截图文件

---

*最后更新：2025-09-03*
