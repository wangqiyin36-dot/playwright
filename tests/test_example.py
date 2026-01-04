# 示例测试文件
# 测试访问example.com网站

import pytest
from playwright.sync_api import Page
import logging

# 配置日志
logger = logging.getLogger(__name__)


@pytest.mark.smoke  # 冒烟测试标记
@pytest.mark.critical  # 关键功能测试标记
def test_access_example_com(page: Page):
    """
    测试访问example.com网站并验证标题
    
    Args:
        page: Playwright页面对象，由fixture提供
    """
    logger.info("开始测试: 访问example.com")
    
    # 导航到example.com
    page.goto("https://example.com")
    logger.info("成功导航到example.com")
    
    # 验证页面标题
    assert page.title() == "Example Domain", f"页面标题不正确，预期: 'Example Domain', 实际: '{page.title()}'"
    logger.info("页面标题验证通过")
    
    # 验证页面包含预期的文本
    h1_text = page.locator("h1").inner_text()
    assert h1_text == "Example Domain", f"页面h1文本不正确，预期: 'Example Domain', 实际: '{h1_text}'"
    logger.info("页面h1文本验证通过")
    
    # 验证页面包含链接
    assert page.locator("a").count() > 0, "页面不包含链接"
    logger.info("页面链接验证通过")
    
    # 截图保存
    page.screenshot(path="tests/screenshots/example_com.png")
    logger.info("保存截图: example_com.png")
    
    logger.info("测试完成: 访问example.com")


@pytest.mark.regression  # 回归测试标记
@pytest.mark.parametrize("url, expected_title", [
    ("https://example.com", "Example Domain"),
    ("https://example.org", "Example Domain"),
    ("https://example.net", "Example Domain"),
], ids=["example_com", "example_org", "example_net"])  # 参数化测试ID
def test_multiple_domains(page: Page, url: str, expected_title: str):
    """
    使用参数化测试访问多个域名
    
    Args:
        page: Playwright页面对象，由fixture提供
        url: 要访问的URL
        expected_title: 预期的页面标题
    """
    logger.info(f"开始测试: 访问{url}")
    
    # 导航到指定URL
    page.goto(url)
    logger.info(f"成功导航到{url}")
    
    # 验证页面标题
    actual_title = page.title()
    assert actual_title == expected_title, f"页面标题不正确，URL: {url}, 预期: '{expected_title}', 实际: '{actual_title}'"
    logger.info(f"页面标题验证通过: {actual_title}")
    
    # 验证页面包含h1标签
    assert page.locator("h1").is_visible(), f"页面不包含h1标签，URL: {url}"
    logger.info(f"页面h1标签验证通过")
    
    logger.info(f"测试完成: 访问{url}")


@pytest.mark.sanity  # 健全测试标记
def test_page_navigation(page: Page):
    """
    测试页面导航功能
    
    Args:
        page: Playwright页面对象，由fixture提供
    """
    logger.info("开始测试: 页面导航功能")
    
    # 导航到example.com
    page.goto("https://example.com")
    logger.info("成功导航到example.com")
    
    # 获取页面URL
    current_url = page.url
    logger.info(f"当前URL: {current_url}")
    
    # 验证URL
    assert current_url == "https://example.com/", f"URL不正确，预期: 'https://example.com/', 实际: '{current_url}'"
    logger.info("URL验证通过")
    
    logger.info("测试完成: 页面导航功能")