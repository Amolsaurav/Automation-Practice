from generated.pages.base_page import BasePage

class CheckoutPage(BasePage):
    def get_delivery_address(self) -> str:
        return self.page.locator("#address_delivery").text_content()

    def get_billing_address(self) -> str:
        return self.page.locator("#address_invoice").text_content()

    def enter_description(self, text: str):
        self.page.locator("textarea[name='message']").fill(text)

    def click_place_order(self):
        self.page.locator("a[href='/payment']").click()

    def is_checkout_loaded(self) -> bool:
        return (
            self.page.locator("a[href='/payment']").is_visible()
            or self.page.locator("#address_delivery").is_visible()
            or "checkout" in self.page.url
        )
