import os
import pytest
import json
import traceback
import xml.etree.ElementTree as ET
from google import genai
from google.genai import types
from pydantic import BaseModel
from generated.pages.home_page import HomePage
from generated.pages.signup_login_page import SignupLoginPage
from generated.pages.register_page import RegisterPage
from generated.pages.account_created_page import AccountCreatedPage
from generated.pages.contact_us_page import ContactUsPage
from generated.pages.products_page import ProductsPage
from generated.pages.product_detail_page import ProductDetailPage
from generated.pages.cart_page import CartPage
from generated.pages.checkout_page import CheckoutPage
from generated.pages.payment_page import PaymentPage
from generated.pages.order_placement_page import OrderPlacementPage
from generated.pages.test_cases_page import TestCasesPage

CURRENT_TEST_ISSUES = []
CURRENT_TEST_COUNT = 0

@pytest.fixture(scope="session")
def base_url():
    return "https://automationexercise.com"

@pytest.fixture
def page(context):
    # Route to block common Google Ads and trackers to stabilize Automation Exercise tests
    def handle_route(route):
        url = route.request.url
        if any(x in url for x in ["google", "doubleclick", "adservice", "analytics", "pagead"]):
            route.abort()
        else:
            route.continue_()
    context.route("**/*", handle_route)
    p = context.new_page()
    p.set_default_timeout(15000)
    yield p
    p.close()

@pytest.fixture
def home_page(page):
    return HomePage(page)

@pytest.fixture
def signup_login_page(page):
    return SignupLoginPage(page)

@pytest.fixture
def register_page(page):
    return RegisterPage(page)

@pytest.fixture
def account_created_page(page):
    return AccountCreatedPage(page)

@pytest.fixture
def contact_us_page(page):
    return ContactUsPage(page)

@pytest.fixture
def products_page(page):
    return ProductsPage(page)

@pytest.fixture
def product_detail_page(page):
    return ProductDetailPage(page)

@pytest.fixture
def cart_page(page):
    return CartPage(page)

@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)

@pytest.fixture
def payment_page(page):
    return PaymentPage(page)

@pytest.fixture
def order_placement_page(page):
    return OrderPlacementPage(page)

@pytest.fixture
def test_cases_page(page):
    return TestCasesPage(page)


def load_env_file():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    if not os.path.exists(env_path):
        return

    try:
        with open(env_path, "r", encoding="utf-8") as env_file:
            for line in env_file:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key == "GEMINI_API_KEY":
                    os.environ[key] = value
                else:
                    os.environ.setdefault(key, value)
    except OSError as exc:
        print(f"[AI Logging] Could not read .env file: {exc}")


def write_local_summary(xml_path):
    issues = []
    try:
        root = ET.parse(xml_path).getroot()
        for testcase in root.iter("testcase"):
            failure = testcase.find("failure")
            error = testcase.find("error")
            problem = failure if failure is not None else error
            if problem is not None:
                issues.append({
                    "test": testcase.get("name", "unknown"),
                    "type": "test_failure" if failure is not None else "test_error",
                    "description": problem.get("message") or (problem.text or "").strip(),
                })
    except (ET.ParseError, OSError) as exc:
        issues.append({
            "test": "pytest_session",
            "type": "summary_error",
            "description": str(exc),
        })

    output_dir = os.path.dirname(os.path.abspath(xml_path))
    with open(os.path.join(output_dir, "test_log.md"), "w", encoding="ascii", errors="ignore") as log_file:
        log_file.write("# Test Run Summary\n\n")
        log_file.write(f"Detected {len(issues)} test issue(s) from results.xml.\n")

    with open(os.path.join(output_dir, "results_summary.json"), "w", encoding="ascii", errors="ignore") as summary_file:
        json.dump({"issues": issues}, summary_file, indent=2)

    return issues


def pytest_runtest_logreport(report):
    global CURRENT_TEST_COUNT
    if report.when != "call":
        return
    CURRENT_TEST_COUNT += 1
    if report.passed:
        return
    CURRENT_TEST_ISSUES.append({
        "test": report.nodeid,
        "type": "test_failure" if report.failed else "test_error",
        "description": str(report.longrepr),
    })


def pytest_sessionfinish(session, exitstatus):
    if os.environ.get("SKIP_AUTO_LOG"):
        return
    results_path = os.path.join(os.getcwd(), "results.xml")
    if not os.path.exists(results_path):
        return

    load_env_file()
    local_issues = list(CURRENT_TEST_ISSUES)
    if not local_issues and CURRENT_TEST_COUNT == 0:
        local_issues = write_local_summary(results_path)
    else:
        output_dir = os.path.dirname(os.path.abspath(results_path))
        with open(os.path.join(output_dir, "test_log.md"), "w", encoding="ascii", errors="ignore") as log_file:
            log_file.write("# Test Run Summary\n\n")
            log_file.write(f"Detected {len(local_issues)} test issue(s) in this run.\n")
        with open(os.path.join(output_dir, "results_summary.json"), "w", encoding="ascii", errors="ignore") as summary_file:
            json.dump({"issues": local_issues}, summary_file, indent=2)
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[AI Logging] GEMINI_API_KEY not set in environment - skipping log generation.")
        return

    try:
        with open(results_path, "r", encoding="utf-8", errors="ignore") as f:
            xml_content = f.read()

        class TestIssue(BaseModel):
            test: str
            type: str
            description: str

        class TestSummary(BaseModel):
            summary_markdown: str
            issues: list[TestIssue]

        client = genai.Client(api_key=api_key)
        prompt = (
            "Analyze the following pytest JUnit XML results and provide a summary of the test run.\n\n"
            f"XML Content:\n{xml_content}"
        )

        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TestSummary,
            ),
        )

        data = json.loads(response.text)
        summary_md = data.get("summary_markdown", "")
        issues = data.get("issues", [])
        if not issues and local_issues:
            issues = local_issues

        output_dir = os.path.dirname(os.path.abspath(results_path))
        with open(os.path.join(output_dir, "test_log.md"), "w", encoding="ascii", errors="ignore") as f:
            f.write(summary_md)

        with open(os.path.join(output_dir, "results_summary.json"), "w", encoding="ascii", errors="ignore") as f:
            json.dump({"issues": issues}, f, indent=2)

    except Exception as e:
        print(f"[AI Logging] Error occurred: {e}")
        traceback.print_exc()
        write_local_summary(results_path)
