import pytest
import allure
from pages.forms_page import FormsPage


@allure.feature("Forms")
@pytest.mark.forms
class TestFormsInput:

    @allure.story("Input Field")
    @allure.title("Should reflect typed input correctly")
    @pytest.mark.parametrize("input_text", [
        "Hello world",           # Normal text
        "123456",                # Numbers
        "!@#$%^&*()",            # Special characters
        "Hi there 😊",           # Unicode (emoji)
        "",                      # Empty input
        "a" * 30                 # Max length input
    ])
    def test_input_field_reflects_typed_text(self, driver, input_text):
        """Check if typed input is reflected correctly in the result text."""
        forms_page = FormsPage(driver)
        forms_page.click_tab()

        forms_page.type_in_input(input_text)
        actual_text = forms_page.get_typed_text()

        with allure.step(f"Verify that input text '{input_text}' is reflected correctly"):
            assert actual_text == input_text, (
                f"Expected '{input_text}', but got '{actual_text}'"
            )

    @allure.story("Toggle Switch")
    @allure.title("Should toggle ON and OFF correctly with correct text")
    def test_toggle_switch_behavior_and_text(self, driver):
        """Toggle switch ON/OFF and verify state and text."""
        forms_page = FormsPage(driver)
        forms_page.click_tab()

        # Toggle ON
        forms_page.toggle_switch()
        with allure.step("Verify toggle is ON"):
            assert forms_page.is_toggle_checked(), "Expected toggle to be ON"
        with allure.step("Verify toggle label says 'Click to turn the switch OFF'"):
            assert forms_page.get_toggle_text() == "Click to turn the switch OFF", \
                "Expected toggle text to indicate switching OFF"

        # Toggle OFF
        forms_page.toggle_switch()
        with allure.step("Verify toggle is OFF"):
            assert not forms_page.is_toggle_checked(), "Expected toggle to be OFF"
        with allure.step("Verify toggle label says 'Click to turn the switch ON'"):
            assert forms_page.get_toggle_text() == "Click to turn the switch ON", \
                "Expected toggle text to indicate switching ON"
