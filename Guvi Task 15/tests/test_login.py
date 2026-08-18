"""
tests/test_login.py
--------------------
Task 15 — Data Driven Testing Framework (DDTF) + Page Object Model (POM) +
Explicit Wait / Expected Conditions + Pytest, for the OrangeHRM demo login
page.

Flow per data row:
    1. Read Username/Password from data/test_data.xlsx (Data Driven Testing)
    2. Attempt login via the LoginPage Page Object
    3. Decide Pass/Fail from the actual page state (Dashboard vs error banner)
    4. Write Date, Time of Test, Name of Tester and Test Result back into
       the SAME Excel file
No time.sleep() is used anywhere — every wait is an Explicit Wait with an
Expected Condition (see pages/base_page.py).
"""

import os
import pytest

from pages.login_page import LoginPage
from utils.excel_utils import read_test_data, write_test_result

# Path to the shared data file, resolved relative to this file so the suite
# runs correctly no matter what directory pytest is invoked from.
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "test_data.xlsx")

# Load once at collection time so pytest can build one parametrized test
# per Excel row (the heart of the Data Driven Testing Framework).
TEST_DATA = read_test_data(DATA_FILE)


def _ids(entry):
    """Human-readable test ID shown in the pytest / HTML report output."""
    return entry["test_id"]


@pytest.mark.parametrize("credentials", TEST_DATA, ids=_ids)
def test_login(driver, tester_name, credentials):
    """
    Data-driven login test: exercises every Username/Password pair listed
    in test_data.xlsx against the OrangeHRM demo portal, then records the
    Pass/Fail outcome back into that same file.
    """
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(credentials["username"], credentials["password"])

    login_successful = login_page.is_login_successful()
    result = "Pass" if login_successful else "Fail"

    # Persist the outcome to Excel regardless of pass/fail so the sheet
    # always reflects the most recent run.
    write_test_result(
        file_path=DATA_FILE,
        row=credentials["row"],
        tester_name=tester_name,
        result=result,
    )

    # The only credential set expected to succeed is the valid "Admin"
    # account (TC_LOGIN_01) — every other row is a deliberate negative
    # test case, so we assert the outcome matches that expectation.
    expected_pass = credentials["username"] == "Admin" and credentials["password"] == "admin123"

    assert login_successful == expected_pass, (
        f"[{credentials['test_id']}] Expected login success={expected_pass} "
        f"but got {login_successful}. Portal error message: "
        f"'{login_page.get_error_message()}'"
    )
