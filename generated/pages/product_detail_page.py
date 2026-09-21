from generated.pages.base_page import BasePage

class ProductDetailPage(BasePage):
    def get_product_name(self) -> str:
        return self.page.locator(".product-information h2").text_content()

    def get_product_category(self) -> str:
        return self.page.locator(".product-information p:has-text('Category:')").text_content()

    def get_product_price(self) -> str:
        return self.page.locator(".product-information span span").text_content()

    def get_product_availability(self) -> str:
        return self.page.locator(".product-information p:has-text('Availability:')").text_content()

    def get_product_condition(self) -> str:
        return self.page.locator(".product-information p:has-text('Condition:')").text_content()

    def get_product_brand(self) -> str:
        return self.page.locator(".product-information p:has-text('Brand:')").text_content()

    def submit_review(self, name: str, email: str, review: str):
        self.page.locator("#name").fill(name)
        self.page.locator("#email").fill(email)
        self.page.locator("#review").fill(review)
        self.page.locator("#button-review").click()

    def get_review_success_message(self) -> str:
        return self.page.locator("#review-section .alert-success").text_content()

    def set_quantity(self, qty: int):
        self.page.locator("#quantity").fill(str(qty))

    def add_to_cart(self):
        self.page.locator("button.cart").click()

    def get_quantity_input_min(self) -> str:
        return self.page.locator("#quantity").get_attribute("min")
