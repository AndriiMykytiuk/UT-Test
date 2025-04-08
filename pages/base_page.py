import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import get_logger


class BasePage:
    """
    Base page class that provides common methods for element interactions,
    such as finding, clicking, and typing. It uses explicit waits and logs actions.
    """

    def __init__(self, driver, timeout=15):
        """
        Initialize the BasePage with a WebDriver and optional timeout.

        :param driver: WebDriver instance (Appium or Selenium)
        :param timeout: Timeout for waiting on elements (default is 10 seconds)
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.logger = get_logger(self.__class__.__name__)

    @allure.step("Finding element: {locator}")
    def find(self, locator):
        """
        Wait for an element to be present in the DOM and return it.
        """
        try:
            self.logger.info(f"Looking for element: {locator}")
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found within timeout: {locator}")
            raise AssertionError(f"Element with locator {locator} not found within timeout.")

    @allure.step("Finding multiple elements: {locator}")
    def find_elements(self, locator):
        """
        Wait for at least one element to be present and return all matching elements.

        :param locator: Tuple (By, locator) to find elements
        :return: List of WebElements
        :raises AssertionError: If no elements are found within the timeout
        """
        try:
            self.logger.info(f"Looking for multiple elements: {locator}")
            elements = self.wait.until(lambda driver: driver.find_elements(*locator))
            if not elements:
                raise TimeoutException("No elements found")
            self.logger.info(f"Found {len(elements)} elements for locator: {locator}")
            return elements
        except TimeoutException:
            self.logger.error(f"No elements found within timeout for locator: {locator}")
            raise AssertionError(f"No elements with locator {locator} found within timeout.")

    @allure.step("Clicking element: {locator}")
    def click(self, locator):
        """
        Wait for an element to be clickable and perform a click action.
        """
        try:
            self.logger.info(f"Clicking element: {locator}")
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            self.logger.info(f"Clicked element: {locator}")
        except TimeoutException:
            self.logger.error(f"Element not clickable within timeout: {locator}")
            raise AssertionError(f"Element with locator {locator} not clickable within timeout.")

    @allure.step("Sending keys to element: {locator} | Value: {value}")
    def send_keys(self, locator, value):
        """
        Find an element, clear its content, and send the given keys to it.
        """
        self.logger.info(f"Sending keys to element: {locator} | Value: {value}")
        element = self.find(locator)
        element.clear()
        element.send_keys(value)
        self.logger.info(f"Keys sent to element: {locator}")
