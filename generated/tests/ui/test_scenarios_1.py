import os
import re
import time
import pytest
from generated.pages.home_page import HomePage
from generated.pages.contact_us_page import ContactUsPage
from generated.pages.products_page import ProductsPage
from generated.pages.product_detail_page import ProductDetailPage
from generated.pages.cart_page import CartPage
from generated.pages.test_cases_page import TestCasesPage

def wait_until_true(func, timeout=10, interval=0.5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if func():
                return True
        except Exception:
            pass
        time.sleep(interval)
    return False

@pytest.fixture(autouse=True)
def configure_page(page):
    page.set_default_navigation_timeout(30000)
    page.set_default_timeout(30000)
    
    page.route(
        re.compile(r".*(google|doubleclick|adservice|googlesyndication|analytics|facebook).*"),
        lambda route: route.abort()
    )

    original_goto = page.goto
    def custom_goto(url, *args, **kwargs):
        if kwargs.get("wait_until") in (None, "load"):
            kwargs["wait_until"] = "domcontentloaded"
        if "timeout" not in kwargs or (kwargs["timeout"] is not None and kwargs["timeout"] < 30000):
            kwargs["timeout"] = 30000
        return original_goto(url, *args, **kwargs)

    page.goto = custom_goto

    def handle_framenavigated(frame):
        if frame == page.main_frame and "google_vignette" in page.url:
            clean_url = page.url.split("#")[0]
            try:
                page.evaluate(f"window.location.href = '{clean_url}'")
            except Exception:
                pass

    page.on("framenavigated", handle_framenavigated)
    yield

def test_contact_us_form(page, home_page, contact_us_page):
    # Accept the browser's confirmation dialog automatically
    page.on("dialog", lambda dialog: dialog.accept())

    home_page.navigate_to()
    home_page.click_contact_us()

    file_path = "test_upload_file.txt"
    with open(file_path, "w") as f:
        f.write("This is a test upload file.")

    contact_us_page.fill_contact_form(
        name="John Doe",
        email="john@example.com",
        subject="Support Inquiry",
        message="I need support with my order.",
        file_path=file_path
    )
    contact_us_page.submit()
    
    # Wait for the success text to appear dynamically on the page
    page.wait_for_selector("text=submitted successfully")
    
    assert "submitted successfully" in contact_us_page.get_success_message()

    if os.path.exists(file_path):
        os.remove(file_path)

    contact_us_page.page.goto("https://automationexercise.com/contact_us", wait_until="domcontentloaded")
    contact_us_page.fill_contact_form(
        name="John Doe",
        email="",
        subject="Support Inquiry",
        message="No email provided."
    )
    is_email_invalid = contact_us_page.page.locator("[data-qa='email']").evaluate("el => !el.validity.valid")
    assert is_email_invalid


def test_test_cases_page(page, home_page, test_cases_page):
    home_page.navigate_to()
    home_page.click_test_cases()
    assert wait_until_true(test_cases_page.is_test_cases_visible)


def test_products_and_product_detail(page, home_page, products_page, product_detail_page):
    home_page.navigate_to()
    home_page.click_products()
    assert wait_until_true(products_page.is_products_list_visible)

    products_page.click_view_product_of_first()
    assert product_detail_page.get_product_name() != ""
    assert "Category:" in product_detail_page.get_product_category()
    assert product_detail_page.get_product_price() != ""
    assert "Availability:" in product_detail_page.get_product_availability()
    assert "Condition:" in product_detail_page.get_product_condition()
    assert "Brand:" in product_detail_page.get_product_brand()


def test_search_product(page, home_page, products_page):
    home_page.navigate_to()
    home_page.click_products()
    products_page.search_product("shirt")
    assert products_page.get_product_cards_count() > 0

    products_page.search_product("no_such_product_999")
    assert products_page.get_product_cards_count() == 0

    products_page.search_product("")
    assert wait_until_true(products_page.is_products_list_visible)


def test_subscription(page, home_page, cart_page):
    home_page.navigate_to()
    home_page.scroll_to_bottom()
    assert wait_until_true(home_page.is_footer_visible)
    home_page.subscribe("test_sub@example.com")
    assert "success" in home_page.get_subscription_success_message().lower()

    home_page.click_cart()
    cart_page.subscribe("test_sub_cart@example.com")
    assert "success" in cart_page.get_subscription_success_message().lower()

    cart_page.page.goto("https://automationexercise.com", wait_until="domcontentloaded")
    home_page.scroll_to_bottom()
    home_page.subscribe("invalid-email")
    is_sub_invalid = home_page.page.locator("#susbscribe_email").evaluate("el => !el.validity.valid")
    assert is_sub_invalid


def test_cart_operations(page, home_page, products_page, cart_page, product_detail_page):
    home_page.navigate_to()
    home_page.click_products()
    products_page.add_first_product_to_cart()
    products_page.click_continue_shopping()

    products_page.click_view_product_of_first()
    product_detail_page.set_quantity(3)
    product_detail_page.add_to_cart()
    products_page.click_view_cart_from_modal()

    assert cart_page.get_cart_items_count() >= 1
    assert int(cart_page.get_item_quantity(0)) > 0

    product_detail_page.page.goto("https://automationexercise.com/product_details/1", wait_until="domcontentloaded")
    qty_min = product_detail_page.get_quantity_input_min()
    assert qty_min == "1"
