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