import logging
from urllib.parse import urlparse, urlunparse, urljoin
import time
from typing import Optional, List
from contextlib import contextmanager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from bs4 import BeautifulSoup
except ImportError:
    logger.error("pip install bs4")
    raise

try:
    import requests
except ImportError:
    logger.error("pip install requests")
    raise

try:
    from allykit.web_kit import fix_url
    from allykit.web_kit.CChrome import chrome
except ImportError:
    raise ImportError("allykit Not fully installed")

try:
    from tenacity import retry, stop_after_attempt, wait_exponential
except ImportError:
    logger.error("pip install tenacity")
    raise
try:
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver import Chrome
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
except ImportError:
    logger.error("pip install selenium")
    raise


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def soup_url(url: str, header: bool = False, 
             headers: dict | None = None, 
             parser: str = "html.parser") -> BeautifulSoup:
    """
    Fetches content and converts it into a BeautifulSoup object.
    
    Args:
        url (str): The target str to fetch and parse.
        header (bool): Whether to use custom headers. Defaults to False.
        headers (dict): Custom HTTP headers. Defaults to a standard Chrome User-Agent.
        parser (str): BeautifulSoup parser to use. Defaults to "html.parser".
    
    Returns:
        BeautifulSoup: Parsed BeautifulSoup object.
    
    Raises:
        requests.exceptions.RequestException: If the request fails.
    
    Examples:
        >>> soup = soup_url("https://example.com")
        >>> soup.title
        <title>Example Domain</title>
    """
    default_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    url = fix_url(url)
    try:
        if not header:
            request = requests.get(url)
        else:
            if headers is None: 
                headers = default_headers
            request = requests.get(url, headers=headers)
        request.raise_for_status() 
        soup =  BeautifulSoup(request.text, parser)
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to retrieve str: {e}") from e
    return soup

def javascript_driver(driver: Chrome,
                      timeout: Optional[int] = 30,
                      wait_for_element: Optional[tuple] = None) -> BeautifulSoup:
    """
    Fetch page content using Selenium and convert to BeautifulSoup.
    
    Parameters
    ----------
    driver : Chrome
        Active Chrome WebDriver instance
    timeout : int, optional
        Maximum wait time for element loading (seconds), default: 30
    wait_for_element : tuple, optional
        Tuple of (selector_type, selector_value) to wait for specific element
        Example: (By.ID, "main-content")
    
    Returns
    -------
    BeautifulSoup
        BeautifulSoup object of the page content
    
    Raises
    ------
    ValueError
        If page source is empty
    
    Examples
    --------
    >>> driver = webdriver.Chrome()
    >>> driver.get("https://example.com")
    >>> soup = javascript_driver(driver)
    >>> title = soup.find("h1").text
    
    >>> # With element wait
    >>> soup = javascript_driver(driver, timeout=20, wait_for_element=(By.CLASS_NAME, "loaded"))
    
    Notes
    -----
    - Browser automatically closes after execution
    - Import By: from selenium.webdriver.common.by import By
    """

    try:       
        if wait_for_element:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(wait_for_element)
            )
        
        html = driver.page_source
        
        if not html or not html.strip():
            raise ValueError("The source page is empty")
        
        soup = BeautifulSoup(html, "html.parser")
        
    except Exception as e:
        print(e)
        
    finally:
        driver.quit()
        
    return soup

def javascript_pro(
    url: str,
    wait_for_load: bool = True,
    timeout: int = 30,
    scroll_to_bottom: bool = False,
    scroll_pause: float = 1.0,
    wait_for_element: Optional[tuple] = None,
    custom_scripts: Optional[List[str]] = None,
    proxy: Optional[str] = None,
    user_agent: Optional[str] = None,
    headless: bool = True,
    viewport_size: tuple = (1920, 1080),
    save_screenshot: Optional[str] = None,
    execute_async: bool = False,
    return_driver: bool = False,
) -> BeautifulSoup:
    """
    Load a dynamic web page using Selenium (Chrome) and return its rendered HTML.

    This helper opens the given str in a Chrome browser, optionally waits for the page
    to load, can scroll to trigger lazy-loaded content, can execute custom JavaScript
    snippets, and can wait for a specific element to appear. Finally, it parses the
    resulting page source into a BeautifulSoup object.

    Parameters
    ----------
    url : str
        The str of the page to load.

    wait_for_load : bool, default=True
        If True, the function waits for the presence of the <body> element to confirm
        that the basic page structure is available.

    timeout : int, default=30
        Maximum number of seconds to wait for Selenium conditions (e.g., element presence).
        Also used as the WebDriverWait timeout for waits inside the function.

    scroll_to_bottom : bool, default=False
        If True, repeatedly scrolls to the bottom of the page until the document height
        stops changing, which can trigger infinite scroll / lazy loading.
        After reaching the bottom, it scrolls back to the top.

    scroll_pause : float, default=1.0
        Delay (in seconds) between scroll steps when scroll_to_bottom is enabled.

    wait_for_element : Optional[tuple], default=None
        A Selenium locator tuple to wait for a specific element.
        Example: (By.CSS_SELECTOR, ".product-title")
        The function will wait until the element is present or a TimeoutException occurs.

    custom_scripts : Optional[List[str]], default=None
        A list of JavaScript code strings to execute after the initial page load.
        Each string is executed via driver.execute_script() or driver.execute_async_script()
        depending on execute_async.

    proxy : Optional[str], default=None
        Proxy server address for Chrome, e.g. 'http://127.0.0.1:8080'.
        If provided, it will be passed to Chrome via --proxy-server.

    user_agent : Optional[str], default=None
        User-Agent string to set for Chrome. If not provided, a default Chrome UA is used.

    headless : bool, default=True
        If True, runs Chrome in headless mode (no visible browser window).

    viewport_size : tuple, default=(1920, 1080)
        Browser window size as (width, height).

    save_screenshot : Optional[str], default=None
        If provided, saves a screenshot to the given file path after optional waits/scripts
        are performed.

    execute_async : bool, default=False
        If True, custom_scripts are executed using driver.execute_async_script(script).
        If False, they are executed using driver.execute_script(script).

    return_driver : bool, default=False
        If True, returns the Selenium WebDriver instance instead of returning BeautifulSoup.
        In that case, the caller is responsible for closing the driver (e.g., driver.quit()).

    Returns
    -------
    BeautifulSoup
        Parsed HTML of the final rendered page (when return_driver=False).

    selenium.webdriver.Chrome
        The Chrome WebDriver instance (when return_driver=True).

    Raises
    ------
    Exception
        Re-raises any unexpected exception that occurs during page loading or processing.
        Selenium-specific timeout errors during waits are handled internally for the
        <body> and wait_for_element steps (logged as warnings).

    Notes
    -----
    - This function is designed for pages that require JavaScript rendering.
    - If the page uses lazy loading, enabling scroll_to_bottom can improve extraction quality.
    - For best results, consider providing wait_for_element to ensure the target content is present.
    - Be careful with network conditions and timeouts for slow pages.

    Examples
    --------
    >>> soup = javascript_pro("https://example.com", scroll_to_bottom=True)
    >>> title = soup.find("title").get_text(strip=True)

    >>> from selenium.webdriver.common.by import By
    >>> soup = javascript_pro(
    ...     "https://example.com/product/123",
    ...     wait_for_element=(By.CSS_SELECTOR, ".price"),
    ...     headless=True
    ... )
    >>> price = soup.select_one(".price").get_text(strip=True)

    >>> driver = javascript_pro("https://example.com", return_driver=True)
    >>> # ... use driver ...
    >>> driver.quit()
    """
    chrome_options = Options()
    
    if headless:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
    
    chrome_options.add_argument(f"--window-size={viewport_size[0]},{viewport_size[1]}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--disable-notifications")
    
    if proxy:
        chrome_options.add_argument(f'--proxy-server={proxy}')
    
    # User-Agent
    if user_agent:
        chrome_options.add_argument(f'user-agent={user_agent}')
    else:
        chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    driver = Chrome(options=chrome_options)
    wait = WebDriverWait(driver, timeout)
    
    try:
        driver.get(url)
        time.sleep(15)          
        if wait_for_load:
            time.sleep(2)  
            try:
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            except TimeoutException:
                logger.warning("Page load failed")
        
        if custom_scripts:
            for script in custom_scripts:
                try:
                    if execute_async:
                        driver.execute_async_script(script)
                    else:
                        driver.execute_script(script)
                except Exception as e:
                    logger.error(f"Error executing script: {e}")
        
        if scroll_to_bottom:
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(scroll_pause)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)
        
        if wait_for_element:
            try:
                wait.until(EC.presence_of_element_located(wait_for_element))
            except TimeoutException:
                logger.warning(f"Element {wait_for_element} not found")
        
        if save_screenshot:
            driver.save_screenshot(save_screenshot)
        
        if return_driver:
            return driver
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        return soup
        
    except Exception as e:
        logger.error(f"Error loading page: {e}")
        raise
    finally:
        if not return_driver:
            driver.quit()

def javascript(url: str) -> BeautifulSoup:
    """
    Fetch HTML content from a str using JavaScript rendering.
    
    This function provides a standalone way to fetch web pages that
    require JavaScript execution. It uses a headless Chrome browser
    to render the page completely before parsing it with BeautifulSoup.
    
    Args:
        url (str): The str to fetch with JavaScript rendering.
    
    Returns:
        BeautifulSoup: Parsed HTML content of the rendered page.
    
    Note:
        This function does NOT use caching. Each call will fetch
        the page fresh. For caching, use the DiskCache class instead.
    
    Example:
        >>> # Fetch a JavaScript-rendered page
        >>> soup = javascript("https://example.com")
        >>> print(soup.find_all("div"))  # All divs including those rendered by JS
        
        >>> # Use with BeautifulSoup methods
        >>> titles = soup.find_all("h2")
        >>> for title in titles:
        ...     print(title.text)
    
    See Also:
        DiskCache.javascript(): Cached version of this functionality
    """
    driver = chrome(criterion=True)
    try:
        driver.get(url)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
    finally:
        driver.quit()
    return soup   
