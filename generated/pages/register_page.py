from generated.pages.base_page import BasePage

class RegisterPage(BasePage):
    def fill_account_details(self, gender: str, password: str, day: str, month: str, year: str):
        if gender.lower() == "mr":
            self.page.locator("#id_gender1").check()
        else:
            self.page.locator("#id_gender2").check()
        self.page.locator("[data-qa='password']").fill(password)
        self.page.locator("[data-qa='days']").select_option(day)
        self.page.locator("[data-qa='months']").select_option(month)
        self.page.locator("[data-qa='years']").select_option(year)

    def fill_address_details(self, first_name: str, last_name: str, company: str, address1: str, address2: str, country: str, state: str, city: str, zipcode: str, mobile: str):
        self.page.locator("[data-qa='first_name']").fill(first_name)
        self.page.locator("[data-qa='last_name']").fill(last_name)
        self.page.locator("[data-qa='company']").fill(company)
        self.page.locator("[data-qa='address']").fill(address1)
        self.page.locator("[data-qa='address2']").fill(address2)
        self.page.locator("[data-qa='country']").select_option(country)
        self.page.locator("[data-qa='state']").fill(state)
        self.page.locator("[data-qa='city']").fill(city)
        self.page.locator("[data-qa='zipcode']").fill(zipcode)
        self.page.locator("[data-qa='mobile_number']").fill(mobile)

    def click_create_account(self):
        self.page.locator("[data-qa='create-account']").click()
