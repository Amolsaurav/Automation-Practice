from generated.pages.base_page import BasePage

class SignupLoginPage(BasePage):
    def signup(self, name: str, email: str):
        self.page.locator("[data-qa='signup-name']").fill(name)
        self.page.locator("[data-qa='signup-email']").fill(email)
        self.page.locator("[data-qa='signup-button']").click()

    def login(self, email: str, password: str):
        self.page.locator("[data-qa='login-email']").fill(email)
        self.page.locator("[data-qa='login-password']").fill(password)
        self.page.locator("[data-qa='login-button']").click()

    def get_signup_error(self) -> str:
        return self.page.locator("form[action='/signup'] p").text_content()

    def get_login_error(self) -> str:
        return self.page.locator("form[action='/login'] p").text_content()
