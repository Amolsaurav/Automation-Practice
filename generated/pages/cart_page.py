from generated.pages.base_page import BasePage

class CartPage(BasePage):
    def get_cart_items_count(self) -> int:
        return self.page.locator("#cart_info_table tbody tr").count()

    def get_item_name(self, index: int) -> str:
        return self.page.locator("#cart_info_table tbody tr").nth(index).locator(".cart_description h4 a").text_content()

    def get_item_price(self, index: int) -> str:
        return self.page.locator("#cart_info_table tbody tr").nth(index).locator(".cart_price p").text_content()

    def get_item_quantity(self, index: int) -> str:
        return self.page.locator("#cart_info_table tbody tr").nth(index).locator(".cart_quantity button").text_content()

    def get_item_total(self, index: int) -> str:
        return self.page.locator("#cart_info_table tbody tr").nth(index).locator(".cart_total_price").text_content()

    def remove_item(self, index: int):
        self.page.locator("#cart_info_table tbody tr").nth(index).locator(".cart_quantity_delete").click()

    def click_proceed_to_checkout(self):
        self.page.locator(".check_out").click()

    def click_register_login_modal(self):
        modal = self.page.locator("#checkoutModal:visible, .modal-checkout:visible").first
        modal.locator("a[href='/login'], a:has-text('Register / Login')").first.click()

    def is_cart_empty(self) -> bool:
        return self.page.locator("#empty_cart").is_visible() or self.page.locator("#cart_info_table tbody tr").count() == 0

    def subscribe(self, email: str):
        self.page.locator("#susbscribe_email").fill(email)
        self.page.locator("#subscribe").click()

    def get_subscription_success_message(self) -> str:
        return self.page.locator("#success-subscribe").text_content()
