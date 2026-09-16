from playwright.sync_api import Page, expect
import pytest

from Pages.login import Login
from Pages.signUp import SignUp
from utilities.data_loader import DataLoader

data = DataLoader.load_json("login.json")

@pytest.mark.parametrize(
    "login_data",
    data["valid_login"],
    ids=[user["id"] for user in data["valid_login"]]
)
def test_valid_login(page: Page, app_url, login_data):
    page.goto(app_url)
    open_login_page = SignUp(page)
    open_login_page.open_signup()
    expect(page.get_by_text('Login to your account')).to_be_visible()
    loginUser = Login(page)
    loginUser.login_user(login_data)
    expect(page.get_by_text('Logged in')).to_be_visible()

@pytest.mark.parametrize(
    "login_data",
    data["invalid_login"],
    ids=[user["id"] for user in data["invalid_login"]]
)
def test_invalid_login(page: Page, app_url, login_data):
    
    page.goto(app_url)
    open_login_page = SignUp(page)
    open_login_page.open_signup()
    expect(page.get_by_text('Login to your account')).to_be_visible()
    loginUser = Login(page)
    loginUser.login_user(login_data)
    if not login_data["email"]:
        expect(loginUser.emailInput).to_have_attribute("required", "")
    else:
        expect(
                page.get_by_text(login_data["expected_error"])
            ).to_be_visible()


@pytest.mark.parametrize(
    "email,password",
    [("", "Password123"), ("valid@example.com", "")],
)
def test_login_requires_email_and_password(page: Page, app_url, email: str, password: str):
    page.goto(app_url)
    open_login_page = SignUp(page)
    open_login_page.open_signup()
    login_form = Login(page)
    login_form.emailInput.fill(email)
    login_form.passwordInput.fill(password)
    login_form.loginBtn.click()

    expect(page.get_by_text("Login to your account")).to_be_visible()
