from generated.pages.base_page import BasePage

class PaymentPage(BasePage):
    def fill_payment_details(self, name: str, card_num: str, cvc: str, exp_month: str, exp_year: str):
        self.page.locator("[data-qa='name-on-card']").fill(name)
        self.page.locator("[data-qa='card-number']").fill(card_num)
        self.page.locator("[data-qa='cvc']").fill(cvc)
        self.page.locator("[data-qa='expiry-month']").fill(exp_month)
        self.page.locator("[data-qa='expiry-year']").fill(exp_year)

    def click_pay_and_confirm(self):
        self.page.locator("[data-qa='pay-button']").click()
