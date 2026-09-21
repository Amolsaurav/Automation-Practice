from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        last_error = None
        for _ in range(3):
            try:
                self.page.goto(url, wait_until="domcontentloaded", timeout=30000)
                return
            except PlaywrightTimeoutError as exc:
                last_error = exc
        if last_error:
            raise last_error

    def click(self, selector: str):
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str):
        self.page.locator(selector).fill(value)

    def wait(self, milliseconds: float):
        self.page.wait_for_timeout(milliseconds)

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()
