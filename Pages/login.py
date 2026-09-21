from Pages.basePage import BasePage
from Pages.dashboard import Dashboard
from playwright.sync_api import Page
from utilities.constants import TEXT_EMAIL_ADDRESS, TEXT_LOGIN, TEXT_PASSWORD

class Login(BasePage):
    def __init__(self,page:Page):
        super().__init__(page)
        self.loginForm = self.page.locator('.login-form')
        self.emailInput = self.loginForm.get_by_role('textbox',name=TEXT_EMAIL_ADDRESS)
        self.passwordInput = self.loginForm.get_by_role('textbox',name=TEXT_PASSWORD)
        self.loginBtn = self.loginForm.get_by_role('button',name=TEXT_LOGIN)
           
    
    def login_user(self,loginData):
        self.fill(self.emailInput,loginData['email'])
        self.fill(self.passwordInput,loginData['password'])
        self.click(self.loginBtn)
        dashboard_page = Dashboard(self.page)
        return dashboard_page
    