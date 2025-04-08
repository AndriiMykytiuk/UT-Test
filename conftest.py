import os
import shutil
import pytest
import allure
from datetime import datetime
from appium import webdriver
from appium.options.android import UiAutomator2Options


@pytest.fixture(scope="function")
def driver():
    """
    Set up and yield an Appium driver instance for Android emulator.

    Uses UiAutomator2 and loads the test APK from the local 'apk' folder.
    Customize the device name and capabilities as needed.
    """
    options = UiAutomator2Options()
    options.set_capability("platformName", "Android")
    options.set_capability("deviceName", "emulator-5554")  # Replace with your emulator/device ID
    options.set_capability("automationName", "UiAutomator2")
    options.set_capability("autoGrantPermissions", True)
    options.set_capability("newCommandTimeout", 300)
    options.set_capability("appPackage", "com.wdiodemoapp")
    options.set_capability("appActivity", "com.wdiodemoapp.MainActivity")

    apk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "apk/test.apk"))
    if not os.path.exists(apk_path):
        raise FileNotFoundError(f"APK file not found at: {apk_path}")
    options.set_capability("app", apk_path)

    driver = webdriver.Remote("http://localhost:4723/wd/hub", options=options)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to collect test result metadata after execution phase.

    This allows access to pass/fail status in fixtures via `request.node`.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def take_screenshot_on_finish(request, driver):
    """
    Automatically take a screenshot at the end of each test and attach it to Allure.

    Only attaches screenshots for passed or failed test cases.
    """
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.when == "call":
        if request.node.rep_call.passed or request.node.rep_call.failed:
            test_name = request.node.name
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            screenshots_dir = os.path.join(os.getcwd(), "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            file_path = os.path.join(screenshots_dir, f"{test_name}_{timestamp}.png")

            try:
                driver.save_screenshot(file_path)
                allure.attach.file(
                    file_path,
                    name=f"{test_name} Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"⚠️ Failed to take screenshot: {e}")


def pytest_configure(config):
    """
    Safely clear the allure-results directory at the very start of pytest config stage.
    This happens before Allure plugin starts writing to the folder.
    """
    results_dir = os.path.join(os.getcwd(), "allure-results")
    if os.path.exists(results_dir):
        try:
            shutil.rmtree(results_dir)
            print(f"🧹 Cleared previous Allure results from: {results_dir}")
        except Exception as e:
            print(f"⚠️ Could not clean allure-results directory: {e}")
    os.makedirs(results_dir, exist_ok=True)
