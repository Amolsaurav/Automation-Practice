import re

from playwright.sync_api import Page, expect
from utilities.constants import (
    CONTACT_MESSAGE,
    CONTACT_SUBJECT,
    NONEXISTENT_PRODUCT,
    PRODUCT_GREEN_TSHIRT,
    REVIEW_EMAIL,
    REVIEW_NAME,
    REVIEW_TEXT,
    ROUTE_BRAND_POLO,
    ROUTE_CATEGORY_PRODUCTS,
    ROUTE_PRODUCT_DETAILS,
    ROUTE_PRODUCTS,
    SUBSCRIPTION_EMAIL,
    TEXT_ADD_TO_CART,
    TEXT_CHECKOUT_LOGIN_REQUIRED,
    TEXT_CONTACT_US,
    TEXT_PLACE_ORDER,
    TEXT_REVIEW_SUBMITTED,
    TEXT_SEARCHED_PRODUCTS,
    TEXT_SUBSCRIBED,
    TEXT_VIEW_CART,
)


def add_product_to_cart(page: Page, app_url: str):
    page.goto(f"{app_url}{ROUTE_BRAND_POLO}", wait_until="domcontentloaded")
    product = page.locator(".productinfo", has_text=PRODUCT_GREEN_TSHIRT)
    expect(product).to_be_visible()
    add_to_cart = product.get_by_role("link", name=TEXT_ADD_TO_CART)
    add_to_cart.scroll_into_view_if_needed()
    add_to_cart.click()
    modal = page.locator(".modal-content:visible")
    expect(modal).to_be_visible()
    modal.get_by_role("link", name=TEXT_VIEW_CART).click()


def test_logout_returns_to_login(authenticated_page: Page):
    authenticated_page.get_by_role("link", name="Logout").click()

    expect(authenticated_page.get_by_text("Login to your account")).to_be_visible()


def test_products_can_be_searched(page: Page, app_url: str):
    page.goto(f"{app_url}{ROUTE_PRODUCTS}")
    page.locator("#search_product").fill(PRODUCT_GREEN_TSHIRT)
    page.locator("#submit_search").click()

    expect(page.get_by_text("Searched Products")).to_be_visible()
    expect(page.locator(".productinfo", has_text=PRODUCT_GREEN_TSHIRT)).to_be_visible()


def test_product_search_with_no_match_shows_no_product(page: Page, app_url: str):
    page.goto(f"{app_url}{ROUTE_PRODUCTS}")
    page.locator("#search_product").fill(NONEXISTENT_PRODUCT)
    page.locator("#submit_search").click()

    expect(page.get_by_text("Searched Products")).to_be_visible()
    expect(page.locator(".productinfo")).to_have_count(0)


def test_product_details_can_be_opened(page: Page, app_url: str):
    page.goto(f"{app_url}{ROUTE_PRODUCT_DETAILS}")

    expect(page).to_have_url(re.compile(r"/product_details/"))
    expect(page.locator(".product-information")).to_be_visible()
    expect(page.locator("#quantity")).to_have_value("1")


def test_product_review_can_be_submitted(page: Page, app_url: str):
    page.goto(f"{app_url}{ROUTE_PRODUCT_DETAILS}")
    page.locator("#name").fill(REVIEW_NAME)
    page.locator("#email").fill(REVIEW_EMAIL)
    page.locator("#review").fill(REVIEW_TEXT)
    page.get_by_role("button", name="Submit").click()

    expect(page.get_by_text(TEXT_REVIEW_SUBMITTED)).to_be_visible()


def test_category_and_brand_filters_open(page: Page, app_url: str):
    page.goto(f"{app_url}{ROUTE_CATEGORY_PRODUCTS}")
    expect(page).to_have_url(re.compile(r"category_products"))

    page.goto(f"{app_url}{ROUTE_PRODUCTS}")
    page.goto(f"{app_url}{ROUTE_BRAND_POLO}")
    expect(page).to_have_url(re.compile(r"brand_products"))


def test_cart_shows_product_price_quantity_and_total(page: Page, app_url: str):
    add_product_to_cart(page, app_url)
    row = page.locator("#cart_info_table tbody tr").first

    expect(row).to_contain_text(PRODUCT_GREEN_TSHIRT)
    expect(row.locator(".cart_price")).to_be_visible()
    expect(row.locator(".cart_quantity")).to_contain_text("1")
    expect(row.locator(".cart_total")).to_be_visible()


def test_checkout_requires_login(page: Page, app_url: str):
    add_product_to_cart(page, app_url)
    page.locator(".check_out").click()

    expect(
        page.get_by_text(TEXT_CHECKOUT_LOGIN_REQUIRED)
    ).to_be_visible()


def test_contact_form_can_be_submitted(page: Page, app_url: str):
    page.goto(app_url)
    page.get_by_role("link", name=TEXT_CONTACT_US).click()
    page.locator("input[name='name']").fill(REVIEW_NAME)
    page.locator("input[name='email']").fill(REVIEW_EMAIL)
    page.locator("input[name='subject']").fill(CONTACT_SUBJECT)
    page.locator("textarea[name='message']").fill(CONTACT_MESSAGE)

    page.locator("#contact-us-form input[data-qa='submit-button']").click()

    expect(page).to_have_url(re.compile(r"/contact_us"))
    expect(page.locator("#contact-us-form")).to_be_visible()


def test_subscription_can_be_submitted(page: Page, app_url: str):
    page.goto(app_url)
    page.locator("#susbscribe_email").fill(SUBSCRIPTION_EMAIL)
    page.locator("#subscribe").click()

    expect(page.get_by_text(TEXT_SUBSCRIBED)).to_be_visible()


def test_empty_payment_form_does_not_complete_order(authenticated_page: Page, app_url: str):
    add_product_to_cart(authenticated_page, app_url)
    authenticated_page.locator(".check_out").click()
    authenticated_page.get_by_role("link", name=TEXT_PLACE_ORDER).click()
    authenticated_page.locator("#submit").click()

    expect(authenticated_page.locator("input[name='name_on_card']")).to_be_visible()
    expect(authenticated_page).to_have_url(re.compile(r"/payment"))


