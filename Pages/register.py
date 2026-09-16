from playwright.sync_api import Page
from Pages.basePage import BasePage
from utilities.constants import TEXT_CREATE_ACCOUNT


class Register(BasePage):
    def __init__(self,page:Page):
        super().__init__(page)
        self.registerForm = self.page.locator('form')
        self.gender = self.registerForm.locator('#uniform-id_gender1')
        self.name = self.registerForm.locator('#name')
        self.password = self.registerForm.locator('#password')
        self.days = self.registerForm.locator('#days')
        self.month = self.registerForm.locator('#months')
        self.year = self.registerForm.locator('#years')
        self.first_name = self.registerForm.locator('#first_name')
        self.last_name = self.registerForm.locator('#last_name')
        self.company = self.registerForm.locator('#company')
        self.address = self.registerForm.locator('#address1')
        self.country = self.registerForm.locator('#country')
        self.state = self.registerForm.locator('#state')
        self.city = self.registerForm.locator('#city')
        self.zipcode = self.registerForm.locator('#zipcode')
        self.mobile = self.registerForm.locator('#mobile_number')
        
        self.createButton = self.registerForm.get_by_role('button',name=TEXT_CREATE_ACCOUNT)
    
    def fillForm(self,registrationData):
        self.check(self.gender)
        self.fill(self.name,registrationData['username'])
        self.fill(self.password,registrationData['password'])
        self.select_option(self.days,value=registrationData['day'])
        self.select_option(self.month,value=registrationData['month'])
        self.select_option(self.year,value=registrationData['year'])
        self.fill(self.first_name,registrationData['first_name'])
        self.fill(self.last_name,registrationData['last_name'])
        self.fill(self.company,registrationData['company'])
        self.fill(self.address,registrationData['address'])
        self.select_option(self.country,value=registrationData['country'])
        self.fill(self.state,registrationData['state'])
        self.fill(self.city,registrationData['city'])
        self.fill(self.zipcode,registrationData['zipcode'])
        self.fill(self.mobile,registrationData['mobile'])
    
    def createAccount(self):
        from Pages.accountCreated import AccountCreated

        self.click(self.createButton)
        accountPage = AccountCreated(self.page)
        return accountPage
    
    