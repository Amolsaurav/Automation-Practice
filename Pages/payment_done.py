from Pages.basePage import BasePage
from playwright.sync_api import Page
from utilities.constants import TEXT_CONTINUE, TEXT_DOWNLOAD_INVOICE


class PaymentDone(BasePage):
    def __init__(self,page:Page):
        super().__init__(page)
        self.download_invoice_btn = self.page.get_by_role('link',name=TEXT_DOWNLOAD_INVOICE)
        self.continue_btn = self.page.get_by_role('link',name = TEXT_CONTINUE)
    
    def download_invoice(self):
        self.click(self.download_invoice_btn)
    
    def continue_next(self):
        from Pages.dashboard import Dashboard

        self.click(self.continue_btn)
        dashboard_page = Dashboard(self.page)
        return dashboard_page
    
        