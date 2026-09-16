from Pages.basePage import BasePage
from playwright.sync_api import Page


class PaymentDone(BasePage):
    def __init__(self,page:Page):
        super().__init__(page)
        self.download_invoice_btn = self.page.get_by_role('link',name='Download Invoice')
        self.continue_btn = self.page.get_by_role('link',name = 'Continue')
    
    def download_invoice(self):
        self.click(self.download_invoice_btn)
    
    def continue_next(self):
        from Pages.dashboard import Dashboard

        self.click(self.continue_btn)
        dashboard_page = Dashboard(self.page)
        return dashboard_page
    
        