# 百度搜索测试
# 展示Playwright的表单填写和交互功能

from playwright.sync_api import Page


def test_baidu_search(page: Page):
    """
    测试百度搜索功能
    """
    # 导航到百度首页
    page.goto("https://www.baidu.com")
    
    # 验证页面标题
    assert "百度" in page.title()
    
    # 定位搜索输入框并输入搜索关键词
    search_input = page.locator("#kw")
    search_input.fill("Python Playwright")
    
    # 定位搜索按钮并点击
    search_button = page.locator("#su")
    search_button.click()
    
    # 等待页面加载完成
    page.wait_for_load_state("networkidle")
    
    # 验证搜索结果包含预期内容
    assert page.locator("#content_left").is_visible()
    
    # 验证搜索结果中包含关键词
    assert page.locator(f"text=Python Playwright").count() > 0
    
    # 截图保存搜索结果
    page.screenshot(path="tests/screenshots/baidu_search_results.png")


def test_baidu_search_suggestions(page: Page):
    """
    测试百度搜索建议功能
    """
    # 导航到百度首页
    page.goto("https://www.baidu.com")
    
    # 定位搜索输入框
    search_input = page.locator("#kw")
    
    # 输入部分搜索关键词
    search_input.fill("Python")
    
    # 等待搜索建议出现
    page.wait_for_selector("#form .bdsug-overflow")
    
    # 获取搜索建议列表
    suggestions = page.locator("#form .bdsug-overflow li")
    
    # 验证搜索建议数量大于0
    assert suggestions.count() > 0
    
    # 截图保存搜索建议
    page.screenshot(path="tests/screenshots/baidu_suggestions.png")
