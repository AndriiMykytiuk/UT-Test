import pytest
import allure
from pages.drag_page import DragPage


@pytest.mark.drag
class TestDragAndDrop:
    """
    Test suite for verifying the drag-and-drop functionality on the Drag screen.

    Contains tests to:
    - Fully solve the puzzle and verify the success state.
    - Partially interact and ensure reset restores the initial state.
    """

    @allure.title("Solve the full drag-and-drop puzzle")
    @allure.description("""
    Solves the full puzzle by dragging each tile into its respective drop zone.
    Verifies that the success screen is displayed and the Retry button resets the puzzle.
    """)
    def test_solve_puzzle(self, driver):
        """
        Test that solves the drag-and-drop puzzle and verifies the success message appears.
        Then checks that pressing Retry resets the state.
        """
        drag_page = DragPage(driver)
        drag_page.open_tab()

        initial_drag_tiles = drag_page.get_drag_elements()
        drag_page.solve_puzzle()

        with allure.step("Verify that the success screen is displayed"):
            assert drag_page.is_success_screen_displayed(), "Success screen not found"

        drag_page.click_retry()
        retry_drag_elements = drag_page.get_drag_elements()

        with allure.step("Verify tiles are reset after clicking Retry"):
            assert len(initial_drag_tiles) == len(retry_drag_elements), "Retry did not reset puzzle"

    @allure.title("Drag a few tiles and verify Reset restores original state")
    @allure.description("""
    Drags two tiles into place, then clicks Reset and ensures all tiles return to initial positions.
    """)
    def test_drag_and_reset(self, driver):
        """
        Test that performs a partial puzzle interaction, then resets,
        and verifies the original state is restored.
        """
        drag_page = DragPage(driver)
        drag_page.open_tab()

        initial_drag_tiles = drag_page.get_drag_elements()

        drag_page.drag_tile_to("l1", "l1")
        drag_page.drag_tile_to("c2", "c2")

        after_drag_tiles = drag_page.get_drag_elements()

        with allure.step("Verify drag reduced the number of visible tiles"):
            assert len(initial_drag_tiles) > len(after_drag_tiles), "Tiles not removed after drag"

        drag_page.click_reset()
        after_reset_tiles = drag_page.get_drag_elements()

        with allure.step("Verify all tiles are restored after reset"):
            assert len(after_reset_tiles) == len(initial_drag_tiles), "Reset did not restore original tiles"
