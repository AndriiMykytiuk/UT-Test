import allure
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage


class FormsPage(BasePage):
    """Page object for interacting with the Forms tab."""

    # Locators
    FORMS_TAB = (AppiumBy.XPATH, "//android.widget.TextView[@text='Forms']")
    INPUT_FIELD = (AppiumBy.XPATH, '//android.widget.EditText[@content-desc="text-input"]')
    INPUT_RESULT = (AppiumBy.XPATH, '//android.widget.TextView[@content-desc="input-text-result"]')
    SWITCH = (AppiumBy.XPATH, '//android.widget.Switch[@content-desc="switch"]')
    SWITCH_TEXT = (AppiumBy.XPATH, '//android.widget.TextView[@content-desc="switch-text"]')

    # Actions

    @allure.step("Opening Forms tab")
    def click_tab(self):
        """Click the Forms tab to open the form screen."""
        self.logger.info("Clicking the Forms tab")
        self.click(self.FORMS_TAB)

    @allure.step("Typing text into input field: {text}")
    def type_in_input(self, text):
        """Type the given text into the input field."""
        self.logger.info(f"Typing into input field: '{text}'")
        self.send_keys(self.INPUT_FIELD, text)

    @allure.step("Getting typed text result from input field")
    def get_typed_text(self):
        """Retrieve the result text displayed below the input field."""
        text = self.find(self.INPUT_RESULT).text
        self.logger.info(f"Retrieved result text: '{text}'")
        return text

    @allure.step("Toggling the switch")
    def toggle_switch(self):
        """Click the toggle switch to change its state."""
        self.logger.info("Toggling the switch")
        self.click(self.SWITCH)

    @allure.step("Checking if toggle switch is ON")
    def is_toggle_checked(self):
        """Return True if the toggle is ON, else False."""
        element = self.find(self.SWITCH)
        status = element.get_attribute("checked") == "true"
        self.logger.info(f"Switch checked status: {status}")
        return status

    @allure.step("Getting toggle switch label text")
    def get_toggle_text(self):
        """Get the label text near the toggle (indicating ON/OFF)."""
        text = self.find(self.SWITCH_TEXT).text
        self.logger.info(f"Toggle text is: '{text}'")
        return text
