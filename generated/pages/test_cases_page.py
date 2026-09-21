from generated.pages.base_page import BasePage

class TestCasesPage(BasePage):
    def is_test_cases_visible(self) -> bool:
        return self.page.locator("section#form").is_visible() or self.page.locator("span:has-text('Test Cases')").first.is_visible()
