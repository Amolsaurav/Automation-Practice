# Automation Tests

Playwright and pytest tests for AutomationExercise.

## Setup

```bash
pip install pytest pytest-playwright pytest-html
playwright install
```

## Run Tests

From this directory:

```bash
pytest
```

Run a specific test file:

```bash
pytest Tests/test_additional.py
```

The HTML report is generated at `report.html`.

## Project Structure

- `Pages/` - Page Object Model classes
- `Tests/` - Test cases and pytest fixtures
- `TestData/` - JSON test data
- `utilities/constants.py` - Shared configuration and test values
- `utilities/data_loader.py` - JSON data loader
# Automation-Practice
