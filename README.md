# Playwright Gemini Automation Framework

Automated UI and API tests for [Automation Exercise](https://automationexercise.com) using Python, pytest, Playwright, and Gemini.

## Features

- Playwright UI automation
- Requests-based API testing
- Page Object Model
- Automatic HTML and JUnit reports
- Automatic test summary generation
- Gemini-powered test generation and failure analysis
- Local fallback summary when Gemini is unavailable

## Requirements

- Python 3.10+
- Node.js and npm
- Google Gemini API key
- Playwright browser dependencies

## Installation

Open PowerShell in this project directory:

```powershell
cd "C:\Users\amol saurav\OneDrive\Desktop\Internship\playwright-gemini"
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install Python packages:

```powershell
pip install pytest pytest-playwright pytest-html requests google-genai pydantic mcp
```

Install Playwright browsers:

```powershell
playwright install
```

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
```

## Project Structure

```text
playwright-gemini/
├── generated/
│   ├── conftest.py
│   ├── pages/
│   └── tests/
│       ├── api/
│       └── ui/
├── generate_tests.py
├── heal_tests.py
├── pytest.ini
├── spec.md
├── ui_test_requirements.md
├── api_test_requirements.md
└── README.md
```

## Generate Tests

The generator reads the specification files and creates page objects and UI/API tests under `generated/`.

```powershell
python generate_tests.py
```

The existing `generated/conftest.py` is preserved during regeneration because it contains the reporting and summary logic.

## Run All Tests

Run pytest from the project root:

```powershell
pytest
```

The project configuration automatically creates:

- `report.html` - interactive HTML test report
- `results.xml` - JUnit XML report
- `test_log.md` - test execution summary
- `results_summary.json` - structured failure summary

## Run Specific Tests

Run only UI tests:

```powershell
pytest generated/tests/ui
```

Run only API tests:

```powershell
pytest generated/tests/api
```

Run one test file:

```powershell
pytest generated/tests/ui/test_auth.py
```

Run one test:

```powershell
pytest generated/tests/ui/test_auth.py::test_login_user_valid
```

Run with detailed output:

```powershell
pytest -vv
```

## Results Summary

After every pytest run, `conftest.py` creates or recreates `test_log.md` (a human-readable test execution log with categorized test suites, clear failure reasons, and exact file locations for fixes) and:

```text
results_summary.json
```

The file contains failed and errored tests:

```json
{
	"issues": [
		{
			"test": "test_name",
			"type": "test_failure",
			"description": "Failure details"
		}
	]
}
```

The file can be deleted before a test run. It will be generated again automatically after pytest finishes.

The local fallback summary is written even when:

- `GEMINI_API_KEY` is missing
- Gemini is unavailable
- Gemini returns an error
- Tests fail

Do not set `SKIP_AUTO_LOG` if you want the summary files to be generated.

## Automatic Test Fixes

`heal_tests.py` reads `results_summary.json` and sends fixable failures to Gemini.

```powershell
python heal_tests.py
```

The script may ask for confirmation before applying a suggested change.

## Reports

Open the generated HTML report:

```powershell
Start-Process .\report.html
```

View the structured summary:

```powershell
Get-Content .\results_summary.json
```

View the Markdown summary:

```powershell
Get-Content .\test_log.md
```

## Configuration

The root `pytest.ini` contains:

```ini
[pytest]
pythonpath = .
addopts = --junitxml=results.xml --html=report.html --self-contained-html
```

`pythonpath = .` allows pytest to import the generated package and its page objects correctly.

## Troubleshooting

### ModuleNotFoundError

Run pytest from the project root:

```powershell
cd "C:\Users\amol saurav\OneDrive\Desktop\Internship\playwright-gemini"
pytest
```

Do not run pytest from a parent directory.

### Browser executable missing

Install the Playwright browsers:

```powershell
playwright install
```

### Gemini API errors

The test summary is still generated locally when Gemini fails. Check that `.env` contains:

```env
GEMINI_API_KEY=your_gemini_api_key
```

### Summary file is missing

Delete the old file and run pytest again:

```powershell
Remove-Item .\results_summary.json -ErrorAction SilentlyContinue
pytest
Test-Path .\results_summary.json
```

The final command should return:

```text
True
```
