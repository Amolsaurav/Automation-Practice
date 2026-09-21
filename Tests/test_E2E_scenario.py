from playwright.sync_api import Page, expect
import pytest

from Pages.signUp import SignUp
from Pages.login import Login
from utilities.data_loader import DataLoader
from utilities.constants import (
    LOGIN_DATA_FILE,
    ORDER_COMMENT,
    PAYMENT_CARD_NUMBER,
    PAYMENT_CVC,
    PAYMENT_EXPIRY_MONTH,
    PAYMENT_EXPIRY_YEAR,
    PAYMENT_NAME,
    PRODUCT_GREEN_TSHIRT,
    TEXT_LOGGED_IN_AS,
)

data = DataLoader.load_json(LOGIN_DATA_FILE)

@pytest.mark.parametrize(
    "login_data",
    data["valid_login"],
    ids=[user["id"] for user in data["valid_login"]]
)
def test_E2E_Scenario(page: Page, app_url, login_data):
    page.goto(app_url)
    open_login_page = SignUp(page)
    open_login_page.open_signup()
    login = Login(page)
    dashboard_page = login.login_user(login_data)
    product_page = dashboard_page.navigate_to_products_page()
    product_page.open_category()
    product_page.add_to_cart(PRODUCT_GREEN_TSHIRT)
    cart_page = product_page.go_to_cart()
    checkout_page = cart_page.proceed_to_checkout()
    payment_page = checkout_page.place_order(ORDER_COMMENT)
    payment_done = payment_page.submit_paymentForm(
        PAYMENT_NAME, PAYMENT_CARD_NUMBER, PAYMENT_CVC, PAYMENT_EXPIRY_MONTH, PAYMENT_EXPIRY_YEAR
    )
    payment_done.download_invoice()
    dashboard_page = payment_done.continue_next()
    expect(dashboard_page.page.get_by_text(TEXT_LOGGED_IN_AS)).to_be_visible()