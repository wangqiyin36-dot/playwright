# Playwright 配置文件
# 用于配置测试运行环境和浏览器设置

import pytest
import os
from datetime import datetime

# 测试报告目录
REPORT_DIR = os.path.join(os.getcwd(), "reports")
# 截图目录
SCREENSHOT_DIR = os.path.join(os.getcwd(), "tests", "screenshots")
# 视频目录
VIDEO_DIR = os.path.join(os.getcwd(), "tests", "videos")
# 跟踪目录
TRACE_DIR = os.path.join(os.getcwd(), "tests", "traces")

# 创建必要的目录
for directory in [REPORT_DIR, SCREENSHOT_DIR, VIDEO_DIR, TRACE_DIR]:
    os.makedirs(directory, exist_ok=True)

# 配置测试项目
projects = [
    {
        "name": "chromium",  # Chrome/Edge浏览器
        "use": {
            "browser_name": "chromium",
            "headless": True,  # 无头模式，设为False可看到浏览器界面
            "viewport": {"width": 1280, "height": 720},  # 视口大小
            "ignore_https_errors": True,  # 忽略HTTPS错误
            "args": ["--no-sandbox", "--disable-dev-shm-usage"],  # 浏览器启动参数
        },
    },
    {
        "name": "firefox",  # Firefox浏览器
        "use": {
            "browser_name": "firefox",
            "headless": True,
            "viewport": {"width": 1280, "height": 720},
        },
    },
    {
        "name": "webkit",  # Safari浏览器
        "use": {
            "browser_name": "webkit",
            "headless": True,
            "viewport": {"width": 1280, "height": 720},
        },
    },
]

# pytest配置类
class PlaywrightConfig:
    # 测试目录
    test_dir = "./tests"
    # 测试文件匹配模式
    python_files = ["test_*.py", "*_test.py"]
    # 测试类匹配模式
    python_classes = ["Test*"]
    # 测试函数匹配模式
    python_functions = ["test_*"]
    # 超时设置
    timeout = 30000
    # 断言超时时间
    expect_timeout = 10000
    # 并行测试数量
    workers = 1
    # 测试报告配置
    reporter = [
        ("html", REPORT_DIR),  # HTML报告
        ("progress", None),     # 进度报告
        ("json", os.path.join(REPORT_DIR, "report.json")),  # JSON报告
    ]
    # 测试项目配置
    projects = projects
    # 全局使用配置
    use = {
        "base_url": "http://example.com",  # 默认基础URL
        "trace": "on-first-retry",  # 失败重试时记录跟踪信息
        "screenshot": "only-on-failure",  # 仅在失败时截图
        "video": "retain-on-failure",  # 仅在失败时保留视频
        "screenshot_dir": SCREENSHOT_DIR,  # 截图保存目录
        "video_dir": VIDEO_DIR,  # 视频保存目录
        "trace_dir": TRACE_DIR,  # 跟踪信息保存目录
    }

# 导出配置
config = PlaywrightConfig()

# pytest配置钩子函数
def pytest_configure(config):
    """
    pytest配置钩子函数
    """
    # 设置测试元数据
    config._metadata["Project"] = "My Playwright Project"
    config._metadata["Author"] = "AI Assistant"
    config._metadata["Environment"] = "Production"
    config._metadata["Report Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 配置自定义标记
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "regression: 回归测试")
    config.addinivalue_line("markers", "sanity: 健全测试")
    config.addinivalue_line("markers", "critical: 关键功能测试")

def pytest_sessionstart(session):
    """
    测试会话开始钩子函数
    """
    print("\n" + "="*60)
    print("          测试开始执行")
    print("="*60)
    print(f"测试项目: My Playwright Project")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试浏览器: {[p['name'] for p in projects]}")
    print("="*60 + "\n")

def pytest_sessionfinish(session, exitstatus):
    """
    测试会话结束钩子函数
    """
    print("\n" + "="*60)
    print("          测试执行完成")
    print("="*60)
    print(f"结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"退出状态: {exitstatus}")
    print("="*60 + "\n")

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    终端报告钩子函数
    """
    terminalreporter.write_sep("-", "自定义测试报告")
    passed = len(terminalreporter.stats.get('passed', []))
    failed = len(terminalreporter.stats.get('failed', []))
    skipped = len(terminalreporter.stats.get('skipped', []))
    total = passed + failed + skipped
    
    terminalreporter.write(f"总测试数: {total}\n")
    terminalreporter.write(f"通过: {passed}\n")
    terminalreporter.write(f"失败: {failed}\n")
    terminalreporter.write(f"跳过: {skipped}\n")
    
    if total > 0:
        success_rate = (passed / total) * 100
        terminalreporter.write(f"通过率: {success_rate:.2f}%\n")
    
    terminalreporter.write_sep("-", "测试报告路径")
    terminalreporter.write(f"HTML报告: {os.path.join(REPORT_DIR, 'index.html')}\n")
    terminalreporter.write(f"JSON报告: {os.path.join(REPORT_DIR, 'report.json')}\n")