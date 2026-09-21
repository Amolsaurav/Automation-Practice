from generated.pages.base_page import BasePage

class ContactUsPage(BasePage):
    def fill_contact_form(self, name: str, email: str, subject: str, message: str, file_path: str = None):
        self.page.locator("[data-qa='name']").fill(name)
        self.page.locator("[data-qa='email']").fill(email)
        self.page.locator("[data-qa='subject']").fill(subject)
        self.page.locator("[data-qa='message']").fill(message)
        if file_path:
            self.page.locator("input[name='upload_file']").set_input_files(file_path)

    def submit(self):
        def handle_dialog(dialog):
            dialog.accept()
        self.page.on("dialog", handle_dialog)
        self.page.locator("[data-qa='submit-button']").click()

    def get_success_message(self) -> str:
        return self.page.locator(".status.alert-success").text_content()
