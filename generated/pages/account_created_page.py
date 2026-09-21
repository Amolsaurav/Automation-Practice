from generated.pages.base_page import BasePage

class AccountCreatedPage(BasePage):
    def is_account_created_visible(self) -> bool:
        return self.page.locator("[data-qa='account-created']").is_visible()

    def is_account_deleted_visible(self) -> bool:
        return self.page.locator("[data-qa='account-deleted']").is_visible()

    def click_continue(self):
        try:
            self.page.locator("[data-qa='continue-button']").click(timeout=5000)
        except Exception:
            pass
        if "google_vignette" in self.page.url or "googleads" in self.page.url:
            self.page.goto("https://automationexercise.com")
        if not self.page.locator("header").is_visible():
            self.page.goto("https://automationexercise.com")
