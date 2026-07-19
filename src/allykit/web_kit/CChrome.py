import logging
from typing import Optional, Union, Dict
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC    
except ImportError:
    logger.error("pip install selenium")
    raise

def get_headless_driver() -> Chrome:
    """
    Initializes and returns a headless Chrome WebDriver instance.

    This function configures the Chrome browser to run in headless mode (without a UI),
    which is ideal for server environments, automation tasks, or scrapers.

    Returns:
        Chrome: A configured instance of the Selenium Chrome WebDriver.
    """    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")  
    chrome_options.add_argument("--window-size=1920,1080") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    return Chrome(options=chrome_options)


def chrome(
        headless: bool = False,
        service_path: str = None, 
        proxy : Optional[str] = None,
        user_agent: Optional[str] = None,
        incognito: bool = False,
        lang: str = "en-US",
        disable_images: bool = False,
        disable : bool = True) -> Chrome:
    """Runs a Chrome browser instance with customizable options using Selenium.

    This function allows fine-grained control over the Chrome browser's behavior
    for automated tasks, web scraping, or testing. It supports headless mode,
    proxy configuration, custom user agents, incognito mode, language settings,
    disabling images, and disabling various browser features like extensions
    and notifications.

    Args:
        headless (bool, optional): If True, runs the browser in headless mode.
            Defaults to False. In headless mode, Chrome runs without a GUI,
            which is useful for servers or automated tasks where a visible
            browser window is not needed. It also sets a default window size
            (1920x1080) and includes arguments for optimal headless operation
            (--disable-gpu, --no-sandbox, --disable-dev-shm-usage).
        service_path (Optional[str], optional): The absolute path to the
            ChromeDriver executable. If provided, Selenium will use this specific
            ChromeDriver. If None, Selenium will try to find ChromeDriver in the
            system's PATH or manage it automatically. Defaults to None.
        proxy (Optional[str], optional): A proxy server address to use for
            the browser. Format should be 'ip_address:port' or a full proxy str.
            Example: '127.0.0.1:8080' or 'http://user:pass@host:port'.
            Defaults to None.
        user_agent (Optional[str], optional): A custom User-Agent string to
            set for the browser. This allows the browser to mimic a specific
            browser or device. If None, the default User-Agent will be used.
            Defaults to None.
        incognito (bool, optional): If True, launches the browser in incognito
            (private browsing) mode. In this mode, browsing history, cookies,
            and site data are not saved locally after the session ends.
            Defaults to False.
        lang (str, optional): The language to set for the browser's UI and
            content negotiation. Format is typically 'language-REGION', e.g.,
            'en-US' for US English, 'fa-IR' for Persian (Iran). Defaults to
            "en-US".
        disable_images (bool, optional): If True, tells the browser not to
            load images. This can significantly speed up page loading and
            reduce bandwidth usage, which is beneficial for scraping tasks
            where only the HTML structure or text content is needed.
            Defaults to False.
        disable (bool, optional): If True, disables common browser features
            that might interfere with automated tasks or add overhead. This
            includes disabling extensions, blocking notifications, and
            disabling popup blocking. Defaults to True.

    Returns:
        Chrome: An instance of the Selenium Chrome WebDriver configured with
            the specified options.

    Raises:
        Any exceptions raised by the Selenium WebDriver during initialization.

    Example:
        >>> # Basic headless Chrome instance
        >>> driver = chrome(criterion=True)
        >>> driver.get("https://www.example.com")
        >>> print(driver.title)
        'Example Domain'
        >>> driver.quit()

        >>> # Chrome with proxy, custom user agent, and Persian language
        >>> driver = chrome(
        ...     proxy="127.0.0.1:8080",
        ...     user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        ...     lang="fa-IR",
        ...     disable_images=True
        ... )
        >>> driver.get("https://www.example.com")
        >>> driver.quit()

        >>> # Chrome instance using a specific ChromeDriver path
        >>> driver = chrome(service_path="/usr/local/bin/chromedriver")
        >>> driver.quit()
    """    
        
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")  
        chrome_options.add_argument("--window-size=1920,1080") 
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")   

    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')

    if user_agent:
        chrome_options.add_argument(f"user-agent={user_agent}")

    if incognito:
        chrome_options.add_argument("--incognito")

    if lang:
        chrome_options.add_argument(f"--lang={lang}")

    if disable:
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")

    if disable_images:
        prefs = {
            "profile.managed_default_content_settings.images": 2
        }
        chrome_options.add_experimental_option("prefs", prefs)

    if service_path:
        service = Service(executable_path=service_path)
        return Chrome(service=service, options=chrome_options)
    
    else:
        return Chrome(options=chrome_options)

@contextmanager
def browser_context(headless: bool = True):
    """
    Context manager for automatic Chrome WebDriver management.
    
    Args:
        headless (bool): Run browser without GUI if True. Defaults to True.
    
    Yields:
        WebDriver: Chrome WebDriver instance
    
    Example:
        with browser_context(headless=False) as driver:
            driver.get("https://example.com")
            print(driver.title)  # Browser auto-closes after block
    
    Raises:
        WebDriverException: ChromeDriver not found or incompatible
    """
    driver = chrome(criterion=headless)
    try:
        yield driver
    finally:
        driver.quit()

def wait_for_element(t: tuple, waits: WebDriverWait) -> Chrome:
    """
    Waits for a specific web element to be present in the DOM.

    This is a helper function that utilizes Selenium's Explicit Wait functionality
    to pause execution until the defined element is found.

    Args:
        t (tuple): A locator tuple containing the strategy and selector, 
                   e.g., (By.ID, 'element_id').
        waits (WebDriverWait): An initialized WebDriverWait object instance.

    Returns:
        WebElement: The located web element once it is present in the DOM.
    """    
    return waits.until(EC.presence_of_element_located(t))


from allykit.Automobile_kit.ProcessManager import close_chrome , close_chrome_driver, kill_chrome , kill_chrome_driver
