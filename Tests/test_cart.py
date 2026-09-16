from playwright.sync_api import Page, expect
from utilities.constants import (
    PRODUCT_BLUE_JEANS,
    PRODUCT_GREEN_TSHIRT,
    ROUTE_BRAND_POLO,
    TEXT_ADD_TO_CART,
    TEXT_CONTINUE_SHOPPING,
    TEXT_VIEW_CART,
)

def add_two_prodcuts(page: Page, app_url: str):
    page.goto(f'{app_url}{ROUTE_BRAND_POLO}')
    product1 = page.locator('.productinfo',has_text=PRODUCT_GREEN_TSHIRT)
    product1.get_by_role('link',name=TEXT_ADD_TO_CART).click(force=True)
    modal = page.locator('.modal-content:visible')
    expect(modal).to_be_visible()
    modal.get_by_role('button', name=TEXT_CONTINUE_SHOPPING).click()
    product2 = page.locator('.productinfo',has_text=PRODUCT_BLUE_JEANS)
    product2.get_by_role('link',name=TEXT_ADD_TO_CART).click(force=True)
    expect(modal).to_be_visible()
    modal.get_by_role('link', name=TEXT_VIEW_CART).click()
    delete_buttons = page.locator('.cart_quantity_delete')
    expect(delete_buttons).to_have_count(2)

    while delete_buttons.count() > 0:
        current = delete_buttons.count()
        delete_buttons.first.click()
        expect(delete_buttons).to_have_count(current - 1)

def test_addCart(page: Page, app_url: str):
    add_two_prodcuts(page, app_url)
    expect(page.locator("#cart_info_table tbody tr")).to_have_count(0)
    

def test_deleteCart(page: Page, app_url: str):
       
    page.goto(f'{app_url}{ROUTE_BRAND_POLO}')
    product1 = page.locator('.productinfo',has_text=PRODUCT_GREEN_TSHIRT)
    product1.get_by_role('link',name=TEXT_ADD_TO_CART).click(force=True)
    modal = page.locator('.modal-content:visible')
    expect(modal).to_be_visible()
    modal.get_by_role('link', name=TEXT_VIEW_CART).click()
    expect(page.locator("#cart_info_table tbody tr")).to_have_count(1)
    page.locator('.cart_quantity_delete').click()
    expect(page.locator("#cart_info_table tbody tr")).to_have_count(0)
    expect(page.get_by_text('Cart is empty!')).to_be_visible()

