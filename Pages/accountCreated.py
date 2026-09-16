from Pages.basePage import BasePage


class AccountCreated(BasePage):
    def __init__(self,page):
        super().__init__(page)
    def naviagte_to_dashboard(self):
        from Pages.dashboard import Dashboard

        self.click(self.page.get_by_role('link',name = 'Continue'))
        dashboardPage = Dashboard(self.page)
        return dashboardPage