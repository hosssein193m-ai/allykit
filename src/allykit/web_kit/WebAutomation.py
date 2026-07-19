"""
Web Automation Module

This module provides a comprehensive wrapper around Selenium WebDriver,
offering a clean, type-safe interface for common web automation tasks.
It includes explicit wait handling, error management, and various interaction methods.
"""
from typing import Tuple

try:
    from allykit.web_kit.CChrome import wait_for_element
    from allykit.web_kit.CChrome import chrome
except ImportError:
    raise ImportError("allykit Not fully installed")
try:
    from selenium.webdriver import Chrome, ActionChains
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait, Select
    from selenium.common.exceptions import (
        TimeoutException,
        NoSuchElementException,
        WebDriverException,
    )
except ImportError:
    raise("pip install selenium")
           

class WebAutomation:
    """
    A comprehensive wrapper class for Selenium WebDriver automation.

    This class provides a set of convenient methods for common web automation tasks,
    including element finding, clicking, typing, scrolling, hovering, and more.
    All methods include built-in error handling and explicit wait management.

    Attributes:
        driver (Chrome): The Selenium WebDriver instance.
        wait (WebDriverWait): The WebDriverWait instance configured with a 30-second timeout.
        default_timeout (int): Default timeout in seconds for wait operations.

    Example:
        >>> # Using existing driver
        >>> from selenium.webdriver import Chrome
        >>> driver = Chrome()
        >>> automation = WebAutomation(driver)
        >>> automation.open("https://example.com")
        >>> automation.click((By.ID, "submit-btn"))
        
        >>> # Auto-create driver (uses CChrome.chrome() by default)
        >>> automation = WebAutomation()
        >>> automation.open("https://google.com")
        >>> automation.write((By.NAME, "q"), "Selenium")
    """

    def __init__(self, driver: Chrome = None, timeout : int = 30):
        """
        Initializes the WebAutomation instance with a WebDriver.

        If no driver is provided, this method will attempt to create one
        using the `chrome()` function from `utile.web_utile.CChrome`.

        Args:
            driver (Chrome, optional): An initialized Chrome WebDriver instance.
                                       The driver should already be configured with
                                       appropriate options and capabilities.
                                       If None, a new driver will be created automatically.
                                       Defaults to None.
            timeout (int): Default timeout in seconds for wait operations.
                           Defaults to 30.

        Raises:
            NameError: If `chrome()` function is not available when driver is None.
            WebDriverException: If driver creation fails.

        Note:
            When auto-creating a driver, this method relies on the `chrome()`
            function from the CChrome module. Make sure this function is properly
            defined and returns a valid Chrome WebDriver instance.

        Example:
            >>> # Manual driver creation
            >>> from selenium.webdriver import Chrome
            >>> driver = Chrome()
            >>> automation = WebAutomation(driver)
            
            >>> # Automatic driver creation
            >>> automation = WebAutomation()  # Uses CChrome.chrome()
        """
        if driver is None:
            driver = chrome()
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def find(self, locator: Tuple[By, str]) -> WebElement:
        """
        Finds a web element using the specified locator.

        This method uses explicit wait to ensure the element is present
        in the DOM before returning it.

        Args:
            locator (Tuple[By, str]): The locator strategy and selector.

        Returns:
            WebElement: The found web element.

        Raises:
            TimeoutException: If the element is not found within the timeout period.

        Example:
            >>> element = automation.find((By.ID, "username"))
        """
        try:
            return wait_for_element(locator, self.wait)
        except TimeoutException:
            raise TimeoutException(f"Element not found: {locator}")

    def open(self, url: str) -> None:
        """
        Navigates the browser to the specified URL.

        Args:
            url (str): The complete URL to navigate to (including protocol).

        Raises:
            RuntimeError: If the URL fails to load due to WebDriver issues.

        Example:
            >>> automation.open("https://example.com")
        """
        try:
            self.driver.get(url)
        except WebDriverException as e:
            raise RuntimeError(f"Failed to open '{url}'") from e

    def maximize_window(self):
        return self.driver.maximize_window()

    def click(self, locator: Tuple[By, str]) -> None:
        """
        Clicks on the specified element using JavaScript.

        This method uses JavaScript execution for clicking, which can bypass
        certain issues like element being covered by other elements or
        not being interactable.

        Args:
            locator (Tuple[By, str]): The locator of the element to click.

        Raises:
            RuntimeError: If the click operation fails.

        Example:
            >>> automation.click((By.XPATH, "//button[text()='Submit']"))
        """
        try:
            element = self.find(locator)
            element.click()
        except Exception as e:
            raise RuntimeError(f"Failed to click element: {locator}") from e

    def send_keys(self, locator: Tuple[By, str], text: str | int) -> None:
        """
        Sends keystrokes to the specified element without clearing it first.

        This method appends the text to the existing content of the element.
        For clearing before typing, use the `write()` method.

        Args:
            locator (Tuple[By, str]): The locator of the target element.
            text (str | int): The text or number to send as keystrokes.

        Raises:
            RuntimeError: If sending keys fails.

        Example:
            >>> automation.send_keys((By.ID, "search"), "query")
        """
        try:
            self.find(locator).send_keys(str(text))
        except Exception as e:
            raise RuntimeError(f"Failed to send keys to: {locator}") from e

    def execute_script(self, locator: Tuple[By, str], text : str) -> None:
        try:
            element = self.find(locator)
            self.driver.execute_script(text , element)
        except Exception as e:
            raise RuntimeError(f"Failed to click element: {locator}") from e

    def write(self, locator: Tuple[By, str], text: str | int) -> None:
        """
        Clears the element and then types the specified text.

        This method ensures the field is empty before typing new text.
        Useful for filling input fields, text areas, and similar elements.

        Args:
            locator (Tuple[By, str]): The locator of the target element.
            text (str | int): The text or number to write into the field.

        Raises:
            RuntimeError: If the write operation fails.

        Example:
            >>> automation.write((By.NAME, "email"), "user@example.com")
        """
        try:
            element = self.find(locator)
            element.clear()
            element.send_keys(str(text))
        except Exception as e:
            raise RuntimeError(f"Failed to write into: {locator}") from e

    def clear(self, locator: Tuple[By, str]) -> None:
        """
        Clears the content of the specified element.

        Useful for clearing input fields, text areas, or any element
        that accepts text input.

        Args:
            locator (Tuple[By, str]): The locator of the element to clear.

        Raises:
            RuntimeError: If clearing the element fails.

        Example:
            >>> automation.clear((By.ID, "search-box"))
        """
        try:
            self.find(locator).clear()
        except Exception as e:
            raise RuntimeError(f"Failed to clear element: {locator}") from e

    def get_text(self, locator: Tuple[By, str]) -> str:
        """
        Retrieves the visible text of the specified element.

        This method returns the text as displayed on the page, including
        whitespace but not stripping it.

        Args:
            locator (Tuple[By, str]): The locator of the element.

        Returns:
            str: The visible text of the element.

        Raises:
            RuntimeError: If retrieving text fails.

        Example:
            >>> text = automation.get_text((By.CLASS_NAME, "title"))
        """
        try:
            return self.find(locator).text
        except Exception as e:
            raise RuntimeError(f"Failed to get text from: {locator}") from e

    def get_text_precise(self, locator: Tuple[By, str]) -> str:
        """
        Retrieves and strips the visible text of the specified element.

        This method returns the text with leading and trailing whitespace removed,
        making it suitable for comparisons and validation.

        Args:
            locator (Tuple[By, str]): The locator of the element.

        Returns:
            str: The stripped visible text of the element.

        Raises:
            RuntimeError: If retrieving text fails.

        Example:
            >>> text = automation.get_text_precise((By.CSS_SELECTOR, ".price"))
        """
        try:
            return self.find(locator).text.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to get precise text from: {locator}") from e

    def get_attribute(self, locator: Tuple[By, str], attribute: str) -> str | None:
        """
        Retrieves the value of the specified attribute from the element.

        Args:
            locator (Tuple[By, str]): The locator of the element.
            attribute (str): The name of the attribute to retrieve.

        Returns:
            str | None: The attribute value, or None if the attribute does not exist.

        Raises:
            RuntimeError: If retrieving the attribute fails.

        Example:
            >>> href = automation.get_attribute((By.LINK_TEXT, "Home"), "href")
        """
        try:
            return self.find(locator).get_attribute(attribute)
        except Exception as e:
            raise RuntimeError(
                f"Failed to get attribute '{attribute}' from: {locator}"
            ) from e

    def is_visible(self, locator: Tuple[By, str]) -> bool:
        """
        Checks if the element exists and is present in the DOM.

        Note: This method checks for presence in DOM, not actual visibility
        on the page (i.e., it doesn't verify if the element is hidden by CSS).

        Args:
            locator (Tuple[By, str]): The locator of the element to check.

        Returns:
            bool: True if the element is present in the DOM, False otherwise.

        Example:
            >>> if automation.is_visible((By.ID, "error-message")):
            ...     print("Error is displayed")
        """
        try:
            self.find(locator)
            return True
        except (TimeoutException, NoSuchElementException):
            return False

    def scroll_to(self, locator: Tuple[By, str]) -> None:
        """
        Scrolls the browser window to bring the specified element into view.

        The element is scrolled to the center of the viewport for optimal visibility.

        Args:
            locator (Tuple[By, str]): The locator of the element to scroll to.

        Raises:
            RuntimeError: If scrolling fails.

        Example:
            >>> automation.scroll_to((By.ID, "footer"))
        """
        try:
            element = self.find(locator)
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});",
                element
            )
        except Exception as e:
            raise RuntimeError(f"Failed to scroll to: {locator}") from e

    def hover(self, locator: Tuple[By, str]) -> None:
        """
        Hovers the mouse cursor over the specified element.

        This action triggers any hover effects or dropdown menus associated
        with the element.

        Args:
            locator (Tuple[By, str]): The locator of the element to hover over.

        Raises:
            RuntimeError: If hovering fails.

        Example:
            >>> automation.hover((By.CLASS_NAME, "dropdown-menu"))
        """
        try:
            ActionChains(self.driver).move_to_element(
                self.find(locator)
            ).perform()
        except Exception as e:
            raise RuntimeError(f"Failed to hover over: {locator}") from e

    def press_enter(self, locator: Tuple[By, str]) -> None:
        """
        Simulates pressing the ENTER key on the specified element.

        This is particularly useful for submitting forms or triggering
        search operations where ENTER key is expected.

        Args:
            locator (Tuple[By, str]): The locator of the element to press ENTER on.

        Raises:
            RuntimeError: If pressing ENTER fails.

        Example:
            >>> automation.press_enter((By.ID, "search-input"))
        """
        try:
            self.find(locator).send_keys(Keys.ENTER)
        except Exception as e:
            raise RuntimeError(f"Failed to press ENTER on: {locator}") from e

    def select_by_text(self, locator: Tuple[By, str], text: str) -> None:
        """
        Selects an option from a <select> dropdown by its visible text.

        This method is specifically designed for HTML SELECT elements.

        Args:
            locator (Tuple[By, str]): The locator of the SELECT element.
            text (str): The visible text of the option to select.

        Raises:
            RuntimeError: If selection fails or the element is not a SELECT.

        Example:
            >>> automation.select_by_text((By.ID, "country"), "United States")
        """
        try:
            Select(self.find(locator)).select_by_visible_text(text)
        except Exception as e:
            raise RuntimeError(
                f"Failed to select '{text}' from: {locator}"
            ) from e

    def select_by_value(self, locator: Tuple[By, str], text: str) -> None:
        try:
            Select(self.find(locator)).select_by_value(text)
        except Exception as e:
            raise RuntimeError(
                f"Failed to select '{text}' from: {locator}"
            ) from e

    def wait_until_disappear(self, locator: Tuple[By, str]) -> None:
        """
        Waits until the specified element disappears from the DOM.

        This is useful for waiting for loading indicators, modal dialogs,
        or any element that should vanish after an action.

        Args:
            locator (Tuple[By, str]): The locator of the element to wait for.

        Raises:
            TimeoutException: If the element does not disappear within the timeout.

        Example:
            >>> automation.wait_until_disappear((By.ID, "loading-spinner"))
        """
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            raise TimeoutException(f"Element did not disappear: {locator}")

    def screenshot(self, path: str) -> None:
        """
        Captures a screenshot of the current browser window.

        The screenshot is saved to the specified file path in PNG format.

        Args:
            path (str): The file path where the screenshot should be saved.
                       Should include the .png extension.

        Raises:
            RuntimeError: If saving the screenshot fails.

        Example:
            >>> automation.screenshot("screenshots/homepage.png")
        """
        try:
            self.driver.save_screenshot(path)
        except Exception as e:
            raise RuntimeError(f"Failed to save screenshot: {path}") from e

    def quit(self) -> None:
        """
        Closes the browser and terminates the WebDriver session.

        This method should be called to clean up resources after automation is complete.
        It closes all browser windows and ends the WebDriver process.

        Example:
            >>> automation.quit()
        """
        self.driver.quit()
