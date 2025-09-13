"""
测试报告管理器
负责生成和管理测试报告
"""
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from loguru import logger
from config.config_manager import config


class ReportManager:
    """测试报告管理器类"""
    
    def __init__(self, report_dir: str = "reports"):
        """
        初始化报告管理器
        
        Args:
            report_dir: 报告保存目录
        """
        self.report_dir = Path(report_dir)
        self.report_config = config.report_config
        self._ensure_directory_exists()
        self.test_results = []
        self.start_time = None
        self.end_time = None
    
    def _ensure_directory_exists(self):
        """确保报告目录存在"""
        self.report_dir.mkdir(parents=True, exist_ok=True)
    
    def start_test_session(self):
        """开始测试会话"""
        self.start_time = datetime.now()
        self.test_results = []
        logger.info("测试会话开始")
    
    def end_test_session(self):
        """结束测试会话"""
        self.end_time = datetime.now()
        logger.info("测试会话结束")
    
    def add_test_result(self, test_name: str, status: str, duration: float, 
                       error_message: str = None, screenshots: List[str] = None):
        """
        添加测试结果
        
        Args:
            test_name: 测试名称
            status: 测试状态 (PASSED, FAILED, SKIPPED)
            duration: 执行时间（秒）
            error_message: 错误信息
            screenshots: 截图文件列表
        """
        test_result = {
            'name': test_name,
            'status': status,
            'duration': duration,
            'timestamp': datetime.now().isoformat(),
            'error_message': error_message,
            'screenshots': screenshots or []
        }
        
        self.test_results.append(test_result)
        logger.info(f"添加测试结果: {test_name} - {status}")
    
    def generate_html_report(self) -> str:
        """
        生成HTML测试报告
        
        Returns:
            报告文件路径
        """
        if not self.test_results:
            logger.warning("没有测试结果，无法生成报告")
            return None
        
        # 计算统计信息
        stats = self._calculate_statistics()
        
        # 生成HTML内容
        html_content = self._generate_html_content(stats)
        
        # 保存报告文件
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_filename = f"test_report_{timestamp}.html"
        report_path = self.report_dir / report_filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML报告已生成: {report_path}")
        return str(report_path)
    
    def _calculate_statistics(self) -> Dict[str, Any]:
        """
        计算测试统计信息
        
        Returns:
            统计信息字典
        """
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASSED'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAILED'])
        skipped_tests = len([r for r in self.test_results if r['status'] == 'SKIPPED'])
        
        total_duration = sum(r['duration'] for r in self.test_results)
        
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'skipped_tests': skipped_tests,
            'pass_rate': round(pass_rate, 2),
            'total_duration': round(total_duration, 2),
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S") if self.start_time else "未知",
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S") if self.end_time else "未知"
        }
    
    def _generate_html_content(self, stats: Dict[str, Any]) -> str:
        """
        生成HTML报告内容
        
        Args:
            stats: 统计信息
            
        Returns:
            HTML内容字符串
        """
        title = self.report_config.get('title', '自动化测试报告')
        description = self.report_config.get('description', '基础验证测试报告')
        
        html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background-color: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #666;
            font-size: 0.9em;
        }}
        .passed {{ color: #28a745; }}
        .failed {{ color: #dc3545; }}
        .skipped {{ color: #ffc107; }}
        .total {{ color: #007bff; }}
        .results {{
            padding: 30px;
        }}
        .test-item {{
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-bottom: 20px;
            overflow: hidden;
        }}
        .test-header {{
            padding: 15px 20px;
            background-color: #f8f9fa;
            border-bottom: 1px solid #ddd;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .test-name {{
            font-weight: bold;
            font-size: 1.1em;
        }}
        .test-status {{
            padding: 5px 15px;
            border-radius: 20px;
            color: white;
            font-size: 0.9em;
        }}
        .status-passed {{ background-color: #28a745; }}
        .status-failed {{ background-color: #dc3545; }}
        .status-skipped {{ background-color: #ffc107; }}
        .test-details {{
            padding: 20px;
        }}
        .test-info {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 15px;
        }}
        .info-item {{
            display: flex;
            justify-content: space-between;
        }}
        .info-label {{
            font-weight: bold;
            color: #666;
        }}
        .error-message {{
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 5px;
            margin-top: 15px;
            font-family: monospace;
            white-space: pre-wrap;
        }}
        .screenshots {{
            margin-top: 15px;
        }}
        .screenshot-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
            margin-top: 10px;
        }}
        .screenshot-item {{
            border: 1px solid #ddd;
            border-radius: 5px;
            overflow: hidden;
        }}
        .screenshot-item img {{
            width: 100%;
            height: auto;
            display: block;
        }}
        .screenshot-caption {{
            padding: 10px;
            background-color: #f8f9fa;
            font-size: 0.9em;
            color: #666;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #ddd;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{title}</h1>
            <p>{description}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number total">{stats['total_tests']}</div>
                <div class="stat-label">总测试数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number passed">{stats['passed_tests']}</div>
                <div class="stat-label">通过</div>
            </div>
            <div class="stat-card">
                <div class="stat-number failed">{stats['failed_tests']}</div>
                <div class="stat-label">失败</div>
            </div>
            <div class="stat-card">
                <div class="stat-number skipped">{stats['skipped_tests']}</div>
                <div class="stat-label">跳过</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['pass_rate']}%</div>
                <div class="stat-label">通过率</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{stats['total_duration']}s</div>
                <div class="stat-label">总耗时</div>
            </div>
        </div>
        
        <div class="results">
            <h2>测试结果详情</h2>
            {self._generate_test_results_html()}
        </div>
        
        <div class="footer">
            <p>报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>测试开始时间: {stats['start_time']} | 测试结束时间: {stats['end_time']}</p>
        </div>
    </div>
</body>
</html>
        """
        
        return html_template
    
    def _generate_test_results_html(self) -> str:
        """
        生成测试结果HTML
        
        Returns:
            测试结果HTML字符串
        """
        results_html = ""
        
        for result in self.test_results:
            status_class = f"status-{result['status'].lower()}"
            
            screenshots_html = ""
            if result['screenshots']:
                screenshots_html = f"""
                <div class="screenshots">
                    <h4>截图记录</h4>
                    <div class="screenshot-grid">
                        {self._generate_screenshots_html(result['screenshots'])}
                    </div>
                </div>
                """
            
            error_html = ""
            if result['error_message']:
                error_html = f"""
                <div class="error-message">
                    <strong>错误信息:</strong><br>
                    {result['error_message']}
                </div>
                """
            
            results_html += f"""
            <div class="test-item">
                <div class="test-header">
                    <div class="test-name">{result['name']}</div>
                    <div class="test-status {status_class}">{result['status']}</div>
                </div>
                <div class="test-details">
                    <div class="test-info">
                        <div class="info-item">
                            <span class="info-label">执行时间:</span>
                            <span>{result['duration']:.2f}秒</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">时间戳:</span>
                            <span>{result['timestamp']}</span>
                        </div>
                    </div>
                    {error_html}
                    {screenshots_html}
                </div>
            </div>
            """
        
        return results_html
    
    def _generate_screenshots_html(self, screenshots: List[str]) -> str:
        """
        生成截图HTML
        
        Args:
            screenshots: 截图文件路径列表
            
        Returns:
            截图HTML字符串
        """
        screenshots_html = ""
        
        for screenshot in screenshots:
            # 获取相对路径
            screenshot_path = Path(screenshot)
            if screenshot_path.is_absolute():
                try:
                    screenshot_path = screenshot_path.relative_to(Path.cwd())
                except ValueError:
                    screenshot_path = screenshot_path.name
            
            caption = screenshot_path.stem.replace('_', ' ')
            
            screenshots_html += f"""
            <div class="screenshot-item">
                <img src="{screenshot_path}" alt="{caption}" onclick="window.open(this.src)">
                <div class="screenshot-caption">{caption}</div>
            </div>
            """
        
        return screenshots_html
    
    def generate_json_report(self) -> str:
        """
        生成JSON格式的测试报告
        
        Returns:
            报告文件路径
        """
        if not self.test_results:
            logger.warning("没有测试结果，无法生成JSON报告")
            return None
        
        stats = self._calculate_statistics()
        
        report_data = {
            'summary': stats,
            'test_results': self.test_results
        }
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_filename = f"test_report_{timestamp}.json"
        report_path = self.report_dir / report_filename
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"JSON报告已生成: {report_path}")
        return str(report_path)


# 全局报告管理器实例
report_manager = ReportManager()
