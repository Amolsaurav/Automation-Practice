from generated.pages.base_page import BasePage

class OrderPlacementPage(BasePage):
    def is_order_placed_visible(self) -> bool:
        return self.page.locator("[data-qa='order-placed']").is_visible()

    def download_invoice(self) -> str:
        with self.page.expect_download() as download_info:
            self.page.locator("a[href='/download_invoice']").click()
        download = download_info.value
        path = download.path()
        return path

    def click_continue(self):
        self.page.locator("[data-qa='continue-button']").click()
