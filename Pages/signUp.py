from Pages.basePage import BasePage
from Pages.register import Register
class SignUp(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.signup_link = self.page.get_by_role('link',name='Signup / Login')
        self.signup_Form = self.page.locator('.signup-form')
        self.username = self.signup_Form.get_by_role('textbox',name='Name')
        self.email = self.signup_Form.get_by_role('textbox', name='Email Address')
        self.submit = self.signup_Form.get_by_role('button')
    def open_signup(self):
        self.click(self.signup_link)
        
    def sign_up_user(self,data):
        self.fill(self.username,data['username'])
        self.fill(self.email,data['email'])
        self.click(self.submit)
        registrationPage = Register(self.page)
        return registrationPage