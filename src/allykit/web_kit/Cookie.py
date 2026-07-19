import os
import pickle
import time
from selenium.webdriver import Chrome


class Cookie:
    """
    A comprehensive cookie management class for Selenium WebDriver.
    
    This class provides complete functionality for storing, loading, managing,
    and cleaning up browser cookies with persistent storage using Pickle files.
    It supports multiple cookie files, expiration handling, and seamless 
    integration with Chrome WebDriver.
    
    Attributes:
        cookie_file (str): Path to the cookie storage file
        driver (Chrome): Selenium Chrome WebDriver instance
    
    Example:
        >>> from selenium import webdriver
        >>> driver = webdriver.Chrome()
        >>> cookie_manager = Cookie(driver, "session_cookies.pkl")
        >>> cookie_manager.load_cookies()
    """

    def __init__(self, driver: Chrome, cookie_file: str = "cookies.pkl", url: str = None):
        """
        Initialize the Cookie manager.
        
        Args:
            driver (Chrome): Selenium Chrome WebDriver instance
            cookie_file (str, optional): Path to the cookie storage file. 
                Defaults to "cookies.pkl".
            url (str, optional): URL to load initially in the browser.
                If provided, navigates to this URL upon initialization.
        
        Returns:
            None
        
        Example:
            >>> driver = webdriver.Chrome()
            >>> cookie_manager = Cookie(driver, "my_cookies.pkl", "https://example.com")
        """
        self.cookie_file = cookie_file
        self.driver = driver
        if url:
            driver.get(url)

    def load_cookies(self, refresh: bool = True) -> bool:
        """
        Load cookies from the stored pickle file and add them to the browser.
        
        This method reads the cookie file, deserializes the cookies, and adds
        them to the current browser session. If the 'refresh' parameter is True,
        it refreshes the page to apply the cookies.
        
        Args:
            refresh (bool, optional): If True, refreshes the page after loading 
                cookies. Defaults to True.
        
        Returns:
            bool: True if cookies were refresh successfully, False otherwise.
                Returns False if the file doesn't exist or an error occurs.
        
        Example:
            >>> if cookie_manager.load_cookies():
            ...     print("Cookies refresh successfully")
            ... else:
            ...     print("Failed to load cookies")
        """
        try:
            if os.path.exists(self.cookie_file):
                with open(self.cookie_file, "rb") as f:
                    cookies = pickle.load(f)
                    for cookie in cookies:
                        try:
                            self.driver.add_cookie(cookie)
                        except Exception:
                            continue
                if refresh:
                    self.driver.refresh()
                return True
        except Exception as e:
            print(f"Error loading cookies: {e}")
            return False
        return False

    def save_cookies(self, cookies: list[dict] = None) -> bool:
        """
        Save cookies to the pickle file.
        
        This method serializes and stores cookies to a file. If no cookies are
        provided, it retrieves all cookies from the current browser session.
        
        Args:
            cookies (list[dict], optional): List of cookie dictionaries to save.
                If None, gets cookies from the current browser session.
                Defaults to None.
        
        Returns:
            bool: True if cookies were saved successfully, False otherwise.
        
        Example:
            >>> # Save current browser cookies
            >>> cookie_manager.save_cookies()
            >>> 
            >>> # Save specific cookies
            >>> custom_cookies = [{'name': 'session', 'value': '12345'}]
            >>> cookie_manager.save_cookies(custom_cookies)
        """
        try:
            if cookies is None:
                cookies = self.driver.get_cookies()
            with open(self.cookie_file, "wb") as f:
                pickle.dump(cookies, f)
            return True
        except Exception as e:
            print(f"Error saving cookies: {e}")
            return False

    def load_cookies_if_needed(self) -> bool:
        """
        Load cookies only if no cookies exist in the current browser session.
        
        This method checks if there are any cookies in the current browser
        session. If no cookies exist and a cookie file is available, it loads
        the cookies from the file.
        
        Returns:
            bool: True if cookies are present or were loaded successfully,
                False if loading failed.
        
        Example:
            >>> # This will only load cookies if the browser has none
            >>> cookie_manager.load_cookies_if_needed()
        """
        if not self.driver.get_cookies() and os.path.exists(self.cookie_file):
            return self.load_cookies()
        return True

    def get_expired_cookies(self) -> list:
        """
        Get a list of expired cookies from the current browser session.
        
        This method checks all cookies in the current session and returns
        those that have expired based on their 'expiry' timestamp.
        
        Returns:
            list: List of expired cookie dictionaries. Returns empty list if
                no expired cookies are found.
        
        Example:
            >>> expired = cookie_manager.get_expired_cookies()
            >>> for cookie in expired:
            ...     print(f"Expired cookie: {cookie['name']}")
        """
        expired = []
        for cookie in self.driver.get_cookies():
            if 'expiry' in cookie:
                if cookie['expiry'] < time.time():
                    expired.append(cookie)
        return expired

    def clear_expired_cookies(self) -> None:
        """
        Remove all expired cookies from the current browser session.
        
        This method identifies expired cookies using get_expired_cookies()
        and deletes them from the browser session. Any errors during deletion
        are silently ignored.
        
        Returns:
            None
        
        Example:
            >>> # Clear all expired cookies
            >>> cookie_manager.clear_expired_cookies()
            >>> print("Expired cookies removed")
        """
        for cookie in self.get_expired_cookies():
            try:
                self.driver.delete_cookie(cookie['name'])
            except Exception:
                continue

    def load_cookies_from_file(self, cookie_file: str = None) -> bool:
        """
        Load cookies from a specified pickle file.
        
        This method allows loading cookies from a custom file path, which is
        useful for switching between different cookie sessions.
        
        Args:
            cookie_file (str, optional): Path to the cookie file to load.
                If None, uses the default cookie_file attribute.
                Defaults to None.
        
        Returns:
            bool: True if cookies were loaded successfully, False otherwise.
        
        Example:
            >>> # Load from default file
            >>> cookie_manager.load_cookies_from_file()
            >>> 
            >>> # Load from a different file
            >>> cookie_manager.load_cookies_from_file("backup_cookies.pkl")
        """
        file_to_load = cookie_file or self.cookie_file
        try:
            if os.path.exists(file_to_load):
                with open(file_to_load, "rb") as f:
                    cookies = pickle.load(f)
                    for cookie in cookies:
                        try:
                            self.driver.add_cookie(cookie)
                        except Exception:
                            continue
                    return True
        except Exception as e:
            print(f"Error loading cookies from {file_to_load}: {e}")
        return False

    def switch_cookie_file(self, new_file: str) -> None:
        """
        Switch to a different cookie file for future operations.
        
        This method changes the default cookie file path used by the instance
        for save and load operations.
        
        Args:
            new_file (str): New cookie file path to use
        
        Returns:
            None
        
        Example:
            >>> # Switch to a different cookie file
            >>> cookie_manager.switch_cookie_file("user_session.pkl")
            >>> # Now all operations will use the new file
            >>> cookie_manager.save_cookies()
        """
        self.cookie_file = new_file

    def __str__(self) -> str:
        """
        String representation of the Cookie instance.
        
        Returns:
            str: A string describing the Cookie instance
        
        Example:
            >>> print(cookie_manager)
            class cookie as allykit
        """
        return f"class cookie as allykit"

