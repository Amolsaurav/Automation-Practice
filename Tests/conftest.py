import pytest
from playwright.sync_api import Page, expect

from Pages.login import Login
from Pages.signUp import SignUp
from utilities.data_loader import DataLoader

APP_URL = "https://automationexercise.com"


@pytest.fixture
def app_url() -> str:
    return APP_URL


@pytest.fixture(autouse=True)
def configure_page(page: Page) -> None:
    page.set_default_navigation_timeout(60_000)
    page.set_default_timeout(10_000)


@pytest.fixture
def authenticated_page(page: Page, app_url: str) -> Page:
    credentials = DataLoader.load_json("login.json")["valid_login"][0]
    page.goto(app_url, wait_until="domcontentloaded")
    SignUp(page).open_signup()
    Login(page).login_user(credentials)
    expect(page.get_by_text("Logged in as")).to_be_visible()
    return page
