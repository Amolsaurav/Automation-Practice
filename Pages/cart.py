from Pages.basePage import BasePage
from Pages.checkout import Checkout
from playwright.sync_api import Page,expect
from utilities.constants import TEXT_PROCEED_TO_CHECKOUT
class Cart(BasePage):
    def __init__(self,page:Page):
        super().__init__(page)
        self.delete_btn = self.page.locator('.cart_quantity_delete')
        self.checkout_btn = self.page.locator('.check_out',has_text=TEXT_PROCEED_TO_CHECKOUT)
        
    def remove_first_item(self):
        self.click(self.delete_btn.first)
    
    def proceed_to_checkout(self):
        self.click(self.checkout_btn)
        checkout_page = Checkout(self.page)
        return checkout_page
    
    def remove_all_items(self):
       while self.delete_btn.count() > 0:
            current = self.delete_btn.count()
            self.click(self.delete_btn.first)
            expect(self.delete_btn).to_have_count(current - 1)