# Automation Exercise Test Generation Spec

## Main rule
This file is the master specification for the project generator. It is intentionally a thin coordinator file. The real test coverage source of truth is split into separate files:
- UI requirements: ui_test_requirements.md
- API requirements: api_test_requirements.md

The generator must treat ui_test_requirements.md and api_test_requirements.md as required inputs for the same project. Do not duplicate the full UI or API list inside this file. Instead, this file defines the rules, project structure, and how the separated requirements are applied.

## Target application
- Base URL: https://automationexercise.com
- Environment: production
- Authentication: use the same flow defined by the UI test cases in ui_test_requirements.md and the API behavior described in api_test_requirements.md

## Required test categories
- UI automation with Playwright + Python
- API automation with requests + Python
- Separate the implementation by responsibility:
  - UI tests under generated/tests/ui/
  - API tests under generated/tests/api/

## Source-of-truth files
Read and apply the conditions from the following files before generating code:
- ui_test_requirements.md: all required UI user journeys, negative cases, and assertions
- api_test_requirements.md: all valid API endpoints, expected status codes, requests, and response validation rules

If a future requirement needs shared data or helper descriptions, create a dedicated supporting file, but keep the workflow the same: the generator still receives only spec.md as its input entry point, and spec.md points to the relevant source files.

## Model rule
- Use model "gemini-3.6-flash" in any generated code that calls the Gemini API.

## Encoding rule
- Use only plain ASCII characters in all generated code, including string literals and comments.
- Do not use em dashes, smart quotes, or non-ASCII punctuation.

## Project layout
- Test code goes under generated/
- Page objects live under generated/pages/
- Shared fixtures go in generated/conftest.py
- A project-root pytest.ini file is required
- A project-root requirements.txt file is required
- generated/pages/, generated/tests/, generated/tests/ui/, and generated/tests/api/ must each include an empty __init__.py file

## POM rules
- One Python class per page under generated/pages/
- Shared actions such as click, fill, wait, navigate, and is_visible live in generated/pages/base_page.py
- Every page class inherits from BasePage
- Prefer data-test/data-testid, role-based locators, and labels before CSS selectors
- Never use XPath-based locators
- Test files should call page-object methods only and not use raw locators

## Fixture rules
- Fixture scope must be written on the decorator itself, for example @pytest.fixture(scope="session")
- Never pass scope as a parameter to the fixture function itself
- base_url must be session-scoped
- Any fixture used by another fixture must be the same scope or broader
- Shared fixtures belong in generated/conftest.py

## Locator rules
- Never use auto-generated CSS classes such as css-* or hashed class names
- Prefer this order: data-testid/data-test, get_by_role, get_by_label, get_by_text(exact=True)
- Repeated page elements must never be treated as a single unique match without scoping them
- Reinspect the page after navigation or state-changing actions before writing locators or assertions
- Any item-count assertion must count the same element type consistently

## Scope and coverage
The generated suite must cover the requirements listed in ui_test_requirements.md and api_test_requirements.md. The test generator must maintain separation of concern:
- UI features and assertions stay in UI test files
- API requests and responses stay in API test files
- Shared fixtures and common logic stay in generated/conftest.py and base_page.py

## Framework
- pytest + pytest-playwright for UI
- pytest + requests for API
- All tests run under one pytest suite, with UI and API tests in separate folders

## Test quality rules
- Every UI test must contain at least one real assertion
- Include negative-path tests for relevant flows
- Avoid duplicate locators across page objects
- Reuse shared behaviors from base_page.py

## Logging requirements for generated/conftest.py
- Include pytest_sessionfinish(session, exitstatus)
- Skip entirely if SKIP_AUTO_LOG is set
- Skip entirely if results.xml is not present in the current working directory
- Load GEMINI_API_KEY from the project .env file before checking the environment
- Read results.xml
- Parse failures and errors from results.xml and write a local fallback summary before any Gemini request
- Check GEMINI_API_KEY; if missing, print the exact message: "[AI Logging] GEMINI_API_KEY not set in environment - skipping log generation." and keep the local fallback summary
- Use the Gemini API with a supported model name and structured JSON output
- If Gemini returns an empty issue list while XML contains failures, keep the XML-derived issues
- Write summary_markdown to test_log.md beside results.xml
- Write issues to results_summary.json beside results.xml
- Wrap the Gemini call and JSON parsing in try/except and always print the actual exception message and a short traceback if it fails
- The hook must never affect the test run exit code

During regeneration, an existing generated/conftest.py must be preserved because it contains the reliable logging fallback. The generator may regenerate page objects and tests, but must not replace this fixture automatically.

## Required project root config
pytest.ini must contain exactly:
[pytest]
addopts = --junitxml=results.xml --html=report.html --self-contained-html

requirements.txt must include the following packages:
- pytest-html
- google-genai

## Output format
Return every file as a separate block, each preceded by a header line exactly like this:

### FILE: generated/pages/base_page.py
```python
<code here>
```

### FILE: generated/conftest.py
```python
<code here>
```

### FILE: pytest.ini
```
<code here>
```

Continue for every file required by the project, including generated pages, generated tests, conftest.py, pytest.ini, and requirements.txt. Paths must include generated/ where appropriate, and pytest.ini and requirements.txt must be placed at the project root without the generated/ prefix. Do not include any other text outside these blocks.

## Mandatory interpretation rule
When generating the project, the model must read ui_test_requirements.md and api_test_requirements.md as authoritative task lists and build the project around those definitions. This spec file is the architectural contract, but the actual functional coverage comes from the dedicated UI and API requirement files.