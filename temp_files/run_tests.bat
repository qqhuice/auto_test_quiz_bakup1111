@echo off
REM 自动化测试运行脚本 (Windows批处理版本)
REM 支持多种测试运行模式

setlocal enabledelayedexpansion

echo.
echo ================================================================
echo                    自动化测试运行脚本
echo ================================================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未找到Python，请确保Python已安装并添加到PATH
    pause
    exit /b 1
)

REM 获取命令行参数
set "MODE=%1"
if "%MODE%"=="" set "MODE=basic"

echo 运行模式: %MODE%
echo 当前时间: %date% %time%
echo.

REM 确保必要的目录存在
if not exist "reports" mkdir reports
if not exist "screenshots" mkdir screenshots

REM 根据模式运行不同的测试
if "%MODE%"=="basic" (
    echo 运行基础功能测试...
    python -m pytest tests/test_basic_functionality.py -v
) else if "%MODE%"=="all" (
    echo 运行所有测试...
    python -m pytest tests/ -v
) else if "%MODE%"=="smoke" (
    echo 运行冒烟测试...
    python -m pytest tests/ -m smoke -v
) else if "%MODE%"=="bdd" (
    echo 运行BDD Cucumber测试...
    python run_bdd_tests.py
) else if "%MODE%"=="ui" (
    echo 运行UI测试...
    python -m pytest tests/ -m ui -v
) else if "%MODE%"=="report" (
    echo 生成测试报告...
    set "TIMESTAMP=%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%"
    set "TIMESTAMP=!TIMESTAMP: =0!"
    python -m pytest tests/ --html=reports/test_report_!TIMESTAMP!.html --self-contained-html -v
) else (
    echo ❌ 错误: 未知的运行模式 "%MODE%"
    echo.
    echo 支持的模式:
    echo   basic  - 运行基础功能测试
    echo   all    - 运行所有测试
    echo   smoke  - 运行冒烟测试
    echo   bdd    - 运行BDD Cucumber测试
    echo   ui     - 运行UI测试
    echo   report - 生成测试报告
    echo.
    echo 使用方法: run_tests.bat [模式]
    echo 示例: run_tests.bat basic
    pause
    exit /b 1
)

echo.
if errorlevel 1 (
    echo ❌ 测试执行失败！
    echo ================================================================
    pause
    exit /b 1
) else (
    echo 🎉 测试执行成功完成！
    echo ================================================================
    pause
    exit /b 0
)
