from playwright.sync_api import Page, expect
import pytest

from Pages.signUp import SignUp
from utilities.data_loader import DataLoader

data = DataLoader.load_json("registration.json")


@pytest.mark.parametrize(
    "registration_data",
    data["valid_registration"],
    ids=[user["id"] for user in data["valid_registration"]]
)
def test_valid_register(page: Page, app_url, registration_data):
    page.goto(app_url)
    sign_up = SignUp(page)
    sign_up.open_signup()
    expect(page.get_by_text('New User Signup!')).to_be_visible()
    register_page = sign_up.sign_up_user(registration_data)
    
    expect(page.get_by_text('Enter Account Information')).to_be_visible()
    register_page.fillForm(registration_data)
    account_page = register_page.createAccount()
    expect(page.get_by_text('ACCOUNT CREATED!')).to_be_visible()
    dashboard_page = account_page.naviagte_to_dashboard()
    expect(page.get_by_text(f"Logged in as {registration_data['username']}")) \
        .to_be_visible()
    dashboard_page.delete_account()
    expect(page.get_by_text('ACCOUNT DELETED!')).to_be_visible()

@pytest.mark.parametrize(
    "registration_data",
    data["invalid_registration"],
    ids=[user["id"] for user in data["invalid_registration"]]
)   
def test_invalid_register(page: Page, app_url, registration_data):
    page.goto(app_url)
    sign_up = SignUp(page)
    sign_up.open_signup()
    expect(page.get_by_text('New User Signup!')).to_be_visible()
    register_page = sign_up.sign_up_user(registration_data)
    if registration_data["id"] in {"IR001", "IR002"}:
        expect(page).to_have_url(f"{app_url}/login")
    else:
        expect(
            page.get_by_text(registration_data["expected_error"])
        ).to_be_visible()