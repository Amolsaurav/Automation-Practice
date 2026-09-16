from playwright.sync_api import Page, Locator
from Pages.basePage import BasePage
from Pages.cart import Cart


class Products(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.polo_category = self.page.get_by_role("link",name="POLO")

        self.continue_shopping_button = self.page.get_by_role("button",name="Continue Shopping")

        self.view_cart_button = self.page.get_by_role("link",name="View Cart")

    def get_product(self, product_name: str) -> Locator:
        return self.page.locator(".productinfo",has_text=product_name)

    def get_add_to_cart_button(self, product: Locator) -> Locator:
        return product.get_by_role("link",name="Add to cart")

    def open_category(self):
        self.click(self.polo_category)

    def add_to_cart(self, product_name: str):

        product = self.get_product(product_name)

        product.hover()

        add_button = self.get_add_to_cart_button(product)

        self.click(add_button)

    def continue_shopping(self):
        self.click(self.continue_shopping_button)

    def add_multiple_products(self, products: list[str]):

        for index, product_name in enumerate(products):

            self.add_to_cart(product_name)

            if index != len(products) - 1:
                self.continue_shopping()

    def go_to_cart(self):

        self.click(self.view_cart_button)

        return Cart(self.page)

    def is_product_visible(self, product_name: str) -> bool:

        return self.get_product(product_name).is_visible()

    def get_product_text(self, product_name: str) -> str:

        return self.get_product(product_name).inner_text()