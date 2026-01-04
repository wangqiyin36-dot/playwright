# 导入必要的库和模块
import os
import logging
import pytest
from datetime import datetime
from playwright.sync_api import Page

# 创建日志目录
os.makedirs(os.path.join(os.getcwd(), 'tests', 'logs'), exist_ok=True)
os.makedirs(os.path.join(os.getcwd(), 'tests', 'screenshots'), exist_ok=True)

# 设置日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.getcwd(), 'tests', 'logs', 'test_log.log')),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 添加自定义命令行参数
def pytest_addoption(parser):
    """
    添加自定义命令行参数
    """
    # 所有浏览器相关的选项都由pytest-playwright插件提供，无需自定义
    pass

# 注册自定义测试标记
def pytest_configure(config):
    """
    配置pytest环境，注册自定义标记
    """
    # 注册自定义标记
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "critical: 关键功能测试")
    config.addinivalue_line("markers", "regression: 回归测试")
    config.addinivalue_line("markers", "sanity: 健全测试")
    config.addinivalue_line("markers", "performance: 性能测试")
    config.addinivalue_line("markers", "api: API测试")
    config.addinivalue_line("markers", "ui: UI测试")

@pytest.fixture(scope="function")
def page(page: Page, request) -> Page:
    """
    函数级别的页面fixture
    每个测试函数都会获得一个新的页面实例
    扩展pytest-playwright提供的page fixture，添加自定义功能
    """
    logger.info(f"创建新页面: {request.node.name}")
    
    # 设置页面超时
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)
    
    yield page
    
    # 测试失败时保存更多信息
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        # 保存截图
        screenshot_path = os.path.join(
            os.getcwd(), 'tests', 'screenshots', 
            f"{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        )
        page.screenshot(path=screenshot_path)
        logger.error(f"测试失败，截图已保存: {screenshot_path}")
        
        # 保存页面内容
        html_path = os.path.join(
            os.getcwd(), 'tests', 'screenshots', 
            f"{request.node.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        )
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(page.content())
        logger.error(f"测试失败，页面HTML已保存: {html_path}")
    
    logger.info(f"关闭页面: {request.node.name}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    钩子函数：保存测试结果
    """
    # 获取钩子方法的调用结果
    outcome = yield
    rep = outcome.get_result()
    
    # 每个测试用例执行后
    if rep.when == "call":
        # 设置属性，保存测试结果
        setattr(item, "rep_call", rep)

@pytest.fixture(autouse=True)
def test_fixture(request):
    """
    自动使用的fixture，记录测试开始和结束
    """
    logger.info(f"测试开始: {request.node.name}")
    
    yield
    
    if hasattr(request.node, "rep_call"):
        if request.node.rep_call.passed:
            logger.info(f"测试通过: {request.node.name}")
        else:
            logger.error(f"测试失败: {request.node.name}")
    else:
        logger.warning(f"测试完成: {request.node.name} (未获取到测试结果)")

@pytest.fixture(scope="function")
def context(browser):
    """为每个测试创建独立的上下文"""
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """为每个测试创建独立的页面"""
    page = context.new_page()
    yield page
    page.close()            