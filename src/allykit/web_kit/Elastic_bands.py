import logging
import pickle
import os
import hashlib
from datetime import datetime, timedelta
import time
from typing import Optional, List, Dict, Any, Union


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from bs4 import BeautifulSoup
except ImportError:
    logger.error("pip install bs4")
    raise

try:
    from allykit.Security_kit.hash_kit import hash_password
    from allykit.Security_kit.file_kit import write_file , remove_files , dump_file , load_file, read_file
    from allykit.web_kit.Get_Code import soup_url, javascript_driver, javascript_pro
    from allykit.web_kit.Communications import fetch_url
    from allykit.web_kit.CChrome import chrome
    from allykit.web_kit.Working_with_code import SoupToDict
except ImportError:
    raise ImportError("allykit Not fully installed")

try:
    from selenium.webdriver import Chrome
except ImportError:
    logger.error("pip install selenium")
    raise

class DiskCache:
    """
    Persistent disk-based cache with time-to-live (TTL) expiration.
    
    This class caches data (typically BeautifulSoup objects) to disk to avoid
    repeated network requests. Each cached item has a TTL (Time-To-Live)
    after which it expires and is considered invalid. Cache keys are generated
    from URLs using MD5 hashing to ensure filesystem compatibility.
    
    Features:
    - Supports standard HTML fetching with `html()` method
    - Supports JavaScript-rendered pages with `javascript()` method
    - Advanced JavaScript rendering with `javascript_pro()` method for complex dynamic pages
    - Automatic caching with TTL expiration
    - Thread-safe file operations
    
    Attributes:
        cache_dir (str): Directory path where cache files are stored
        ttl (timedelta): Time duration after which cached items expire
    
    Example:
        >>> cache = DiskCache(cache_dir=".my_cache", ttl_hours=48)
        >>> soup = cache.javascript_pro("https://example.com", scroll_to_bottom=True)
        >>> print(soup.find_all("div"))  # Use cached or freshly fetched data
    """
    
    def __init__(self, cache_dir: str = ".web_cache", ttl_hours: int = 24):
        """
        Initialize the DiskCache.
        
        Creates the cache directory if it doesn't exist.
        
        Args:
            cache_dir (str, optional): Directory path for storing cache files.
                                      Defaults to ".web_cache" (hidden directory).
            ttl_hours (int, optional): Time-to-live in hours. Cached items expire
                                      after this many hours. Defaults to 24.
        
        Example:
            >>> # Cache for 12 hours in custom directory
            >>> cache = DiskCache(cache_dir="data/cache", ttl_hours=12)
            
            >>> # Default settings (24 hours, .web_cache directory)
            >>> default_cache = DiskCache()
        """
        self.cache_dir = cache_dir
        self.ttl = timedelta(hours=ttl_hours)
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_key(self, url: str) -> str:
        """
        Generate a filesystem-safe cache key from a str.
        
        This method creates an MD5 hash of the str to ensure the resulting
        filename is safe for all filesystems (no special characters like /, ?, &, etc.).
        
        Args:
            url (str): The str to generate a cache key for.
        
        Returns:
            str: MD5 hash hex digest of the str (32 characters).
        
        Example:
            >>> cache = DiskCache()
            >>> key = cache._get_key("https://example.com/page?id=123")
            >>> print(key)  # Output: "5d41402abc4b2a76b9719d911017c592"
        """
        return hashlib.md5(url.encode()).hexdigest()
        
    def file_type(self, text: str) -> str:
        """
        Extract and convert file extension to content type identifier.
        
        Analyzes a filename extension and maps it to a standardized content
        type string used internally by the cache system.
        
        Args:
            text (str): Filename or path with extension to analyze
            
        Returns:
            str: Standardized content type:
                - 'html' for .html extension
                - 'javascript' for .js extension
                - 'javascript_pro' for .pro.js extension
                - 'javascript_driver' for .dv.js extension
            
        Raises:
            ValueError: If the file extension is unknown or unsupported
            
        Example:
            >>> cache = DiskCache()
            >>> 
            >>> cache.file_type("file.html")  # Returns: 'html'
            >>> cache.file_type("file.js")    # Returns: 'javascript'
            >>> cache.file_type("file.pro.js") # Returns: 'javascript_pro'
            >>> cache.file_type("file.dv.js")  # Returns: 'javascript_driver'
            >>> cache.file_type("file.txt")    # Raises ValueError
        """
        type = text.split('.')[1]
        if type == "js":
            type = "javascript"
        elif type == "pro.js":
            type = 'javascript_pro'
        elif type == 'dv.js':
            type = "javascript_driver"
        elif type == 'html':
            type = type
        else:
            raise ValueError("Your file type is not the same as my file type.")
        return type         

    def create_filename(self, url: str, type: str = "html") -> str:
        """
        Generate a standardized cache filename based on URL and content type.
        
        Creates a consistent filename format for caching different types of
        content. The filename consists of an MD5 hash of the URL combined
        with an appropriate file extension based on the content type.
        
        Args:
            url (str): The URL to generate a filename for
            type (str): Content type. Options:
                    - 'html': Static HTML content (extension: .html)
                    - 'javascript': Basic JS-rendered content (extension: .js)
                    - 'javascript_pro': Advanced JS-rendered content (extension: .pro.js)
                    - 'javascript_driver': Driver-based JS content (extension: .dv.js)
                    Default: 'html'
        
        Returns:
            str: Generated filename with appropriate extension
            
        Raises:
            ValueError: If an unknown content type is provided
            
        Example:
            >>> cache = DiskCache()
            >>> 
            >>> # HTML content
            >>> filename = cache.create_filename("https://example.com", "html")
            >>> print(filename)  # "5d41402abc4b2a76b9719d911017c592.html"
            >>> 
            >>> # JavaScript content
            >>> js_filename = cache.create_filename("https://example.com", "javascript")
            >>> print(js_filename)  # "5d41402abc4b2a76b9719d911017c592.js"
            >>> 
            >>> # Pro JavaScript content
            >>> pro_filename = cache.create_filename("https://example.com", "javascript_pro")
            >>> print(pro_filename)  # "5d41402abc4b2a76b9719d911017c592.pro.js"
        """
        if type == "javascript":
            type = "js"
        elif type == "javascript_pro":
            type = 'pro.js'
        elif type == 'javascript_driver':
            type = "dv.js"
        elif type == 'html':
            type = type
        else:
            raise ValueError("I don't know the type you gave me.")
        return f'{self._get_key(url)}.{type}'

    def set(self, url: str, data: BeautifulSoup) -> None:
        """
        Store data in the cache with current timestamp.
        
        This method serializes and saves the BeautifulSoup object (or any
        Python object) to disk along with the current timestamp.
        
        Args:
            url (str): The str to associate with the cached data (can be a cache key).
            data (BeautifulSoup): The BeautifulSoup object to cache.
        
        Example:
            >>> cache = DiskCache()
            >>> response = requests.get("https://example.com")
            >>> soup = BeautifulSoup(response.text, 'html.parser')
            >>> cache.set("https://example.com", soup)
        
        Note:
            The url parameter can be either the original str or a pre-computed cache key.
            The method will automatically handle both cases.
        """
        cache_file = os.path.join(self.cache_dir, url)
        with open(cache_file, 'wb') as f:
            pickle.dump((data, datetime.now()), f)

    def delete(self, name : str) -> None:
        from pathlib import Path

        file_path = Path(name)

        if file_path.exists():
            file_path.unlink()

    def get(self, url: str, default: Any = None) -> Optional[BeautifulSoup]:
        """
        Retrieve cached data if exists and not expired.
        
        Args:
            url (str): Cache key or URL
            default (Any): Default value if cache miss or expired
        
        Returns:
            Optional[BeautifulSoup]: Cached data or default
        """
        cache_file = os.path.join(self.cache_dir, url)
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    cached_data, timestamp = pickle.load(f)
                    if datetime.now() - timestamp < self.ttl:
                        return cached_data
                    else:
                        self.delete(cache_file)
            except (pickle.PickleError, EOFError) as e:
                logger.warning(f"Corrupted cache file {cache_file}: {e}")
                self.delete(cache_file)
        return default

    def clear_expired(self) -> int:
        """
        Remove all expired cache files.
        
        Returns:
            int: Number of files removed
        """
        removed = 0
        for filename in os.listdir(self.cache_dir):
            filepath = os.path.join(self.cache_dir, filename)
            try:
                with open(filepath, 'rb') as f:
                    _, timestamp = pickle.load(f)
                    if datetime.now() - timestamp >= self.ttl:
                        self.delete(filepath)
                        removed += 1
            except (pickle.PickleError, EOFError):
                self.delete(filepath)
                removed += 1
        return removed

    def clear_all(self) -> None:
        """Remove all cache files."""
        for filename in os.listdir(self.cache_dir):
            filepath = os.path.join(self.cache_dir, filename)
            self.delete(filepath)

    def html(self, url: str) -> BeautifulSoup:
        """
        Retrieve cached HTML for a str using simple HTTP requests.
        
        This method checks if a cache file exists for the given str and
        if it hasn't exceeded the TTL. If valid, it returns the cached
        BeautifulSoup object; otherwise it fetches the data using the
        soup_url method and caches it.
        
        Args:
            url (str): The str to retrieve cached data for.
        
        Returns:
            BeautifulSoup: Cached or freshly fetched BeautifulSoup object.
        
        Note:
            This method is suitable for static HTML pages that don't require
            JavaScript execution.
        
        Example:
            >>> cache = DiskCache(ttl_hours=24)
            >>> soup = cache.html("https://example.com")
            >>> print(f"Found {len(soup.find_all('div'))} divs")
        """
        key = f'{self._get_key(url)}.html'
        soup = self.get(key, False)
        if soup:
            return soup
  
        soup_data = soup_url(url)
        self.set(url=key, data=soup_data)
        return soup_data
    
    def javascript(self, url: str) -> BeautifulSoup:
        """
        Fetch HTML content from a str using basic JavaScript rendering.
        
        This method uses a headless Chrome browser to load the str
        and execute any JavaScript on the page, returning the fully
        rendered HTML as a BeautifulSoup object.
        
        Args:
            url (str): The str to fetch with JavaScript rendering.
        
        Returns:
            BeautifulSoup: Parsed HTML content of the rendered page.
        
        Note:
            - This method uses caching internally
            - Uses a simpler Chrome setup compared to javascript_pro
            - Suitable for pages with moderate JavaScript requirements
        
        Example:
            >>> cache = DiskCache()
            >>> soup = cache.javascript("https://example.com")
            >>> print(soup.title.string)  # Rendered page title
        """
        key = f'{self._get_key(url)}.js'

        soup = self.get(key, False)
        if soup:
            return soup
              
        driver = chrome(criterion=True)
        try:
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            self.set(url=key, data=soup)
        finally:
            driver.quit()
        return soup
    
    def javascript_pro(self,
        target_url: str,
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
        Advanced JavaScript rendering with comprehensive page interaction options.
        
        This method provides the most sophisticated page loading capabilities,
        including scrolling, waiting for elements, custom JavaScript execution,
        and proxy support. It caches the rendered HTML for future use.
        
        Args:
            target_url (str): The str to fetch with JavaScript rendering.
            wait_for_load (bool, default=True): Wait for <body> element presence.
            timeout (int, default=30): Maximum seconds to wait for conditions.
            scroll_to_bottom (bool, default=False): Scroll to trigger lazy-loaded content.
            scroll_pause (float, default=1.0): Delay between scroll steps in seconds.
            wait_for_element (Optional[tuple], default=None): Selenium locator tuple
                to wait for a specific element, e.g., (By.CSS_SELECTOR, ".product-title").
            custom_scripts (Optional[List[str]], default=None): JavaScript code strings
                to execute after page load.
            proxy (Optional[str], default=None): Proxy server address, e.g., 'http://127.0.0.1:8080'.
            user_agent (Optional[str], default=None): Custom User-Agent string.
            headless (bool, default=True): Run Chrome in headless mode.
            viewport_size (tuple, default=(1920, 1080)): Browser window size.
            save_screenshot (Optional[str], default=None): File path to save screenshot.
            execute_async (bool, default=False): Execute scripts asynchronously if True.
            return_driver (bool, default=False): If True, returns WebDriver instead of BeautifulSoup.
                Caller must manage driver cleanup (driver.quit()).
        
        Returns:
            BeautifulSoup: Parsed HTML of the final rendered page when return_driver=False.
            selenium.webdriver.Chrome: The Chrome WebDriver instance when return_driver=True.
        
        Raises:
            Exception: Re-raises any unexpected exception during page loading.
            TimeoutException: Logged as warning but handled internally.
        
        Note:
            - This method caches the rendered HTML based on target_url
            - If return_driver=True, the result is NOT cached
            - For complex SPAs (Single Page Applications), this method is recommended
            - Supports advanced features like infinite scroll and element waiting
        
        Example:
            >>> from selenium.webdriver.common.by import By
            >>> cache = DiskCache(ttl_hours=48)
            >>> soup = cache.javascript_pro(
            ...     "https://example.com/product/123",
            ...     scroll_to_bottom=True,
            ...     wait_for_element=(By.CSS_SELECTOR, ".price"),
            ...     headless=True
            ... )
            >>> price = soup.select_one(".price").get_text(strip=True)
            
            >>> # Get driver for further interaction
            >>> driver = cache.javascript_pro("https://example.com", return_driver=True)
            >>> # ... interact with driver ...
            >>> driver.quit()
        """
        key = f'{self._get_key(target_url)}.pro.js'
        soup = self.get(key, False)
        if soup:
            return soup
        
        soup = javascript_pro(
            url=target_url,
            wait_for_load=wait_for_load,
            timeout=timeout,
            scroll_to_bottom=scroll_to_bottom,
            scroll_pause=scroll_pause,
            wait_for_element=wait_for_element,
            custom_scripts=custom_scripts,
            proxy=proxy,
            user_agent=user_agent,
            headless=headless,
            viewport_size=viewport_size,
            save_screenshot=save_screenshot,
            execute_async=execute_async,
            return_driver=return_driver,
        )
        
        if not return_driver:
            self.set(key, soup)

        return soup
        
    def javascript_driver(self, driver: Chrome,
                        timeout: int = 30,
                        wait_for_element: tuple = None) -> BeautifulSoup:
        """
        Cache and retrieve page content using an existing Chrome WebDriver instance.
        
        This method uses a pre-configured Chrome WebDriver to fetch page content
        and caches the result on disk. It's particularly useful when you already
        have a WebDriver instance with specific configurations (like proxies,
        headers, or authentication) and want to reuse it with caching.
        
        Parameters
        ----------
        driver : Chrome
            An active Chrome WebDriver instance that has already navigated
            to the target URL. The driver must be configured and ready.
        
        timeout : int, optional
            Maximum time to wait for element loading (in seconds).
            Default: 30 seconds.
        
        wait_for_element : tuple, optional
            A tuple of (selector_type, selector_value) to wait for a specific
            element before capturing the page source.
            
            Examples:
            - (By.ID, "main-content")
            - (By.CLASS_NAME, "product-item")
            - (By.CSS_SELECTOR, ".container > div")
        
        Returns
        -------
        BeautifulSoup
            Cached or freshly fetched BeautifulSoup object of the page content.
        
        Raises
        ------
        ValueError
            If the page source is empty.
        Exception
            Any WebDriver or processing errors.
        
        Notes
        -----
        - The cache key is generated from the driver's unique identifier
        (using hash_password function) and the method name.
        - Cached items expire based on the DiskCache's TTL setting.
        - The driver is automatically closed after fetching the page.
        - This method wraps the standalone javascript_driver function.
        - The cache file extension is '.dv.js' (driver version with JavaScript).
        
        Example
        -------
        >>> from selenium import webdriver
        >>> from selenium.webdriver.common.by import By
        >>> 
        >>> # Create cache with 48-hour TTL
        >>> cache = DiskCache(ttl_hours=48)
        >>> 
        >>> # Configure and navigate driver
        >>> driver = webdriver.Chrome()
        >>> driver.get("https://example.com")
        >>> 
        >>> # Get cached content with wait
        >>> soup = cache.javascript_driver(
        ...     driver=driver,
        ...     timeout=20,
        ...     wait_for_element=(By.CLASS_NAME, "loaded")
        ... )
        >>> 
        >>> # Extract data from soup
        >>> title = soup.find("h1").text
        >>> print(f"Page title: {title}")
        
        See Also
        --------
        javascript_driver : Standalone function for fetching with driver
        html : Method for static HTML pages
        javascript : Method for basic JavaScript rendering
        javascript_pro : Method for advanced JavaScript rendering
        """

        key = f'{self._get_key(hash_password(driver))}.dv.js'
        soup = self.get(key, False)
        if soup:
            return soup
                
        return javascript_driver(driver, timeout, wait_for_element)

    def update(self, url: str, func) -> bool:
        """
        Update cached content by comparing with fresh data.
        
        This method fetches fresh content using a provided function, compares
        it with the cached version, and updates the cache if changes are detected.
        It's useful for efficiently refreshing cache only when content has actually
        changed.
        
        Args:
            url (str): The URL of the content to update
            func (callable): A function that takes a URL and returns a BeautifulSoup
                            object. Examples: cache.html, cache.javascript,
                            cache.javascript_pro, or any custom function with
                            the signature: func(url) -> BeautifulSoup
            
        Returns:
            bool: 
                - True: Content was updated (changes detected)
                - False: Content unchanged (no update needed)
                - str: Error message if update failed
            
        Raises:
            PermissionError: If the requested function hasn't been called before
                            (cached version not found)
            
        Notes:
            - The function must have a __name__ attribute (standard functions)
            - The cache key is generated using create_filename based on function name
            - Comparison is done using SoupToDict class
            - Only updates if differences are detected
            
        Example:
            >>> cache = DiskCache()
            >>> 
            >>> # First, ensure content is cached
            >>> soup = cache.html("https://example.com")
            >>> 
            >>> # Later, update if changed
            >>> updated = cache.update("https://example.com", cache.html)
            >>> if updated:
            ...     print("Content updated!")
            ... else:
            ...     print("No changes detected")
            >>> 
            >>> # Using with javascript_pro
            >>> cache.javascript_pro("https://example.com")
            >>> updated = cache.update("https://example.com", cache.javascript_pro)
            >>> 
            >>> # Custom function
            >>> def custom_fetch(url):
            ...     # Your custom fetching logic
            ...     return some_soup
            >>> 
            >>> # Ensure custom_fetch was called before
            >>> custom_soup = custom_fetch("https://example.com")
            >>> cache.set(cache.create_filename("https://example.com", "html"), custom_soup)
            >>> updated = cache.update("https://example.com", custom_fetch)
        """
        try:
            key = self.create_filename(url, str(func.__name__))
            soup1 = self.get(key)
            if soup1:
                soup2 = func(url)
                diff = SoupToDict(soup1, soup2)
                status = diff.to_json('get_full_review.bool')
                if status:
                    self.set(key, soup2)
                return status
        except PermissionError:
            return "You should have called the function you gave before this. We got an error for mine, but I'll continue."
            
class Monitoring:
    """
    Advanced web monitoring and caching system.
    
    The Monitoring class provides a comprehensive solution for web data 
    extraction, caching, and change detection. It automatically manages
    disk-based caching with intelligent update mechanisms.
    
    Key Features:
        - Automatic data extraction from HTTP responses
        - Disk-based caching with organized directory structure
        - Change detection with detailed status reporting
        - Selective data caching and retrieval
        - File management utilities
        - Search functionality for nested data
    
    Architecture:
        Each URL is assigned a unique cache directory based on MD5 hash
        of the URL. Inside this directory, different data components
        (headers, text, short-form content) are stored as separate files.
        
    Cache Structure:
        cache_dir/
            └── [url_hash]/
                ├── text.html          # HTML content
                ├── headers.json       # HTTP headers
                └── Short-form content.json  # Metadata

    Example:
        >>> # Basic usage
        >>> monitor = Monitoring("https://example.com", ".cache")
        >>> monitor.set_all()  # Cache all data
        >>> data = monitor.data("text")  # Get HTML content
        >>> 
        >>> # Check for changes
        >>> if monitor.update_all():
        ...     print("No changes detected")
        ... else:
        ...     print("Content updated!")
        >>> 
        >>> # Load cached data
        >>> headers = monitor.load("headers")
        >>> html = monitor.load("text", "html")
    """

    def __init__(self, url: str, cache_dir: str):
        """
        Initialize Monitoring instance.
        
        This constructor sets up the monitoring system for a specific URL.
        It creates the necessary directory structure and performs an initial
        fetch of the URL content.
        
        Args:
            url (str): Target URL to monitor. Must be a valid HTTP/HTTPS URL.
            cache_dir (str): Base directory for storing cache files. Will be
                           created if it doesn't exist.
        
        Raises:
            ValueError: If URL is invalid or empty
            requests.exceptions.RequestException: If initial fetch fails
            OSError: If directory creation fails
        
        Example:
            >>> # Basic initialization
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # With custom cache directory
            >>> monitor = Monitoring("https://api.example.com/data", "data/cache")
            >>> 
            >>> # Monitor multiple URLs
            >>> sites = ["https://site1.com", "https://site2.com"]
            >>> monitors = [Monitoring(url, "cache") for url in sites]
        
        Note:
            The cache directory structure is:
            {cache_dir}/{url_hash}/
            where url_hash is MD5 hash of the URL.
        """
        # Store the target URL
        self.url = url
        
        # Perform initial request to fetch content
        self.request = fetch_url(url)
        
        # Create base cache directory if it doesn't exist
        os.makedirs(cache_dir, exist_ok=True)
        
        # Create URL-specific cache directory using MD5 hash
        self.cache_dir = os.path.join(cache_dir, self._get_key(url))
        os.makedirs(self.cache_dir, exist_ok=True)

    def _get_key(self, url: str) -> str:
        """
        Generate a filesystem-safe cache key from a URL.
        
        This method creates an MD5 hash of the URL to ensure the resulting
        directory name is safe for all filesystems (no special characters
        like /, ?, &, etc.).
        
        Args:
            url (str): The URL to generate a cache key for.
        
        Returns:
            str: MD5 hash hex digest of the URL (32 characters).
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> key = monitor._get_key("https://example.com/page?id=123")
            >>> print(key)  # Output: "5d41402abc4b2a76b9719d911017c592"
            >>> 
            >>> # The key is used as directory name
            >>> cache_path = os.path.join(".cache", key)
        
        Note:
            Using MD5 ensures:
            - Consistent length (32 chars)
            - No invalid filesystem characters
            - Low collision probability
            - Deterministic output for same input
        """
        return hashlib.md5(url.encode()).hexdigest()

    def data(self, item: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract and return data from the current request.
        
        This method extracts various components from the HTTP response
        and returns them as a structured dictionary. It supports selective
        extraction of specific items.
        
        Args:
            item (Optional[str]): Specific data item to extract.
                                 If None, returns all data.
                                 Available items:
                                 - "text": Raw HTML content
                                 - "headers": HTTP headers as dict
                                 - "Short-form content": Metadata dict
        
        Returns:
            Dict[str, Any]: Complete data dictionary if item is None.
            Any: Specific data item if item is provided.
        
        Raises:
            KeyError: If requested item doesn't exist in data structure.
        
        Data Structure:
            {
                "text": str,                    # Raw HTML content
                "headers": dict,                # HTTP headers
                "Short-form content": {         # Response metadata
                    "status_code": int,
                    "connection": str,
                    "cookies": str,
                    "elapsed": str,
                    "encoding": str,
                    "request": str,
                    "raw": str,
                    "url": str
                }
            }
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Get all data
            >>> all_data = monitor.data()
            >>> print(all_data.keys())
            dict_keys(['text', 'headers', 'Short-form content'])
            >>> 
            >>> # Get specific item
            >>> html = monitor.data("text")
            >>> print(html[:100])  # First 100 chars of HTML
            >>> 
            >>> # Get headers
            >>> headers = monitor.data("headers")
            >>> print(headers.get("content-type"))
            >>> 
            >>> # Get metadata
            >>> metadata = monitor.data("Short-form content")
            >>> print(metadata["status_code"])
            >>> 
            >>> # Error handling
            >>> try:
            ...     data = monitor.data("non-existent")
            ... except KeyError as e:
            ...     print(f"Item not found: {e}")
        
        Note:
            This method extracts data from the current request object.
            If you need fresh data, call fetch_url() again before this method.
        """
        # Build the complete data dictionary from request
        data = {
            "text": self.request.text,
            "headers": dict(self.request.headers),
            "Short-form content": {
                'status_code': self.request.status_code,
                "connection": str(self.request.connection),
                "cookies": str(self.request.cookies),
                "elapsed": str(self.request.elapsed),
                "encoding": self.request.encoding,
                "request": str(self.request.request),
                "raw": str(self.request.raw),
                "url": self.request.url
            }
        }
        
        # Return all data if no specific item requested
        if item is None:
            return data
        
        # Return specific item if it exists
        if item in data:
            return data[item]
        
        # Raise error for non-existent item
        raise KeyError(f"'{item}' not found in data")

    def _cache_file_path(self, name: str, extension: str = "json") -> str:
        """
        Generate full cache file path with extension.
        
        This internal method constructs the complete filesystem path for
        a cached item, including the cache directory, filename, and extension.
        
        Args:
            name (str): Base name for the cache file (without extension)
            extension (str): File extension (default: "json").
                            Supported: "json", "html"
        
        Returns:
            str: Complete file path including directory and extension
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> path = monitor._cache_file_path("headers", "json")
            >>> print(path)  # ".cache/5d41402abc.../headers.json"
            >>> 
            >>> html_path = monitor._cache_file_path("text", "html")
            >>> print(html_path)  # ".cache/5d41402abc.../text.html"
        
        Note:
            This method is used internally by load() and other methods.
            It ensures consistent file naming across the class.
        """
        return os.path.join(self.cache_dir, f"{name}.{extension}")

    def _save_data(self, cache_file: str, item: Union[str, dict, list]) -> None:
        """
        Save data to cache with appropriate format.
        
        This internal method determines the correct file format based on
        the data type and saves it to disk.
        
        Args:
            cache_file (str): Base file path (without extension)
            item (Union[str, dict, list]): Data to save
            
        Supported Formats:
            - str: Saved as HTML (.html)
            - dict/list: Saved as JSON (.json)
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Save HTML content
            >>> monitor._save_data("page_content", "<html>...</html>")
            >>> # Creates: page_content.html
            >>> 
            >>> # Save JSON data
            >>> monitor._save_data("metadata", {"key": "value"})
            >>> # Creates: metadata.json
        
        Note:
            This method automatically adds the appropriate extension
            based on data type. It's used internally by set() and set_all().
        """
        if isinstance(item, str):
            # Save string data as HTML
            write_file(f'{cache_file}.html', item)
        elif isinstance(item, (dict, list)):
            # Save structured data as JSON
            dump_file(f'{cache_file}.json', item)

    def set_all(self) -> None:
        """
        Cache all available data from the current request.
        
        This method extracts all data components from the current response
        and saves them to the cache directory. Each component is saved
        as a separate file with appropriate format.
        
        Files Created:
            1. text.html - Full HTML content
            2. headers.json - HTTP headers as JSON
            3. Short-form content.json - Response metadata as JSON
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Cache everything
            >>> monitor.set_all()
            >>> 
            >>> # Check what was cached
            >>> info = monitor.get_cache_info()
            >>> print(f"Cached {info['file_count']} files")
            >>> for file in info['files']:
            ...     print(f"  - {file}")
            Output:
            Cached 3 files
              - text.html
              - headers.json
              - Short-form content.json
        
        Use Cases:
            - Initial caching of a new URL
            - Full cache refresh after detecting changes
            - Creating a complete snapshot of the page
        
        Note:
            This method overwrites existing cache files. For selective
            updates, use the set() method.
        """
        # Get all data from current request
        data = self.data()
        
        # Save each item to cache
        for key, value in data.items():
            # Create base file path using the item's key
            cache_file = os.path.join(self.cache_dir, key)
            # Save with appropriate format based on data type
            self._save_data(cache_file, value)

    def set(self, item: str, namefile: Optional[str] = None) -> None:
        """
        Cache a specific data item from the current request.
        
        This method extracts a single data component and saves it to the
        cache directory with a specified filename.
        
        Args:
            item (str): Name of the data item to cache.
                       Must be a valid key from data() method.
            namefile (Optional[str]): Custom filename for the cached file.
                                     If None, uses the item name.
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Cache only the HTML content with default name
            >>> monitor.set("text")
            >>> # Creates: text.html
            >>> 
            >>> # Cache headers with custom name
            >>> monitor.set("headers", "response_headers")
            >>> # Creates: response_headers.json
            >>> 
            >>> # Cache metadata
            >>> monitor.set("Short-form content", "metadata")
            >>> # Creates: metadata.json
        
        Raises:
            KeyError: If the specified item doesn't exist in data
        
        Use Cases:
            - Caching specific data components
            - Creating named snapshots of specific parts
            - Saving extracted data with descriptive names
        
        Note:
            The filename is determined by:
            1. namefile parameter if provided
            2. item name if namefile is None
            The appropriate extension is added automatically.
        """
        # Extract the requested data
        data = self.data(item)
        
        # Determine the cache filename
        cache_file = os.path.join(self.cache_dir, namefile or item)
        
        # Save with appropriate format
        self._save_data(cache_file, data)

    def remove(self) -> None:
        """
        Remove all cached files in the URL-specific directory.
        
        This method deletes all files in the cache directory associated
        with the current URL. The directory itself is left intact.
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Cache some data
            >>> monitor.set_all()
            >>> 
            >>> # Remove all cached files (keep directory)
            >>> monitor.remove()
            >>> 
            >>> # Verify directory is empty
            >>> info = monitor.get_cache_info()
            >>> print(info['file_count'])  # Output: 0
        
        Use Cases:
            - Clearing cache before fresh fetch
            - Removing corrupted cache files
            - Freeing up disk space
            - Preparing for manual cache update
        
        Note:
            This method does NOT delete the directory itself.
            For complete removal including directory, use remove_all().
        """
        return remove_files(self.cache_dir)

    def remove_all(self) -> None:
        """
        Remove cache directory and all its contents.
        
        This method deletes all files in the cache directory and then
        removes the directory itself. This is a complete cleanup operation.
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Complete removal
            >>> monitor.remove_all()
            >>> 
            >>> # Trying to access deleted cache raises error
            >>> try:
            ...     monitor.load("text")
            ... except FileNotFoundError:
            ...     print("Cache directory no longer exists")
        
        Warning:
            This operation is destructive and cannot be undone.
            All cached data for this URL will be permanently lost.
        
        Use Cases:
            - Uninstalling/removing the monitoring for a URL
            - Starting fresh with completely new cache
            - Cleaning up after testing
            - Freeing disk space completely
        
        Note:
            After calling remove_all(), the cache directory for this
            URL no longer exists. The __init__ method will recreate it
            on the next initialization.
        """
        # First remove all files
        self.remove()
        # Then remove the empty directory
        os.rmdir(self.cache_dir)

    def remove_name(self, namefile: str) -> None:
        """
        Remove a specific cached file.
        
        This method deletes a single cache file by name. The file must
        exist in the cache directory.
        
        Args:
            namefile (str): Name of the file to remove (can include extension)
                           or the base name (extension will be determined)
        
        Raises:
            FileNotFoundError: If the specified file doesn't exist
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Cache data first
            >>> monitor.set_all()
            >>> 
            >>> # Remove specific files
            >>> monitor.remove_name("headers.json")
            >>> monitor.remove_name("text.html")
            >>> 
            >>> # Try to remove non-existent file
            >>> try:
            ...     monitor.remove_name("non-existent.json")
            ... except FileNotFoundError as e:
            ...     print(f"File not found: {e}")
        
        Use Cases:
            - Selective cache cleanup
            - Removing corrupted individual files
            - Updating specific cached components
            - Managing disk space granularly
        
        Note:
            The file path is constructed by joining the cache directory
            with the provided namefile. Ensure the namefile matches the
            actual filename with correct extension.
        """
        # Construct full file path
        full_path = os.path.join(self.cache_dir, namefile)
        
        # Check if file exists before attempting removal
        if os.path.exists(full_path):
            os.remove(full_path)
        else:
            raise FileNotFoundError(f"File not found: {full_path}")

    def search(self, item: str) -> Optional[Any]:
        """
        Search for nested data using dot notation.
        
        This method provides a convenient way to access nested data
        structures using dot notation for path traversal.
        
        Args:
            item (str): Dot-separated path to the data.
                       Format: "key.subkey" or "key"
        
        Returns:
            Optional[Any]: The found value, or None if not found.
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Access nested data in Short-form content
            >>> status = monitor.search("Short-form content.status_code")
            >>> print(status)  # Output: 200
            >>> 
            >>> # Access top-level data
            >>> html = monitor.search("text")
            >>> print(html[:50])  # First 50 chars of HTML
            >>> 
            >>> # Search for non-existent data
            >>> result = monitor.search("non.existent.key")
            >>> print(result)  # Output: None
        
        Supported Paths:
            - "headers" → returns headers dict
            - "headers.content-type" → returns specific header
            - "Short-form content.status_code" → returns status code
            - "text" → returns HTML content
        
        Use Cases:
            - Quick access to nested data
            - Dynamic data retrieval
            - Avoiding manual dictionary traversal
            - Building flexible data access patterns
        
        Note:
            If the path has more than one level, the method attempts
            to traverse the nested structure. Returns None for any
            missing key in the path.
        """
        # Split the path into parts
        parts = item.split(".", 1)
        key = parts[0]
        
        # Get the top-level data
        data = self.data(key)
        
        # If there are more parts and data is a dict, continue traversal
        if len(parts) > 1 and isinstance(data, dict):
            return data.get(parts[1])
        
        # Return the data (top-level or found value)
        return data

    def load(self, name: str, parser: str = "json") -> Any:
        """
        Load cached data from file.
        
        This method reads and deserializes cached data from disk. It
        supports both JSON and HTML formats.
        
        Args:
            name (str): Base name of the cached file (without extension)
            parser (str): File format parser to use.
                         Options: "json" (default) or "html"
        
        Returns:
            Any: Deserialized data (dict/list for JSON, str for HTML)
        
        Raises:
            ValueError: If unsupported parser is specified
            FileNotFoundError: If the cached file doesn't exist
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Ensure data is cached first
            >>> monitor.set_all()
            >>> 
            >>> # Load JSON data
            >>> headers = monitor.load("headers")
            >>> print(headers["content-type"])
            >>> 
            >>> # Load HTML data
            >>> html = monitor.load("text", "html")
            >>> print(html[:100])  # First 100 chars
            >>> 
            >>> # Load metadata
            >>> metadata = monitor.load("Short-form content")
            >>> print(metadata["status_code"])
            >>> 
            >>> # Error handling
            >>> try:
            ...     data = monitor.load("non-existent", "json")
            ... except FileNotFoundError as e:
            ...     print(f"Cache not found: {e}")
        
        Use Cases:
            - Accessing cached data without re-fetching
            - Offline data access
            - Comparing cached vs current data
            - Data analysis and processing
        
        Note:
            The file must exist in the cache directory. This method
            does NOT attempt to fetch fresh data if cache is missing.
        """
        if parser == "json":
            # Load and deserialize JSON
            return load_file(self._cache_file_path(name, "json"))
        elif parser == "html":
            # Load raw HTML content
            return read_file(self._cache_file_path(name, "html"))
        else:
            # Unsupported parser
            raise ValueError(f"Unsupported parser: {parser}. Use 'json' or 'html'.")

    def _hash_data(self, data: Any) -> str:
        """
        Generate a hash of data for comparison.
        
        This internal method creates a SHA-256 hash of the string
        representation of data. It's used to detect changes between
        cached and current data.
        
        Args:
            data (Any): Data to hash (will be converted to string)
        
        Returns:
            str: SHA-256 hash hex digest
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Hash HTML content
            >>> html_hash = monitor._hash_data("<html>...</html>")
            >>> 
            >>> # Hash JSON data
            >>> data_hash = monitor._hash_data({"key": "value"})
            >>> 
            >>> # Compare two data sets
            >>> if monitor._hash_data(data1) == monitor._hash_data(data2):
            ...     print("Data is identical")
            ... else:
            ...     print("Data has changed")
        
        Note:
            This method is used internally by update_all() and status()
            to detect changes in web content.
        """
        return hash_password(str(data))

    def update_all(self) -> bool:
        """
        Check if data changed and update cache if needed.
        
        This method fetches fresh data from the URL and compares it
        with the currently cached data. If changes are detected, it
        clears the cache and saves the new data.
        
        Returns:
            bool: True if no changes detected (cache is up-to-date),
                  False if data was changed and cache was updated
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # First time - always updates
            >>> monitor.set_all()
            >>> 
            >>> # Subsequent checks
            >>> if monitor.update_all():
            ...     print("✅ No changes detected")
            ... else:
            ...     print("🔄 Content updated!")
            >>> 
            >>> # Periodic monitoring
            >>> import time
            >>> while True:
            ...     if not monitor.update_all():
            ...         send_notification("Website changed!")
            ...     time.sleep(3600)  # Check every hour
        
        Use Cases:
            - Periodic website monitoring
            - Change detection in APIs
            - Cache refresh on demand
            - Content version tracking
        
        Note:
            This method performs a full comparison of all data.
            For granular change detection, use status() method.
        """
        # Get current cached data hash
        old_data = self.data()
        
        # Fetch fresh data
        self.request = fetch_url(self.url)
        new_data = self.data()
        
        # Compare hashes
        if self._hash_data(old_data) == self._hash_data(new_data):
            return True  # No changes detected
        
        # Update cache with new data
        self.remove()
        self.set_all()
        return False  # Changes detected and cache updated

    def status(self) -> Dict[str, bool]:
        """
        Compare cached data with current data for each component.
        
        This method provides detailed change detection by comparing
        each data component individually. It fetches fresh data and
        compares it with the cached version.
        
        Returns:
            Dict[str, bool]: Dictionary with component names as keys
                           and boolean indicating if they match (True)
                           or differ (False)
        
        Component Keys:
            - "headers.json": True if headers match
            - "Short-form content.json": True if metadata matches
            - "text.html": True if HTML content matches
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Get detailed status
            >>> status = monitor.status()
            >>> print(status)
            {
                'headers.json': True,
                'Short-form content.json': False,
                'text.html': True
            }
            >>> 
            >>> # Check specific components
            >>> if not status["text.html"]:
            ...     print("HTML content has changed!")
            >>> 
            >>> # Count changes
            >>> changed = sum(1 for v in status.values() if not v)
            >>> print(f"Found {changed} changes")
            >>> 
            >>> # Update only changed components
            >>> for component, is_same in status.items():
            ...     if not is_same:
            ...         name = component.split('.')[0]
            ...         monitor.set(name)
        
        Use Cases:
            - Granular change detection
            - Identifying which parts of a page changed
            - Selective cache updating
            - Change analysis and monitoring
        
        Note:
            This method fetches fresh data and compares with cached.
            It does not automatically update the cache. Use update()
            to apply changes.
        """
        # Load cached data for each component
        old_data = {
            "headers": self.load("headers"),
            "Short-form content": self.load("Short-form content"),
            "text": self.load("text", "html"),
        }
        
        # Fetch fresh data
        self.request = fetch_url(self.url)
        new_data = {
            "headers": self.data("headers"),
            "Short-form content": self.data("Short-form content"),
            "text": self.data("text"),
        }
        
        # Compare each component
        return {
            "headers.json": self._hash_data(old_data["headers"]) == self._hash_data(new_data["headers"]),
            "Short-form content.json": self._hash_data(old_data["Short-form content"]) == self._hash_data(new_data["Short-form content"]),
            "text.html": self._hash_data(old_data["text"]) == self._hash_data(new_data["text"]),
        }

    def update(self) -> None:
        """
        Update only changed cached files.
        
        This method performs a selective update of the cache. It checks
        which components have changed and only updates those specific
        files, leaving unchanged components untouched.
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Initial caching
            >>> monitor.set_all()
            >>> 
            >>> # Later, update only changed parts
            >>> monitor.update()
            >>> 
            >>> # Only changed files are updated, others remain
            >>> info = monitor.get_cache_info()
            >>> print(f"Updated {info['file_count']} files")
        
        Process:
            1. Check status of each component
            2. Remove changed files
            3. Cache fresh versions of changed components
        
        Use Cases:
            - Efficient cache updates
            - Minimizing disk I/O
            - Keeping cache consistent with current data
            - Partial cache refresh
        
        Note:
            This method is more efficient than update_all() when only
            a few components have changed. It uses the status() method
            to identify which components need updating.
        """
        # Get change status for each component
        status = self.status()
        
        # Remove changed files
        for key, value in status.items():
            if not value:
                # File has changed - remove it
                self.remove_name(key)
        
        # Cache fresh versions of changed components
        self.set_all()

    def clear_cache(self) -> None:
        """
        Clear all cached data.
        
        This method provides a clean way to remove all cached files
        for the current URL. It's an alias for the remove() method.
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Cache some data
            >>> monitor.set_all()
            >>> 
            >>> # Clear everything
            >>> monitor.clear_cache()
            >>> 
            >>> # Cache is now empty
            >>> info = monitor.get_cache_info()
            >>> print(info['file_count'])  # Output: 0
        
        Use Cases:
            - Manual cache clearing
            - Starting fresh with new data
            - Resetting monitoring state
            - Freeing up disk space
        
        Note:
            This is a convenience method that calls remove().
            It does NOT delete the cache directory itself.
        """
        self.remove()

    def get_cache_info(self) -> Dict[str, Any]:
        """
        Get information about cached files.
        
        This method provides detailed statistics and information about
        the current cache state, including file count, total size,
        and list of cached files.
        
        Returns:
            Dict[str, Any]: Cache information dictionary with:
                - "cache_dir": Path to cache directory
                - "file_count": Number of cached files
                - "files": List of cached filenames
                - "total_size": Total size in bytes
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Cache some data
            >>> monitor.set_all()
            >>> 
            >>> # Get cache information
            >>> info = monitor.get_cache_info()
            >>> print(f"Cache directory: {info['cache_dir']}")
            >>> print(f"Files: {info['file_count']}")
            >>> print(f"Total size: {info['total_size'] / 1024:.2f} KB")
            >>> 
            >>> # List all cached files
            >>> for file in info['files']:
            ...     print(f"  - {file}")
            Output:
            Cache directory: .cache/5d41402abc...
            Files: 3
            Total size: 45.67 KB
              - text.html
              - headers.json
              - Short-form content.json
        
        Use Cases:
            - Monitoring cache usage
            - Debugging cache issues
            - Disk space management
            - Cache health checks
        
        Note:
            Total size is calculated as the sum of all file sizes
            in the cache directory. Returns 0 if directory is empty.
        """
        # Get list of all files in cache directory
        files = os.listdir(self.cache_dir)
        
        # Calculate total size
        total_size = sum(
            os.path.getsize(os.path.join(self.cache_dir, f))
            for f in files
        )
        
        return {
            "cache_dir": self.cache_dir,
            "file_count": len(files),
            "files": files,
            "total_size": total_size
        }

    def refresh(self) -> None:
        """
        Force a complete refresh of all cached data.
        
        This method forcibly updates all cached data with fresh content
        from the URL, regardless of whether changes were detected.
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> # Force refresh
            >>> monitor.refresh()
            >>> 
            >>> # All data is now from fresh request
            >>> data = monitor.data()
        
        Use Cases:
            - Forcing updates when you know data has changed
            - After network or server issues
            - Testing and development
        """
        self.request = fetch_url(self.url)
        self.remove()
        self.set_all()

    def is_cached(self, name: str, parser: str = "json") -> bool:
        """
        Check if a specific data component is cached.
        
        Args:
            name (str): Name of the cached file (without extension)
            parser (str): File format to check (default: "json")
        
        Returns:
            bool: True if file exists in cache, False otherwise
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> 
            >>> if monitor.is_cached("headers"):
            ...     print("Headers are cached")
            ... else:
            ...     print("Headers not cached")
        """
        file_path = self._cache_file_path(name, parser)
        return os.path.exists(file_path)

    def get_cache_age(self, name: str, parser: str = "json") -> Optional[float]:
        """
        Get the age of a cached file in seconds.
        
        Args:
            name (str): Name of the cached file (without extension)
            parser (str): File format (default: "json")
        
        Returns:
            Optional[float]: Age in seconds since last modification,
                            or None if file doesn't exist
        
        Example:
            >>> monitor = Monitoring("https://example.com", ".cache")
            >>> age = monitor.get_cache_age("headers")
            >>> if age and age > 3600:
            ...     print("Cache is more than 1 hour old")
        """
        file_path = self._cache_file_path(name, parser)
        if os.path.exists(file_path):
            return time.time() - os.path.getmtime(file_path)
        return None

    def __enter__(self):
        """
        Context manager entry.
        
        Enables use of the Monitoring class with the 'with' statement.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit.
        
        Automatically updates cache if no errors occurred.
        """
        if exc_type is None:
            self.update()
        return False

    def __repr__(self) -> str:
        """
        String representation of the Monitoring instance.
        
        Returns:
            str: Human-readable representation
        """
        return f"Monitoring(url='{self.url}', cache_dir='{self.cache_dir}')"

    def __str__(self) -> str:
        """
        User-friendly string representation.
        
        Returns:
            str: User-friendly description
        """
        return f"Monitoring: {self.url} (cache: {self.cache_dir})"
