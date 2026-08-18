# OrangeHRM Login Automation — Task 15

Data Driven Testing Framework (DDTF) + Page Object Model (POM) + Explicit
Wait / Expected Conditions + Pytest, testing login on the OrangeHRM demo
portal: https://opensource-demo.orangehrmlive.com/web/index.php/auth/login

## Project structure

```
orangehrm_login_framework/
├── conftest.py                # WebDriver fixture + CLI options
├── pytest.ini                 # pytest config (auto HTML report)
├── requirements.txt
├── data/
│   ├── create_test_data.py    # one-time script that builds test_data.xlsx
│   └── test_data.xlsx         # Test ID, Username, Password, Date, Time, Tester, Result
├── pages/
│   ├── base_page.py           # shared Explicit Wait helpers
│   └── login_page.py          # Login page POM (locators + actions)
├── tests/
│   └── test_login.py          # data-driven pytest test
└── reports/
    └── report.html            # generated after each run
```

## Setup

```bash
pip install -r requirements.txt
```

Chrome must be installed locally; `webdriver-manager` downloads the
matching ChromeDriver automatically the first time the suite runs.

## (Re)generate the test data file

```bash
python data/create_test_data.py
```

This creates `data/test_data.xlsx` with 5 Username/Password rows — one
valid OrangeHRM credential and four intentionally invalid ones, so the
suite covers both the successful and failed login paths. Edit the
Username/Password (yellow) cells directly in Excel if you want different
credentials; leave the Date/Time/Tester/Result (green) cells alone — the
framework fills those in automatically.

## Run the tests

```bash
pytest --tester-name="Your Name"
```

Add `--headless` to run without opening a visible Chrome window:

```bash
pytest --tester-name="Your Name" --headless
```

After the run:
- `data/test_data.xlsx` is updated in place with Date, Time of Test, Name
  of Tester and Test Result (Pass/Fail) for every row.
- `reports/report.html` contains the full Pytest HTML report (mandatory
  per the task notes).

## Design notes

- **DDTF** — `utils/excel_utils.read_test_data()` turns every Excel row
  into a pytest parametrize entry, so adding a 6th credential pair to the
  spreadsheet automatically adds a 6th test case, no code changes needed.
- **POM** — `pages/login_page.py` holds every locator and page action;
  `tests/test_login.py` contains zero locators, only test logic.
- **Explicit Wait + Expected Conditions** — `pages/base_page.py` wraps
  `WebDriverWait` + `expected_conditions` for every interaction. No
  `time.sleep()` is used anywhere in the codebase.
- **Pass/Fail logic** — a login is judged successful by the presence of
  the Dashboard header, not by the absence of an exception, so the test
  reflects real UI state.
