# 🚀 快速开始指南

## 📋 5分钟快速体验

### 1. 环境检查
```bash
# 检查Python版本（需要3.8+）
python --version

# 检查项目结构
python demo_api_usage.py
```

### 2. 安装依赖
```bash
pip install -r config/requirements.txt
```

### 3. 运行测试

#### 🔥 一键运行所有测试
```bash
python run_all_tests.py
```

#### 🌐 单独运行浏览器测试
```bash
# Chrome浏览器测试
python run_chrome_tests.py

# Edge浏览器测试  
python run_edge_tests.py

# BDD行为驱动测试
python run_bdd_tests.py
```

### 4. 查看结果

#### 📊 HTML测试报告
```bash
# 报告位置
reports/Chrome_Detailed_Test_Report_YYYYMMDD_HHMMSS.html
reports/Edge_Detailed_Test_Report_YYYYMMDD_HHMMSS.html
```

#### 📸 测试截图
```bash
# 截图位置
screenshots/chrome_tests_YYYYMMDD_HHMMSS/
screenshots/edge_tests_YYYYMMDD_HHMMSS/
```

## 🎯 测试内容概览

### ✅ 登录功能测试
- TC001: 正确凭据登录
- TC002: 错误用户名登录  
- TC003: 错误密码登录

### ⚠️ 异常处理测试
- TC004: NoSuchElementException
- TC005: ElementNotInteractableException
- TC006: InvalidElementStateException
- TC007: StaleElementReferenceException
- TC008: TimeoutException

### 🏢 BDD业务流程测试
- 员工申请创建
- 费用添加验证
- 数据一致性检查

## 🔧 常用命令

```bash
# 查看项目结构和API演示
python demo_api_usage.py

# 只生成报告（不执行测试）
python -c "from run_chrome_tests import ChromeTestRunner; ChromeTestRunner().generate_detailed_test_report(True)"

# 检查配置文件
cat config/config.yaml

# 查看最新日志
ls -la logs/

# 清理旧报告和截图
rm -rf reports/* screenshots/*
```

## 💡 提示

1. **首次运行**: 会自动下载浏览器驱动，需要网络连接
2. **无头模式**: 在`config/config.yaml`中设置`headless: true`可提高速度
3. **并行执行**: 使用`pytest -n auto`可并行运行测试
4. **调试模式**: 设置日志级别为`DEBUG`获取详细信息

## 📞 需要帮助？

- 📖 查看完整文档: [README.md](README.md)
- 🐛 问题反馈: [GitHub Issues](https://github.com/qqhuice/auto_test_quiz/issues)
- 💬 API使用示例: [demo_api_usage.py](demo_api_usage.py)
