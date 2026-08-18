"""
conftest.py
-----------
Shared pytest fixtures for the whole suite:
  * `driver`      -> a fresh Chrome WebDriver instance per test function
  * `tester_name` -> the name written into the "Name of Tester" Excel column

Run with, e.g.:
    pytest --tester-name="Priya Sharma" --html=reports/report.html --self-contained-html
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def pytest_addoption(parser):
    """Custom CLI flag so whoever runs the suite can identify themselves."""
    parser.addoption(
        "--tester-name",
        action="store",
        default="Automation Bot",
        help="Name recorded in the 'Name of Tester' column of test_data.xlsx",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome in headless mode (no visible browser window).",
    )


@pytest.fixture(scope="session")
def tester_name(request):
    return request.config.getoption("--tester-name")


@pytest.fixture(scope="function")
def driver(request):
    """
    Creates one Chrome WebDriver per test function (fresh browser session
    per login attempt, avoiding any state leaking between test cases) and
    guarantees it's closed even if the test fails.
    """
    options = Options()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    service = Service(ChromeDriverManager().install())
    chrome_driver = webdriver.Chrome(service=service, options=options)

    yield chrome_driver

    chrome_driver.quit()
