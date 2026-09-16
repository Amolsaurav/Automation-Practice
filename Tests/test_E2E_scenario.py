from playwright.sync_api import Page, expect
import pytest

from Pages.signUp import SignUp
from Pages.login import Login
from utilities.data_loader import DataLoader

data = DataLoader.load_json("login.json")

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
    product_page.add_to_cart('Green Side Placket Detail T-Shirt')
    cart_page = product_page.go_to_cart()
    checkout_page = cart_page.proceed_to_checkout()
    payment_page = checkout_page.place_order("This is the order placed by automation")
    payment_done = payment_page.submit_paymentForm("Abc","12345678980","125","8","2025")
    payment_done.download_invoice()
    dashboard_page = payment_done.continue_next()
    expect(dashboard_page.page.get_by_text('Logged in as')).to_be_visible()