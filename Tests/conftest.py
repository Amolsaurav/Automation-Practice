import pytest
from playwright.sync_api import Page, expect

from Pages.login import Login
from Pages.signUp import SignUp
from utilities.data_loader import DataLoader
from utilities.constants import (
    APP_URL,
    DEFAULT_TIMEOUT_MS,
    LOGIN_DATA_FILE,
    NAVIGATION_TIMEOUT_MS,
    TEXT_LOGGED_IN_AS,
)


@pytest.fixture
def app_url() -> str:
    return APP_URL


@pytest.fixture(autouse=True)
def configure_page(page: Page) -> None:
    page.set_default_navigation_timeout(NAVIGATION_TIMEOUT_MS)
    page.set_default_timeout(DEFAULT_TIMEOUT_MS)


@pytest.fixture
def authenticated_page(page: Page, app_url: str) -> Page:
    credentials = DataLoader.load_json(LOGIN_DATA_FILE)["valid_login"][0]
    page.goto(app_url, wait_until="domcontentloaded")
    SignUp(page).open_signup()
    Login(page).login_user(credentials)
    expect(page.get_by_text(TEXT_LOGGED_IN_AS)).to_be_visible()
    return page
