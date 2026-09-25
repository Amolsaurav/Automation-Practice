from generated.pages.base_page import BasePage

class ProductsPage(BasePage):
    def is_products_list_visible(self) -> bool:
        return self.page.locator(".features_items").is_visible()

    def search_product(self, term: str):
        self.page.locator("#search_product").fill(term)
        self.page.locator("#submit_search").click()

    def get_product_cards_count(self) -> int:
        return self.page.locator(".features_items .col-sm-4").count()

    def click_view_product_of_first(self):
        self.page.locator("a[href^='/product_details/']").first.click()

    def add_first_product_to_cart(self):
        self.page.locator(".features_items .add-to-cart").first.click()

    def click_continue_shopping(self):
        self.page.locator(".modal-confirm:visible button[data-dismiss='modal']").click()

    def click_view_cart_from_modal(self):
        self.page.locator(".modal-confirm:visible a[href='/view_cart']").click()

    def click_category(self, parent: str, subcategory: str):
        self.page.locator(f"a[href='#{parent}']").click()
        self.page.locator(f"#{parent} a[href*='/category_products/']").filter(
            has_text=subcategory
        ).click()

    def click_brand(self, brand_name: str):
        self.page.locator(f"a[href='/brand_products/{brand_name}']").click()

    def get_category_title(self) -> str:
        return self.page.locator(".features_items .title").text_content()
