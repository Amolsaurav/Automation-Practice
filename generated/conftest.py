import os
import pytest
import json
import re
import tempfile
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


def humanize_test_name(raw_name):
    params = ""
    param_match = re.search(r"\[(.*?)\]$", raw_name)
    if param_match:
        params = f" ({param_match.group(1).capitalize()})"
        clean_name = raw_name[:param_match.start()]
    else:
        clean_name = raw_name

    if clean_name.startswith("test_"):
        clean_name = clean_name[5:]

    words = clean_name.split("_")
    readable = " ".join(
        word.capitalize() if word not in ("and", "or", "to", "by", "for", "in", "of", "with", "on", "from") else word
        for word in words
    )
    if readable:
        readable = readable[0].upper() + readable[1:]
    return f"{readable}{params}"


def classname_to_filepath(classname):
    if not classname:
        return "unknown"
    parts = classname.split(".")
    return "/".join(parts) + ".py"


def extract_fix_locations(classname, test_name, details):
    fix_locations = []
    test_file_path = classname_to_filepath(classname)
    clean_test_func = re.sub(r"\[.*?\]$", "", test_name)
    fix_locations.append({
        "type": "test_file",
        "path": test_file_path,
        "function": clean_test_func,
        "description": f"Test script: `{test_file_path}` (function `{clean_test_func}`)"
    })

    if not details:
        return fix_locations

    file_line_matches = re.findall(r"((?:generated[/\\](?:pages|tests)[/\\][\w/\\]+\.py):(\d+))", details)
    seen_paths = {test_file_path}
    for full_match, line_num in file_line_matches:
        norm_path = full_match.replace("\\", "/")
        if norm_path not in seen_paths:
            seen_paths.add(norm_path)
            fix_locations.append({
                "type": "stack_trace_file",
                "path": norm_path,
                "line": line_num,
                "description": f"Failure point: `{norm_path}` at line {line_num}"
            })

    page_object_matches = re.findall(r"<generated\.pages\.(\w+)\.(\w+) object", details)
    for module_name, class_name in page_object_matches:
        po_path = f"generated/pages/{module_name}.py"
        if po_path not in seen_paths:
            seen_paths.add(po_path)
            fix_locations.append({
                "type": "page_object",
                "path": po_path,
                "class": class_name,
                "description": f"Page Object class: `{po_path}` (`{class_name}`)"
            })

    return fix_locations


def summarize_failure_reason(details):
    if not details:
        return "No error details available."
    
    lines = [line.strip() for line in details.splitlines() if line.strip()]
    assertion_lines = [l for l in lines if l.startswith("E   ") or l.startswith("assert ") or "AssertionError" in l]
    if assertion_lines:
        clean_assertion = " ".join(l.replace("E   ", "").strip() for l in assertion_lines[:3])
        return f"Assertion Error: {clean_assertion}"
    
    for line in lines:
        if any(kw in line for kw in ("Error:", "Exception:", "TimeoutError", "ElementNotFound")):
            return line
            
    return lines[0] if lines else "Test execution failed."


def read_test_results(xml_path):
    tests = []
    try:
        root = ET.parse(xml_path).getroot()
        for testcase in root.iter("testcase"):
            failure = testcase.find("failure")
            error = testcase.find("error")
            skipped = testcase.find("skipped")
            if error is not None:
                status = "error"
                problem = error
            elif failure is not None:
                status = "failed"
                problem = failure
            elif skipped is not None:
                status = "skipped"
                problem = skipped
            else:
                status = "passed"
                problem = None

            details = ""
            if problem is not None:
                details = problem.get("message") or (problem.text or "").strip()

            test_name = testcase.get("name", "unknown")
            classname = testcase.get("classname", "")
            file_path = classname_to_filepath(classname)
            title = humanize_test_name(test_name)
            category = "API Test" if "api" in classname.lower() or "api" in file_path.lower() else "UI Test"

            fix_locations = extract_fix_locations(classname, test_name, details) if status in {"failed", "error"} else []
            summary_reason = summarize_failure_reason(details) if status in {"failed", "error"} else ""

            tests.append({
                "raw_test": f"{classname}::{test_name}" if classname else test_name,
                "title": title,
                "category": category,
                "file_path": file_path,
                "classname": classname,
                "test_name": test_name,
                "status": status,
                "duration_seconds": float(testcase.get("time", "0") or 0),
                "details": details,
                "summary_reason": summary_reason,
                "fix_locations": fix_locations,
            })
    except (ET.ParseError, OSError) as exc:
        return [], [{
            "test": "pytest_session",
            "type": "summary_error",
            "description": str(exc),
        }]

    issues = [
        {
            "test": test["raw_test"],
            "title": test["title"],
            "file": test["file_path"],
            "type": "test_error" if test["status"] == "error" else "test_failure",
            "description": test["details"],
            "summary_reason": test["summary_reason"],
            "fix_locations": test["fix_locations"],
        }
        for test in tests
        if test["status"] in {"failed", "error"}
    ]
    return tests, issues


def build_local_log(tests, issues):
    counts = {status: sum(test["status"] == status for test in tests) for status in ("passed", "failed", "error", "skipped")}
    total = len(tests)
    completed = counts["passed"] + counts["failed"] + counts["error"]
    pass_rate = (counts["passed"] / completed * 100) if completed else 0
    total_duration = sum(t["duration_seconds"] for t in tests)

    lines = [
        "# Automated Test Execution Summary",
        "",
        "## Overview",
        f"- **Total Tests:** {total}",
        f"- **Passed:** {counts['passed']}",
        f"- **Failed:** {counts['failed']}",
        f"- **Errors:** {counts['error']}",
        f"- **Skipped:** {counts['skipped']}",
        f"- **Pass Rate:** {pass_rate:.1f}%",
        f"- **Total Duration:** {total_duration:.2f} seconds",
        "",
    ]

    failed_tests = [t for t in tests if t["status"] in {"failed", "error"}]
    if failed_tests:
        lines.extend([
            "---",
            "",
            "## ⚠️ Failure Analysis & Search Fix Locations",
            "*(Failed tests listed first with human-readable reasons and exact file locations)*",
            "",
        ])
        for idx, test in enumerate(failed_tests, 1):
            lines.extend([
                f"### {idx}. {test['title']}",
                f"- **Category:** {test['category']}",
                f"- **Status:** {test['status'].upper()}",
                f"- **Duration:** {test['duration_seconds']:.3f}s",
                f"- **Failure Reason:** {test['summary_reason']}",
                "- **Where to Search for Fixes:**",
            ])
            for loc in test["fix_locations"]:
                lines.append(f"  - 📄 {loc['description']}")
            
            if test["details"]:
                lines.extend([
                    "- **Raw Failure Details:**",
                    "```text",
                    test["details"][:1500] + ("\n...[truncated]" if len(test["details"]) > 1500 else ""),
                    "```",
                ])
            lines.append("")

    lines.extend([
        "---",
        "",
        "## 📋 Detailed Test Case Results",
        "",
    ])

    api_tests = [t for t in tests if t["category"] == "API Test"]
    ui_tests = [t for t in tests if t["category"] == "UI Test"]

    if api_tests:
        api_passed = sum(1 for t in api_tests if t["status"] == "passed")
        lines.extend([
            f"### API Test Suite ({api_passed}/{len(api_tests)} Passed)",
            "",
        ])
        for test in api_tests:
            icon = "✅" if test["status"] == "passed" else ("❌" if test["status"] == "failed" else "⚠️")
            lines.append(f"- {icon} **{test['title']}**")
            lines.append(f"  - **File:** `{test['file_path']}` (Function: `{test['test_name']}`)")
            lines.append(f"  - **Status:** {test['status'].upper()} ({test['duration_seconds']:.3f}s)")
            if test["status"] in {"failed", "error"}:
                lines.append(f"  - **Reason:** {test['summary_reason']}")
                if test["fix_locations"]:
                    fix_paths = ", ".join(f"`{loc['path']}`" for loc in test["fix_locations"])
                    lines.append(f"  - **Fix Location:** {fix_paths}")
            lines.append("")

    if ui_tests:
        ui_passed = sum(1 for t in ui_tests if t["status"] == "passed")
        lines.extend([
            f"### UI Test Suite ({ui_passed}/{len(ui_tests)} Passed)",
            "",
        ])
        for test in ui_tests:
            icon = "✅" if test["status"] == "passed" else ("❌" if test["status"] == "failed" else "⚠️")
            lines.append(f"- {icon} **{test['title']}**")
            lines.append(f"  - **File:** `{test['file_path']}` (Function: `{test['test_name']}`)")
            lines.append(f"  - **Status:** {test['status'].upper()} ({test['duration_seconds']:.3f}s)")
            if test["status"] in {"failed", "error"}:
                lines.append(f"  - **Reason:** {test['summary_reason']}")
                if test["fix_locations"]:
                    fix_paths = ", ".join(f"`{loc['path']}`" for loc in test["fix_locations"])
                    lines.append(f"  - **Fix Location:** {fix_paths}")
            lines.append("")

    if not tests:
        lines.extend([
            "No test case records were found in results.xml.",
        ])

    return "\n".join(lines) + "\n"


def write_atomically(path, content):
    output_dir = os.path.dirname(path)
    file_descriptor, temporary_path = tempfile.mkstemp(
        prefix=f".{os.path.basename(path)}.",
        suffix=".tmp",
        dir=output_dir,
        text=True,
    )
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8", errors="replace") as output_file:
            output_file.write(content)
            output_file.flush()
            os.fsync(output_file.fileno())
        os.replace(temporary_path, path)
    except Exception:
        try:
            os.unlink(temporary_path)
        except OSError:
            pass
        raise


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


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_sessionfinish(session, exitstatus):
    yield
    if os.environ.get("SKIP_AUTO_LOG"):
        return
    output_dir = str(session.config.rootpath)
    results_path = os.path.join(output_dir, "results.xml")
    if not os.path.exists(results_path):
        return

    load_env_file()
    tests, local_issues = read_test_results(results_path)
    if not tests and CURRENT_TEST_ISSUES:
        local_issues = list(CURRENT_TEST_ISSUES)

    local_log = build_local_log(tests, local_issues)
    final_log = local_log
    final_issues = local_issues
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[AI Logging] GEMINI_API_KEY not set in environment - skipping AI log enhancement.")
    else:
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
                "Analyze the following pytest JUnit XML results and provide a clear, human-readable summary of the test run.\n"
                "IMPORTANT INSTRUCTIONS FOR FORMATTING:\n"
                "1. Convert raw test identifiers like 'generated.tests.api.test_api_suite::test_get_all_brands' into human-readable titles (e.g. 'Get All Brands').\n"
                "2. Clearly separate API Tests and UI Tests.\n"
                "3. For any failures or errors, provide a human-readable explanation of WHY it failed and specify EXACT file paths (e.g., 'generated/tests/ui/test_scenarios_2.py', 'generated/pages/cart_page.py') and line numbers where developers can search for fixes.\n"
                "4. Format the output in clean GitHub-flavored Markdown.\n\n"
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
            if summary_md.strip():
                final_log = summary_md.rstrip() + "\n\n" + local_log
        except Exception as e:
            print(f"[AI Logging] Error occurred during AI enhancement: {e}")
            traceback.print_exc()

    write_atomically(os.path.join(output_dir, "test_log.md"), final_log)
    write_atomically(
        os.path.join(output_dir, "results_summary.json"),
        json.dumps({"issues": final_issues}, indent=2),
    )
