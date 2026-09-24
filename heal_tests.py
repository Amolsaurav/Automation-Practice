import difflib
import json
import os
import re
import sys
import traceback

from google import genai

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_DIR, "generated")
RESULTS_FILE = os.path.join(PROJECT_DIR, "results_summary.json")


def load_env_file():
    env_path = os.path.join(PROJECT_DIR, ".env")
    if not os.path.exists(env_path):
        return

    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
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
    except Exception as exc:
        print(f"[AI Test Healer] Could not read .env file: {exc}")


def resolve_issue_file(issue):
    file_value = (issue.get("file") or "").strip()
    if file_value:
        candidates = [
            file_value,
            os.path.join(PROJECT_DIR, file_value),
            os.path.join(OUTPUT_DIR, file_value),
        ]
        for candidate in candidates:
            if os.path.exists(candidate):
                return os.path.abspath(candidate)

    description = issue.get("description", "")
    match = re.search(
        r"((?:generated[\\/])?(?:pages|tests)[\\/][\w.\\/-]+\.py)",
        description,
    )
    if match:
        relative_path = match.group(1).replace("/", os.sep).replace("\\", os.sep)
        if relative_path.startswith("generated" + os.sep):
            relative_path = relative_path[len("generated" + os.sep):]
        candidate = os.path.join(OUTPUT_DIR, relative_path)
        if os.path.exists(candidate):
            return os.path.abspath(candidate)

    test_name = (issue.get("test") or "").lower()
    test_function = re.search(r"(test_[a-z0-9_]+)", test_name)
    if test_function:
        for root, _, files in os.walk(os.path.join(OUTPUT_DIR, "tests")):
            for file_name in files:
                if not file_name.endswith(".py"):
                    continue
                candidate = os.path.join(root, file_name)
                with open(candidate, "r", encoding="utf-8") as test_file:
                    if f"def {test_function.group(1)}" in test_file.read().lower():
                        return os.path.abspath(candidate)

    page_candidates = []
    if "login" in test_name:
        page_candidates.append("login_page.py")
    if "checkout" in test_name or "missing_info" in test_name:
        page_candidates.append("checkout_page.py")
    if "cart" in test_name or "backpack" in test_name:
        page_candidates.append("cart_page.py")
    for page_name in page_candidates:
        candidate = os.path.join(OUTPUT_DIR, "pages", page_name)
        if os.path.exists(candidate):
            return os.path.abspath(candidate)

    return None


def extract_python_code(response_text):
    text = response_text.strip()
    fenced = re.search(r"```(?:python|py)?\s*\n(.*?)```", text, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        return fenced.group(1).strip()

    code_start = re.search(r"(?m)^(?:from |import |class |def |async def |if )", text)
    if code_start:
        return text[code_start.start():].strip()

    return text


def main():
    load_env_file()

    if os.path.exists(os.path.join(PROJECT_DIR, ".env")):
        env_key = os.environ.get("GEMINI_API_KEY")
        if env_key:
            print(f"[AI Test Healer] Using GEMINI_API_KEY from .env file: {env_key[:6]}...{env_key[-2:]}")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[AI Test Healer] GEMINI_API_KEY not set in environment - skipping automatic test fixes.")
        sys.exit(0)

    try:
        gemini = genai.Client(api_key=api_key)
    except Exception as exc:
        print(f"[AI Test Healer] Failed to initialize Gemini client: {exc}")
        traceback.print_exc()
        sys.exit(0)

    if not os.path.exists(RESULTS_FILE):
        print(f"[AI Test Healer] {RESULTS_FILE} not found - nothing to fix.")
        sys.exit(0)

    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        issues = json.load(f)

    if isinstance(issues, dict):
        issues = issues.get("issues", [])
    if not isinstance(issues, list):
        issues = []

    fixable_issues = [
        issue for issue in issues
        if isinstance(issue, dict)
        and issue.get("type") in {"locator_issue", "test_failure", "test_error"}
    ]

    if not fixable_issues:
        print("No fixable test issues found.")
        sys.exit(0)

    for issue in fixable_issues:
        issue_title = issue.get("title") or issue.get("test")
        print(f"\n=== {issue_title} ===\n{issue['description']}")

        file_path = resolve_issue_file(issue)
        if not file_path:
            print("Couldn't find a file for this issue — skipping.")
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            old_code = f.read()

        prompt = f"""A generated automated test failed. Repair the test suite code in the file below.
The issue category is: {issue.get('type', 'test_failure')}

Failure details:
{issue['description']}

File:
{old_code}

Fix the root cause in the generated test suite, page object, or test data as appropriate.
Do not modify the external website, production behavior, or unrelated files.
Preserve the intended assertion and test coverage. Do not hide the failure by deleting or weakening assertions.
If the failure is solely caused by a temporary external service outage and no test-code fix is justified, return the original code unchanged.
Return only the corrected Python code, nothing else."""

        try:
            response = gemini.models.generate_content(model="gemini-3.6-flash", contents=prompt)
            new_code = extract_python_code(response.text)
            compile(new_code, file_path, "exec")
        except Exception as exc:
            print(f"[AI Test Healer] Gemini response rejected for {issue['test']}: {exc}")
            traceback.print_exc()
            continue

        diff = difflib.unified_diff(old_code.splitlines(), new_code.splitlines(), lineterm="")
        print("\n".join(diff))

        if input("\nApply this fix? [y/N] ").strip().lower() == "y":
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_code + "\n")
            print(f"Updated {file_path}")
        else:
            print("Skipped.")

    print("\nDone. Re-run pytest to confirm.")


if __name__ == "__main__":
    main()
