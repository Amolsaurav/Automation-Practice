import time
import pytest
from generated.pages.home_page import HomePage
from generated.pages.signup_login_page import SignupLoginPage
from generated.pages.register_page import RegisterPage
from generated.pages.account_created_page import AccountCreatedPage

@pytest.fixture(autouse=True)
def setup_page(page):
    page.set_default_navigation_timeout(30000)
    page.set_default_timeout(30000)

    original_goto = page.goto
    def custom_goto(url, *args, **kwargs):
        if kwargs.get("wait_until") in (None, "load"):
            kwargs["wait_until"] = "domcontentloaded"
        return original_goto(url, *args, **kwargs)
    page.goto = custom_goto

    def block_ads(route):
        url = route.request.url.lower()
        resource_type = route.request.resource_type
        if any(domain in url for domain in [
            "google", "doubleclick", "adservice", "googlesyndication",
            "analytics", "adsystem", "facebook", "twitter", "fontawesome",
            "disqus", "criteo", "amazon", "adroll", "popads", "syndication",
            "clarity", "bing", "yandex", "fundingchoices"
        ]) or resource_type in ["image", "media", "font"]:
            route.abort()
        else:
            route.continue_()
    page.route("**/*", block_ads)

def get_unique_email():
    return f"ui_user_{int(time.time() * 1000)}@example.com"

def test_register_user_valid(page, home_page, signup_login_page, register_page, account_created_page):
    email = get_unique_email()
    name = "UI Test User"

    home_page.navigate_to()
    home_page.click_signup_login()

    signup_login_page.signup(name, email)

    register_page.fill_account_details("Mr", "ValidPass123!", "10", "May", "1990")
    register_page.fill_address_details(
        "John", "Doe", "Test Company", "123 Main St", "Suite 100",
        "United States", "California", "Los Angeles", "90001", "1234567890"
    )
    register_page.click_create_account()

    assert account_created_page.is_account_created_visible()

    account_created_page.click_continue()
    page.locator(f"text=Logged in as {name}").wait_for()
    assert home_page.is_logged_in_as(name)

    home_page.click_delete_account()
    assert account_created_page.is_account_deleted_visible()
    account_created_page.click_continue()


def test_register_user_invalid_and_missing_data(page, home_page, signup_login_page, register_page, account_created_page):
    email = get_unique_email()
    name = "UI Test User"
    home_page.navigate_to()
    home_page.click_signup_login()
    signup_login_page.signup(name, email)
    register_page.fill_account_details("Mr", "ValidPass123!", "10", "May", "1990")
    register_page.fill_address_details(
        "John", "Doe", "Test Company", "123 Main St", "Suite 100",
        "United States", "California", "Los Angeles", "90001", "1234567890"
    )
    register_page.click_create_account()
    account_created_page.click_continue()
    home_page.click_logout()

    home_page.click_signup_login()
    signup_login_page.signup(name, email)
    assert signup_login_page.get_signup_error() == "Email Address already exist!"

    signup_login_page.page.goto("https://automationexercise.com/login", wait_until="domcontentloaded")
    signup_login_page.signup("", get_unique_email())
    is_name_invalid = signup_login_page.page.locator("form[action='/signup'] input[name='name']").evaluate("el => !el.validity.valid")
    assert is_name_invalid

    signup_login_page.page.goto("https://automationexercise.com/login", wait_until="domcontentloaded")
    signup_login_page.signup("Name", "invalid-email")
    is_email_invalid = signup_login_page.page.locator("form[action='/signup'] input[name='email']").evaluate("el => !el.validity.valid")
    assert is_email_invalid

    signup_login_page.page.goto("https://automationexercise.com/login", wait_until="domcontentloaded")
    signup_login_page.signup("Name", "")
    is_email_empty = signup_login_page.page.locator("form[action='/signup'] input[name='email']").evaluate("el => !el.validity.valid")
    assert is_email_empty


def test_login_user_valid(page, home_page, signup_login_page, register_page, account_created_page):
    email = get_unique_email()
    name = "Login User"

    home_page.navigate_to()
    home_page.click_signup_login()
    signup_login_page.signup(name, email)
    register_page.fill_account_details("Mr", "ValidPass123!", "10", "May", "1990")
    register_page.fill_address_details(
        "John", "Doe", "Test Company", "123 Main St", "Suite 100",
        "United States", "California", "Los Angeles", "90001", "1234567890"
    )
    register_page.click_create_account()
    account_created_page.click_continue()
    home_page.click_logout()

    home_page.click_signup_login()
    signup_login_page.login(email, "ValidPass123!")

    page.locator(f"text=Logged in as {name}").wait_for()
    assert home_page.is_logged_in_as(name)


def test_login_user_invalid(page, home_page, signup_login_page):
    home_page.navigate_to()
    home_page.click_signup_login()
    signup_login_page.login("unregistered_user_999@example.com", "WrongPass123!")
    assert signup_login_page.get_login_error() == "Your email or password is incorrect!"
    assert home_page.is_logged_out()

    signup_login_page.page.goto("https://automationexercise.com/login", wait_until="domcontentloaded")
    signup_login_page.login("", "ValidPass123!")
    is_email_invalid = signup_login_page.page.locator("form[action='/login'] input[name='email']").evaluate("el => !el.validity.valid")
    assert is_email_invalid


def test_logout_user(page, home_page, signup_login_page, register_page, account_created_page):
    email = get_unique_email()
    name = "Logout User"

    home_page.navigate_to()
    home_page.click_signup_login()
    signup_login_page.signup(name, email)
    register_page.fill_account_details("Mr", "ValidPass123!", "10", "May", "1990")
    register_page.fill_address_details(
        "John", "Doe", "Test Company", "123 Main St", "Suite 100",
        "United States", "California", "Los Angeles", "90001", "1234567890"
    )
    register_page.click_create_account()
    account_created_page.click_continue()

    home_page.click_logout()

    assert "login" in page.url
    assert home_page.is_logged_out()
