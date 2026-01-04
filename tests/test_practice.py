import pytest

@pytest.mark.parametrize("username,password,expected", [
    ("admin", "admin123", True),
    ("user", "wrongpass", False),
    ("", "password", False),
    ("admin", "", False),
])
def test_login_combinations(page: Page, username, password, expected):
    page.goto("/login")
    page.fill("#username", username)
    page.fill("#password", password)

    page.click("#submit")
    
    if expected:
        expect(page).to_have_url("**/dashboard")
    else:
        expect(page.locator(".error")).to_be_visible()


# 测试在一个 context 中使用多个页面
def test_multiple_pages(context: BrowserContext):
    """在一个 context 中使用多个页面"""
    # 创建第一个页面
    page1 = context.new_page()
    page1.goto("https://example.com")
    
    # 创建第二个页面（共享同一个 context）
    page2 = context.new_page()
    page2.goto("https://google.com")
    
    # 两个页面共享 cookies、localStorage 等
    # 因为它们属于同一个 BrowserContext
    
    # 验证两个页面都正常打开
    assert "Example" in page1.title()
    assert "Google" in page2.title()        

#使用多个
def test_cookie_management(context, logged_in_page):
    # 获取登录后的 cookies
    cookies = context.cookies()
    
    # 验证是否包含认证 cookie
    auth_cookie = next((c for c in cookies if c["name"] == "auth_token"), None)
    assert auth_cookie is not None
    
    # 可以使用这些 cookies 在其他 context 中保持登录状态    