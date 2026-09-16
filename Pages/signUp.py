from Pages.basePage import BasePage
from Pages.register import Register
from utilities.constants import TEXT_EMAIL_ADDRESS, TEXT_NAME, TEXT_SIGNUP_LOGIN
class SignUp(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.signup_link = self.page.get_by_role('link',name=TEXT_SIGNUP_LOGIN)
        self.signup_Form = self.page.locator('.signup-form')
        self.username = self.signup_Form.get_by_role('textbox',name=TEXT_NAME)
        self.email = self.signup_Form.get_by_role('textbox', name=TEXT_EMAIL_ADDRESS)
        self.submit = self.signup_Form.get_by_role('button')
    def open_signup(self):
        self.click(self.signup_link)
        
    def sign_up_user(self,data):
        self.fill(self.username,data['username'])
        self.fill(self.email,data['email'])
        self.click(self.submit)
        registrationPage = Register(self.page)
        return registrationPage