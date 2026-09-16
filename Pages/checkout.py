from Pages.basePage import BasePage
from Pages.payment import Payment
from playwright.sync_api import Page
class Checkout(BasePage):
    def __init__(self,page:Page):
        super().__init__(page)
        self.comment_box  = self.page.locator('textarea')
        self.place_order_btn = self.page.get_by_role('link',name='Place Order')
    
    def place_order(self,message:str):
        self.fill(self.comment_box,message)
        self.click(self.place_order_btn)
        payment_page = Payment(self.page)
        return payment_page
    