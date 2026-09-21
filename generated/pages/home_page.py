from generated.pages.base_page import BasePage

class HomePage(BasePage):
    def navigate_to(self):
        self.navigate("https://automationexercise.com")

    def click_signup_login(self):
        self.page.locator("header a[href='/login']").click()

    def click_cart(self):
        self.page.locator("header a[href='/view_cart']").click()

    def click_products(self):
        self.page.locator("header a[href='/products']").click()

    def click_contact_us(self):
        self.page.locator("header a[href='/contact_us']").click()

    def click_test_cases(self):
        self.page.locator("header a[href='/test_cases']").click()

    def click_logout(self):
        self.page.locator("header a[href='/logout']").click()

    def click_delete_account(self):
        self.page.locator("header a[href='/delete_account']").click()

    def is_logged_in_as(self, name: str) -> bool:
        return self.page.locator("header").get_by_text(f"Logged in as {name}").is_visible()

    def is_logged_out(self) -> bool:
        return not self.page.locator("header a[href='/logout']").is_visible()

    def subscribe(self, email: str):
        self.page.locator("#susbscribe_email").fill(email)
        self.page.locator("#subscribe").click()

    def get_subscription_success_message(self) -> str:
        return self.page.locator("#success-subscribe").text_content()

    def scroll_to_bottom(self):
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self):
        self.page.evaluate("window.scrollTo(0, 0)")

    def is_footer_visible(self) -> bool:
        return self.page.locator("#footer").is_visible()

    def click_scroll_up(self):
        self.page.locator("#scrollUp").click()

    def is_header_logo_visible(self) -> bool:
        return self.page.locator(".logo img").is_visible()

    def click_recommended_item_add_to_cart(self):
        self.page.locator("#recommended-item-carousel .add-to-cart:visible").first.click()
