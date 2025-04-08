import allure
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.common.actions import interaction
from pages.base_page import BasePage


class DragPage(BasePage):
    """
    Page object model for the Drag & Drop screen.
    Provides methods to interact with drag tiles and drop zones,
    including resetting and validating dropped state.
    """

    # Locators
    DRAG_TAB = (AppiumBy.ACCESSIBILITY_ID, "Drag")
    DRAG_ELEMENTS = (
        AppiumBy.XPATH,
        '//android.view.ViewGroup[@content-desc="renew"]/following-sibling::android.view.ViewGroup[starts-with(@content-desc, "drag-")]'
    )
    RESET_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="renew"]')
    SUCCESS_TEXT = (AppiumBy.XPATH, '//android.widget.TextView[@text="You made it, click retry if you want to try it again."]')
    RETRY_BUTTON = (AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="button-Retry"]/android.view.ViewGroup')

    @allure.step("Opening Drag tab")
    def open_tab(self):
        """
        Open the Drag tab from the home screen.
        """
        self.click(self.DRAG_TAB)

    @allure.step("Getting all draggable tile elements")
    def get_drag_elements(self):
        """
        Return a list of all drag elements currently rendered below the 'renew' button.

        :return: list of WebElement drag tiles
        """
        return self.find_elements(self.DRAG_ELEMENTS)

    @allure.step("Getting drag tile at position: {position}")
    def get_drag_element(self, position: str):
        """
        Get a specific draggable tile element by position ID.

        :param position: Tile ID such as 'l1', 'c2', or 'r3'
        :return: WebElement representing the drag tile
        """
        locator = (
            AppiumBy.XPATH,
            f'//android.view.ViewGroup[@content-desc="drag-{position}"]/android.widget.ImageView'
        )
        return self.find(locator)

    @allure.step("Getting drop zone at position: {position}")
    def get_drop_zone(self, position: str):
        """
        Get a drop zone WebElement by its position ID.

        :param position: Zone ID like 'l1', 'c2', or 'r3'
        :return: WebElement representing the drop zone
        """
        locator = (
            AppiumBy.XPATH,
            f'//android.view.ViewGroup[@content-desc="drop-{position}"]/android.view.ViewGroup'
        )
        return self.find(locator)

    @allure.step("Dragging tile from {from_position} to {to_position}")
    def drag_tile_to(self, from_position: str, to_position: str):
        """
        Drag a tile from its drag-{from_position} location to drop-{to_position}.
        This method uses W3C Actions and targets the center of both elements.

        :param from_position: Position ID of source tile
        :param to_position: Position ID of drop zone
        """
        source = self.get_drag_element(from_position)
        target = self.get_drop_zone(to_position)

        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        actions = ActionBuilder(self.driver, mouse=finger)

        # Calculate source center
        src_rect = source.rect
        src_center_x = src_rect["x"] + src_rect["width"] // 2
        src_center_y = src_rect["y"] + src_rect["height"] // 2

        # Calculate target center
        tgt_rect = target.rect
        tgt_center_x = tgt_rect["x"] + tgt_rect["width"] // 2
        tgt_center_y = tgt_rect["y"] + tgt_rect["height"] // 2

        # Perform drag & drop
        actions.pointer_action.move_to_location(src_center_x, src_center_y)
        actions.pointer_action.pointer_down()
        actions.pointer_action.pause(0.2)
        actions.pointer_action.move_to_location(tgt_center_x, tgt_center_y)
        actions.pointer_action.pause(1.0)  # simulate holding before drop
        actions.pointer_action.pointer_up()

        actions.perform()
        self.logger.info(f"Dragged from {from_position} to {to_position} (center-to-center)")

    @allure.step("Verifying puzzle completion screen is shown")
    def is_success_screen_displayed(self) -> bool:
        """Check if the 'Congratulations' screen is displayed after solving the puzzle."""
        try:
            return self.find(self.SUCCESS_TEXT).is_displayed()
        except AssertionError:
            return False

    @allure.step("Clicking the reset button")
    def click_reset(self):
        """
        Click the reset button to return tiles to the initial state.
        """
        self.click(self.RESET_BUTTON)
        self.driver.implicitly_wait(3)

    @allure.step("Clicking Retry button to return to initial puzzle state")
    def click_retry(self):
        """Click the Retry button to return to the drag-and-drop start state."""
        self.click(self.RETRY_BUTTON)

    @allure.step("Solving the full puzzle")
    def solve_puzzle(self):
        """
        Drag and drop each puzzle tile into its correct drop zone to solve the puzzle.
        The default mapping assumes drag-{pos} goes into drop-{pos}.
        """
        positions = [
            "l1", "c1", "r1",
            "l2", "c2", "r2",
            "l3", "c3", "r3"
        ]
        for pos in positions:
            self.drag_tile_to(pos, pos)

        self.logger.info("Puzzle solved via drag and drop.")


