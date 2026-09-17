from Pages.basePage import BasePage
from Pages.payment_done import PaymentDone
from playwright.sync_api import Page
class Payment(BasePage):
    def __init__(self,page:Page):
        super().__init__(page)
        self.payment_form = self.page.locator('#payment-form')
        self.input_name = self.payment_form.locator("[name='name_on_card']")
        self.input_card_number = self.payment_form.locator("[name='card_number']")
        self.cvc = self.payment_form.locator("[name='cvc']")
        self.exp_month = self.payment_form.locator("[name='expiry_month']")
        self.exp_year = self.payment_form.locator("[name='expiry_year']")
        self.submit_btn = self.payment_form.locator("#submit")
    
    def submit_paymentForm(self,name,card_number,cvc,exp_month,exp_year):
        self.fill(self.input_name,name)
        self.fill(self.input_card_number,card_number)
        self.fill(self.cvc,cvc)
        self.fill(self.exp_month,exp_month)
        self.fill(self.exp_year,exp_year)
        self.click(self.submit_btn)
        payment_done = PaymentDone(self.page)
        return payment_done
    